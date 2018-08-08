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
        con = MySQLdb.connect('127.0.0.1', 'root', 'Snynitfqm$janson10254415', 'janson_disk')
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


def sqlSelectMsg(db, table_id, id):
    info = 'select {} from {} where {}={}'.format(table_id, db, table_id, id)
    return info


def sqlUpdateOrInsertMsg(msg, db, table_name, cpudata, datetime, table_id, id):
    if msg == "update":
        info = "update {} set {}='{}',add_time='{}' where {}='{}'".format(db, table_name, cpudata, datetime, table_id,
                                                                          id)
    elif msg == "insert":
        info = "insert into {} set {}='{}',add_time='{}',{}='{}'".format(db, table_name, cpudata, datetime, table_id,
                                                                         id)
    return info


def sqlNetUpdateOrInsertMsg(msg, db, name, number, datetime, table_id, id):
    if msg == "update":
        info = 'update {} set name=\'{}\',number=\'{}\',add_time=\'{}\' where {}=\'{}\''.format(db, name, number, datetime,
                                                                                                table_id, id)
    elif msg == "insert":
        info = 'insert into {} set name=\'{}\',number=\'{}\',add_time=\'{}\',{}=\'{}\''.format(db, name, number, datetime,
                                                                                               table_id, id)
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
    con = connMysql()
    cur = con.cursor()
    try:
        while 1:
            one_load, five_load, fifteen_load = cpuLoad().split()[:3]
            if id < 24:
                id += 1
            else:
                id = 1
            cpudata = cpuUser()
            datetime = dateTime()
            db = "janson_cpu"
            table_id = "janson_cpu_id"
            table_name = "cpu"
            cmd = sqlSelectMsg(db, table_id, id)
            cmd1 = sqlUpdateOrInsertMsg("update", db, table_name, cpudata, datetime, table_id, id)
            cmd2 = sqlUpdateOrInsertMsg("insert", db, table_name, cpudata, datetime, table_id, id)
            sqlSelectAndExec(cur, cmd, cmd1, cmd2)

            load_name = "five"
            db = "janson_load_{}".format(load_name)
            table_id = "janson_load_{}_id".format(load_name)
            table_name = "percent"
            load_one_cmd = sqlSelectMsg(db, table_id, id)
            load_one_cmd1 = sqlUpdateOrInsertMsg("update", db, table_name, one_load, datetime, table_id, id)
            load_one_cmd2 = sqlUpdateOrInsertMsg("insert", db, table_name, one_load, datetime, table_id, id)
            sqlSelectAndExec(cur, load_one_cmd, load_one_cmd1, load_one_cmd2)

            load_name = "ten"
            db = "janson_load_{}".format(load_name)
            table_id = "janson_load_{}_id".format(load_name)
            table_name = "percent"
            load_one_cmd = sqlSelectMsg(db, table_id, id)
            load_one_cmd1 = sqlUpdateOrInsertMsg("update", db, table_name, five_load, datetime, table_id, id)
            load_one_cmd2 = sqlUpdateOrInsertMsg("insert", db, table_name, five_load, datetime, table_id, id)
            sqlSelectAndExec(cur, load_one_cmd, load_one_cmd1, load_one_cmd2)

            load_name = "fifteen"
            db = "janson_load_{}".format(load_name)
            table_id = "janson_load_{}_id".format(load_name)
            table_name = "percent"
            load_one_cmd = sqlSelectMsg(db, table_id, id)
            load_one_cmd1 = sqlUpdateOrInsertMsg("update", db, table_name, fifteen_load, datetime, table_id, id)
            load_one_cmd2 = sqlUpdateOrInsertMsg("insert", db, table_name, fifteen_load, datetime, table_id, id)
            sqlSelectAndExec(cur, load_one_cmd, load_one_cmd1, load_one_cmd2)

            net = netSpeed()
            db_on = "janson_flow_on"
            db_down = "janson_flow_down"
            table_on_id = "janson_flow_on_id"
            table_down_id = "janson_flow_down_id"
            for net_name, net_speed in net.iteritems():
                name = net_name
                net_speed_on = net_speed[1]
                net_speed_down = net_speed[0]
                db = "janson_flow_on"
                net_on_cmd = sqlSelectMsg(db_on, table_on_id, net_id)
                net_down_cmd = sqlSelectMsg(db_down, table_down_id, net_id)
                net_on_cmd1 = sqlNetUpdateOrInsertMsg("update", db_on, name, net_speed_on, datetime, table_on_id,
                                                      net_id)
                net_down_cmd1 = sqlNetUpdateOrInsertMsg("update", db_down, name, net_speed_down, datetime,
                                                        table_down_id, net_id)
                net_on_cmd2 = sqlNetUpdateOrInsertMsg("insert", db_on, name, net_speed_on, datetime, table_on_id,
                                                      net_id)
                net_down_cmd2 = sqlNetUpdateOrInsertMsg("insert", db_down, name, net_speed_down, datetime,
                                                        table_down_id, net_id)
                sqlSelectAndExec(cur, net_on_cmd, net_on_cmd1, net_on_cmd2)
                sqlSelectAndExec(cur, net_down_cmd, net_down_cmd1, net_down_cmd2)
                if net_id < len(net) * 24:
                    net_id += 1
                else:
                    net_id = 1
            cur.execute(cmd)
            con.commit()
            print "#" * 25
            time.sleep(300)
    except Exception as e:
        logger.warning(e)
        con.close()
