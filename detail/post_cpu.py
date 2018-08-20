#!/usr/bin/python
# _*_encoding:utf-8_*_
"""
# @TIME:2018/8/20 14:08
# @FILE:post_cpu.py
# @Author:ytym00
"""
import time

try:
    import MySQLdb
except:
    import pymysql as MySQLdb


def getCpuInfo():
    with open('/proc/stat', 'r') as fd:
        data = fd.readline().split()[1:]
    total = 0
    for i in data:
        total += long(i)
    return total, long(data[3])


def cpuUser():
    total, ide = getCpuInfo()
    time.sleep(2)
    total1, ide1 = getCpuInfo()
    total_a = total1 - total
    ide_a = ide1 - ide
    cpu = float(total_a - ide_a) / total_a * 100
    cpu = '%.2f' % cpu
    return cpu


if __name__ == '__main__':
    sql_conf = {
        "host": "192.168.1.57",
        "user": "trusme",
        "password": "6286280300",
        "database": "cmdb"
    }
    con = MySQLdb.connect(**sql_conf)
    while 1:
        now_time = int(time.time()) * 1000
        cpu_stat = cpuUser()

        cur = con.cursor()
        cmd = 'insert into detail_cpustat set now_time=\'{}\',cpu_stat=\'{}\''.format(now_time, cpu_stat)
        cur.execute(cmd)
        con.commit()
        time.sleep(1)
    con.close()
