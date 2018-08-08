#!/usr/bin/env python
# _*_enconding:utf-8_*_
# TIME:2018/8/7 14:38
# FILE:sql_update.py
from __builtin__ import long

import MySQLdb
import time


def getInfo():
    with open('/proc/stat') as fd:
        data = fd.readline().split()[1:]
    total = 0
    for i in data:
        total += long(i)
    return total, long(data[3])


def cpuUser():
    total, ide = getInfo()
    time.sleep(2)
    total1, ide1 = getInfo()
    total_a = total1 - total
    ide_a = ide1 - ide
    cpu = float(total_a - ide_a) / total_a * 100
    cpu = '%.2f%%' % cpu
    return cpu


def connMysql():
    try:
        con = MySQLdb.connect('127.0.0.1', 'root', 'Snynitfqm$janson10254415', 'janson_disk')
    except Exception as e:
        return ''
    return con


def dateTime():
    datetime = time.time()
    return int(datetime)


def cpuLoad():
    with open('/proc/loadavg', 'r') as fd:
        data = fd.read()
    return data

def netFlow():
    from subprocess import PIPE, Popen
    cmd_msg = Popen("sar -n DEV", stderr=PIPE, stdout=PIPE, shell=True)
    msg = cmd_msg.stdout.read().split("\n\n")[1]
    return msg


def sqlSelectMsg(db, id):
    info = "select * from {} where {}=1".format(db, id)
    return info


def sqlUpdateOrInsertMsg(msg, db, table_name, cpudata, datetime, table_id, id):
    if msg == "update":
        info = "update {} set {}='{}',add_time='{}' where {}='{}'".format(db, table_name, cpudata, datetime, table_id, id)
    elif msg == "insert":
        info = "insert into {} set {}='{}',add_time='{}' where {}='{}'".format(db, table_name, cpudata, datetime, table_id, id)
    return info


def sqlSelectAndExec(cur, cmd, cmd1, cmd2):
    cur.execute(cmd)
    data = cur.fetchall()
    if data:
        cur.execute(cmd1)
    else:
        cur.execute(cmd2)

if __name__ == '__main__':
    id = 0
    con = connMysql()
    cur = con.cursor()
    while 1:
        one_load, five_load, ten_load = cpuLoad().split()[:3]
        if id < 25:
            id += 1
        else:
            id = 1
        cpudata = cpuUser()
        datetime = dateTime()
        db = "janson_cpu"
        table_id = "janson_cpu_id"
        table_name = "cpu"
        cmd = sqlSelectMsg(db, table_id)
        cmd1 = sqlUpdateOrInsertMsg("update", db, table_name, cpudata, datetime, table_id, id)
        cmd2 = sqlUpdateOrInsertMsg("insert", db, table_name, cpudata, datetime, table_id, id)
        sqlSelectAndExec(cur, cmd, cmd1, cmd2)
        load_name = "five"
        db = "janson_load_{}".format(load_name)
        table_id = "janson_load_{}_id".format(load_name)
        table_name = "percent"
        load_one_cmd = sqlSelectMsg(db, table_id)
        load_one_cmd1 = sqlUpdateOrInsertMsg("update", db, table_name, cpudata, datetime, table_id, id)
        load_one_cmd2 = sqlUpdateOrInsertMsg("insert", db, table_name, cpudata, datetime, table_id, id)
        sqlSelectAndExec(cur, load_one_cmd, load_one_cmd1, load_one_cmd2)
        load_name = "ten"
        db = "janson_load_{}".format(load_name)
        table_id = "janson_load_{}_id".format(load_name)
        table_name = "percent"
        load_one_cmd = sqlSelectMsg(db, table_id)
        load_one_cmd1 = sqlUpdateOrInsertMsg("update", db, table_name, cpudata, datetime, table_id, id)
        load_one_cmd2 = sqlUpdateOrInsertMsg("insert", db, table_name, cpudata, datetime, table_id, id)
        sqlSelectAndExec(cur, load_one_cmd, load_one_cmd1, load_one_cmd2)
        load_name = "fifteen"
        db = "janson_load_{}".format(load_name)
        table_id = "janson_load_{}_id".format(load_name)
        table_name = "percent"
        load_one_cmd = sqlSelectMsg(db, table_id)
        load_one_cmd1 = sqlUpdateOrInsertMsg("update", db, table_name, cpudata, datetime, table_id, id)
        load_one_cmd2 = sqlUpdateOrInsertMsg("insert", db, table_name, cpudata, datetime, table_id, id)
        sqlSelectAndExec(cur, load_one_cmd, load_one_cmd1, load_one_cmd2)
        cur.execute(cmd)
        con.commit()
    con.close()
