#!/usr/bin/python3
import json
import threading
import time

import itchat
from io import BytesIO

import requests
from PIL import Image
from itchat.content import *

import constants
from kefu import customerService


class sendThread(threading.Thread):
    def __init__(self, newInstance, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.newInstance = newInstance

    def run(self):
        list_dict_friends = self.newInstance.get_friends()
        friendsnum = len(list_dict_friends)
        i = 0
        for x in range(1,friendsnum):
            try:
                friend=list_dict_friends[x]
                NickName = friend['NickName']
                UserNameValue = friend['UserName']
                url="https://www.meipian.cn/lb5waaf"

                self.newInstance.send(constants.SEND_GROUP%url,UserNameValue)
                time.sleep(5)
            except Exception as e:
                print("消息失败:"+str(e))
            i += 1
        print("send success="+str(i))
        time.sleep(5)
        customerService.sendBeforeLogout(self.newInstance.storageClass.nickName)
        self.newInstance.logout()