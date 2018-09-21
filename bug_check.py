#!/usr/bin/python
# _*_encoding:utf-8_*_
"""
# @TIME:2018/9/21 11:14
# @FILE:bug_check.py
# @Author:ytym00
"""
# !/usr/bin/env python
import MySQLdb
import paramiko
from multiprocessing import Pool
import json
import urllib, urllib2
import datetime
import re


def mysqlInfo(cmd):
    con = MySQLdb.connect('192.168.1.57', 'trusme', '6286280300', 'cmdb')
    cur = con.cursor()
    cur.execute(cmd)
    data = cur.fetchall()
    con.commit()
    con.close()
    return data


def checkInfo():
    cmd = 'select id, sn, sn_1 from web_host where Stress_test = "running"'
    msg = mysqlInfo(cmd)
    id_dict = {}
    for each in msg:
        id_dict[each[0]] = (each[1], each[2])
    return id_dict


def debugInfo(info):
    id_list = []
    for key, value in info.items():
        if info.values().count(value) > 1:
            id_list.append(key)
    id_list = list(set(id_list))
    return id_list


def sqlDelete(info):
    for each in info:
        cmd = 'delete from web_host where id ={}'.format(each)
        print cmd


if __name__ == '__main__':
    msg = checkInfo()
    print(debugInfo(msg))

