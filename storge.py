#!/usr/bin/python
# _*_encoding:utf-8_*_
from __future__ import print_function

"""
# @TIME:2018/9/4 17:12
# @FILE:storge.py
# @Author:ytym00
"""
import json
import re
from subprocess import Popen, PIPE
import requests
import os


class GetDiskMessage(object):
    def __init__(self):
        self.enclosu = self.getEnclosu()[0]

    def getInfo(self, cmd):
        popen = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
        msg = popen.stdout.read()
        return msg

    def getEnclosu(self):
        cmd = "lsscsi -g"
        enclosu = re.compile(r"[0-9:]+.*JB4242.*(/dev/\w+)$", re.M)
        enclosu_msg = enclosu.findall(self.getInfo(cmd))
        return enclosu_msg

    def getUUID(self, msg):
        cmd = "blkid {}".format(msg)
        uuid_msg = re.compile(r"UUID=\"(.*)\"\sTYPE=.*", re.M)
        uuid = uuid_msg.search(self.getInfo(cmd))
        if uuid:
            uuid = uuid.group(1)
        else:
            uuid = ""
        return uuid

    def getSlotNumber(self):
        cmd = "sg_ses -p2 {}".format(self.enclosu)
        msg = self.getInfo(cmd).split("Element type:")[1]
        compile_msg = re.compile(r"Element\s+(?P<disknum>[0-9]+)[\s\S]+?status:\s(.*)[\s\S]+?Device\soff=(.*)", re.M)
        msg_list = compile_msg.findall(msg)
        slot_num,disk_num = {}, {}
        disk_msg, enclosu = self.makeJson()
        if os.path.exists('/opt/storge.json'):
            with open('/opt/storge.json', 'r') as fd:
                msg = eval(fd.read())
                for key, value in msg.items():
                     disk_num[key] = value['slot']
        if not disk_num:
            disk_num = eval(disk_msg)
        for id, status, off in msg_list:
            for key, value in disk_num.items():
                if value == id:
                    slot_num[key] = {"status": status, "slot": id, "off": off, "UUID":self.getUUID(key)}
        return slot_num

    def parseInfo(self):
        cmd = "lsscsi -L -t -g"
        ident = re.compile(
            r"[0-9:]+.*?(?P<diskname>/dev/\w+)\s+(?P<diskgroupname>/dev/\w+)[\s\S]+?bay_identifier=(?P<disknumber>[0-9]+)",
            re.M)
        parse_msg = ident.findall(self.getInfo(cmd))
        return parse_msg

    def makeJson(self):
        disk_dict = {}
        msg = self.parseInfo()
        if msg:
            for i in msg:
                disk_dict[i[0]] = i[2]
            info = json.dumps(disk_dict)
            return info, self.enclosu
        else:
            return False

if __name__ == '__main__':
    msg = GetDiskMessage()
    data = msg.getSlotNumber()
    import os
    if not os.path.exists('/opt/storge.json'):
        with open('/opt/storge.json', "w") as fd:
            fd.write(str(data))
    else:
        with open('/opt/storge1.json', "w") as ff:
            ff.write(str(data))
    print(data)
    session = requests.session()
    url = "http://127.0.0.1:8080/disk/diskMangerInfo/"
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    req = session.post(url, data=json.dumps(data), headers=headers)
    print("status_code:{}".format(req.status_code))
