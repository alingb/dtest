#!/usr/bin/python
# _*_encoding:utf-8_*_
"""
# @TIME:2018/8/31 15:17
# @FILE:sql_disk_update.py
# @Author:ytym00
"""
import datetime
import time
from subprocess import PIPE, Popen

import MySQLdb
import logging

log_file = '/var/log/sql_disk_update.log'
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def getDiskInfo():
    cmd = "df -Th | grep /dev/sd"
    info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    cmd_info = info.stdout.readlines()
    return cmd_info


def connMysql():
    try:
        con = MySQLdb.connect('127.0.0.1', 'trusme', '6286280300', 'blog')
    except Exception as e:
        logger.warning(e)
        return ''
    return con


def sqlSelectMsg(id):
    info = 'select disk_id from disk_diskinfo where disk_id={}'.format(id)
    return info


def sqlUpdateOrInsertMsg(msg, name,  type, size, used, avial, mount, id, ntime):
    global info
    if msg == "update":
        info = 'update disk_diskinfo set disk_name=\'{}\',disk_type=\'{}\',' \
               'disk_size=\'{}\', disk_used=\'{}\',disk_avail=\'{}\',' \
               'disk_back_stat=0, disk_use_stat=0,' \
               'disk_mount=\'{}\', disk_add_time=\'{}\', disk_disk_time=\'{}\'  where disk_id=\'{}\''.format(name, type,
                                                                                                             size, used,
                                                                                                             avial,
                                                                                                             mount,
                                                                                                             ntime,
                                                                                                             ntime, id)
    elif msg == "insert":
        info = 'insert into disk_diskinfo set disk_name=\'{}\',disk_type=\'{}\',' \
               'disk_size=\'{}\', disk_used=\'{}\',disk_avail=\'{}\',' \
               'disk_back_stat=0, disk_use_stat=0,' \
               'disk_mount=\'{}\', disk_add_time=\'{}\', disk_disk_time=\'{}\', disk_id=\'{}\''.format(name, type, size,
                                                                                                       used, avial,
                                                                                                       mount, ntime,
                                                                                                       ntime, id)
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
    con = connMysql()
    msg = getDiskInfo()
    ntime = datetime.datetime.now()
    table_id = 1
    if con:
        while 1:
            cur = con.cursor()
            for data in msg:
                filesystem, type, size, used, avail, use, mount = data.split()
                cmd = sqlSelectMsg(table_id)
                cmd1 = sqlUpdateOrInsertMsg("update", filesystem, type, size, used, avail, mount, table_id, ntime)
                cmd2 = sqlUpdateOrInsertMsg("insert", filesystem, type, size, used, avail, mount, table_id, ntime)
                sqlSelectAndExec(cur, cmd, cmd1, cmd2)
                table_id += 1
            con.commit()
            time.sleep(300)





