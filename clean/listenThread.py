#!/usr/bin/python3
import json
import threading
import time

import itchat
from io import BytesIO

import requests
from PIL import Image
from itchat.content import *

from clean import sendThread

from kefu import customerService


class cleanThread(threading.Thread):
    def __init__(self, msg, threadID, name, counter):
        threading.Thread.__init__(self)
        self.msg = msg
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.newInstance = itchat.new_instance()
        self.qrDir=r'F:\PythonSpace\WXServer\kefu'+self.msg['FromUserName']+'.png'

        @self.newInstance.msg_register([TEXT, MAP, CARD, NOTE])
        def note_receive(msg):
            if msg['Status'] == 4:
                if '消息已发出，但被对方拒收了' in msg['Content']:
                    print("黑名单%s-- " % msg['User']['NickName'])
                    self.newInstance.set_alias(msg['FromUserName'],'A000僵尸-%s'%msg['User']['NickName'])
                elif '开启了朋友验证' in msg['Content'] :
                    print("开启了好友验证%s-- "%msg['User']['NickName'])
                    self.newInstance.set_alias(msg['FromUserName'],'A000需验证_%s'%msg['User']['NickName'])

    def run(self):
        statusStorageDir = 'itchat_clean.pkl'
        self.newInstance.auto_login(loginCallback=None, statusStorageDir=statusStorageDir, qrCallback=self.qrCallback)
        customerService.sendAfterLogin(self.newInstance.storageClass.nickName)
        sThread=sendThread.sendThread(self.newInstance, 1, "Thread-1", 1)
        sThread.start()
        self.newInstance.run()

    def qrCallback(self, uuid, status, qrcode):
        if status == '0':
            with open(self.qrDir, 'wb') as f:
                f.write(qrcode)
            itchat.send_image(self.qrDir, self.msg['FromUserName'])
            pass
        if status == '400':
            self.newInstance.logout()
