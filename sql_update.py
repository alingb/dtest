#!/usr/bin/python
# _*_enconding:utf-8_*_
# TIME:2018/8/7 14:38
# FILE:sql_update.py

import time

try:
    import MySQLdb
except:
    import pymysql as MySQLdb

import logging

log_file = '/var/log/sql_update.log'
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



def getCpuInfo():
    with open('/proc/stat', 'r') as fd:
        data = fd.readline().split()[1:]
    total = 0
    for i in data:
        total += long(i)
    return total, long(data[3])


def getNetInfo():
    with open('/proc/net/dev', 'r') as fd:
        data = fd.readlines()[2:]
    net_msg = {}
    for msg in data:
        msg = msg.split()
        net_msg[msg[0][:-1]] = [msg[1], msg[9]]
    return net_msg


def netSpeed():
    net = {}
    net_msg_1 = getNetInfo()
    time.sleep(1)
    net_msg_2 = getNetInfo()
    for net_name, net_bye in net_msg_2.iteritems():
        net_receive = int(net_bye[0]) - int(net_msg_1[net_name][0])
        if net_receive > 0:
            net_receive = net_receive * 8 / 1024
        net_transmit = int(net_bye[1]) - int(net_msg_1[net_name][1])
        if net_transmit > 0:
            net_transmit = net_transmit * 8 / 1024
        net[net_name] = [net_receive, net_transmit]
    return net


def memStat():
    with open('/proc/meminfo') as fd:
        info = fd.readlines()
    for i in info:
        if i.startswith('MemTotal:'):
            total = long(i.split()[1])
            continue
        if i.startswith('MemFree:'):
            free = long(i.split()[1])
            continue
    mem = float(total - free) / total * 100
    return '%.2f' % mem


def cpuUser():
    total, ide = getCpuInfo()
    time.sleep(2)
    total1, ide1 = getCpuInfo()
    total_a = total1 - total
    ide_a = ide1 - ide
    cpu = float(total_a - ide_a) / total_a * 100
    cpu = '%.2f' % cpu
    return cpu


def connMysql():
    try:
        con = MySQLdb.connect('127.0.0.1', 'trusme', 'Trusem6286280300!', 'blog')
    except Exception as e:
        logger.warning(e)
        return ''
    return con


def dateTime():
    datetime = time.time()
    return int(datetime)


def cpuLoad():
    with open('/proc/loadavg', 'r') as fd:
        data = fd.read()
    return data


def sqlSelectMsg(db, id):
    info = 'select id from {} where id={}'.format(db, id)
    return info


def sqlUpdateOrInsertMsg(msg, db, data, datetime, id):
    global info
    if msg == "update":
        info = "update {} set stat='{}',add_time='{}' where id='{}'".format(db,  data, datetime, id)
    elif msg == "insert":
        info = "insert into {} set stat='{}',add_time='{}', id='{}'".format(db,  data, datetime, id)
    return info


def sqlNetUpdateOrInsertMsg(msg, name, on_stat, down_stat, add_time, id):
    global info
    if msg == "update":
        info = 'update detail_networkstat set name=\'{}\',on_stat=\'{}\', down_stat=\'{}\', add_time=\'{}\' where id=\'{}\''.format(
            name, on_stat, down_stat, add_time, id)
    elif msg == "insert":
        info = 'insert into detail_networkstat set name=\'{}\',on_stat=\'{}\', down_stat=\'{}\',add_time=\'{}\',id=\'{}\''.format(
            name, on_stat, down_stat, add_time, id)
    return info


def sqlSelectAndExec(cur, cmd, cmd1, cmd2):
    cur.execute(cmd)
    data = cur.fetchall()
    logger.info(data)
    if data:
        logger.info(cmd1)
        cur.execute(cmd1)
    else:
        logger.info(cmd2)
        cur.execute(cmd2)


if __name__ == '__main__':
    id = 0
    net_id = 1
    number = 2000
    con = connMysql()
    if not con:
        exit(2)
    cur = con.cursor()
    try:
        while 1:
            one_load, five_load, fifteen_load = cpuLoad().split()[:3]
            if id < number:
                id += 1
            else:
                id = 1
            data = cpuUser()
            datetime = dateTime() * 1000
            db = "detail_cpustat"
            cmd = sqlSelectMsg(db, id)
            cmd1 = sqlUpdateOrInsertMsg("update", db, data, datetime, id)
            cmd2 = sqlUpdateOrInsertMsg("insert", db, data, datetime, id)
            sqlSelectAndExec(cur, cmd, cmd1, cmd2)

            data = memStat()
            db = "detail_memstat"
            cmd = sqlSelectMsg(db, id)
            cmd1 = sqlUpdateOrInsertMsg("update", db, data, datetime, id)
            cmd2 = sqlUpdateOrInsertMsg("insert", db, data, datetime, id)
            sqlSelectAndExec(cur, cmd, cmd1, cmd2)

            net = netSpeed()
            db = "detail_networkstat"
            for net_name, net_speed in net.iteritems():
                name = net_name
                net_speed_on = net_speed[1]
                net_speed_down = net_speed[0]
                net_cmd = sqlSelectMsg(db, net_id)
                net_cmd1 = sqlNetUpdateOrInsertMsg("update", name, net_speed_on, net_speed_down, datetime, net_id)
                net_cmd2 = sqlNetUpdateOrInsertMsg("insert", name, net_speed_on, net_speed_down, datetime, net_id)
                sqlSelectAndExec(cur, net_cmd, net_cmd1, net_cmd2)
                if net_id < len(net) * number:
                    net_id += 1
                else:
                    net_id = 1
            cur.execute(cmd)
            con.commit()
            time.sleep(300)
    except Exception as e:
        logger.warning(e)
        con.close()
