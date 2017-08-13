#coding=utf8

import time

import itchat
from itchat.content import *

from clean import listenThread


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    if msg['Text'] in ['二维码','QR' ,'qr']:
        newThread=listenThread.cleanThread(msg, 1, "Thread-1", 1)
        newThread.start()

@itchat.msg_register([SHARING])
def share(msg):
    itchat.send_raw_msg(msg['MsgType'], msg['Content'], msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])


def start():
    statusStorageDir = 'itchat_robbot.pkl'
    print(statusStorageDir)
    # 通过如下命令登陆，即使程序关闭，一定时间内重新开启也可以不用重新扫码。
    itchat.auto_login(hotReload=True,statusStorageDir=statusStorageDir)
    itchat.run()