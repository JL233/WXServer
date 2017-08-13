#coding=utf8

import time

import itchat
from itchat.content import *



import constants
from kefu.user import User

global userMap
userMap= {}
priceMap = {'A':3,'B':5,'C':10,'D':15}

ccInstance=itchat.new_instance()
def auth(username):
    if username in userMap:
        return userMap[username]
    else:
        user=User(username,userMap)
        return user


@ccInstance.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    username=msg['FromUserName']
    user=auth(username)
    if msg['Text'] in ['A','B' ,'C','D'] and user.step==1:
        price=priceMap[msg['Text']]
        text="您好，直接之付[红包]%d￥，之后系统这边发送您二维码登录即可检测！\n" \
             "（业务比较忙，如不能及时解答，请留言！亲们登录后系统自动开始检测）"%price
        send_msg(text, username, 2)
    elif msg['Text'] == constants.RECV_RED_PACKET:
        pass
    else:
        text = u'您好，需要检测疆尸粉服务吗，请问您有多少好友呢？\n' \
               u'A：50以上\n' \
               u'B：300以上\n' \
               u'C：1000以上\n' \
               u'D：3000以上\n'
        # send_msg(text, username,1)



@itchat.msg_register([SHARING])
def share(msg):
    itchat.send_raw_msg(msg['MsgType'], msg['Content'], msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@ccInstance.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

# 收到好友邀请自动添加好友
@ccInstance.msg_register([FRIENDS])
def add_friend(msg):
    global list_customer,mainInstance

    ccInstance.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    text=u'您好，需要检测疆尸粉服务吗，请问您有多少好友呢？\n' \
         u'A：50以上\n' \
         u'B：300以上\n' \
         u'C：1000以上\n' \
         u'D：3000以上\n'
    send_msg(text, msg['RecommendInfo']['UserName'],1)

@itchat.msg_register([SYSTEM])
def system_msg(msg):
    pass

def send_msg(text,username,step=0):
    ccInstance.send_msg(text, username)
    if username in userMap:
        user = userMap[username]
    else :
        user=User(username,userMap)
    user.step=step
def sendAfterLogin(nickName):
    text=constants.SEND_QR_LOGIN
    friend=ccInstance.search_friends(nickName=nickName)
    if friend:
        ccInstance.send_msg(text, friend[0]['UserName'])
def sendBeforeLogout(nickName):
    text = constants.SEND_LOGOUT
    friend = ccInstance.search_friends(nickName=nickName)
    if friend:
        ccInstance.send_msg(text, friend[0]['UserName'])

def start():
    statusStorageDir = 'ccInstance.pkl'
    print(statusStorageDir)
    # 通过如下命令登陆，即使程序关闭，一定时间内重新开启也可以不用重新扫码。
    ccInstance.auto_login(hotReload=True,statusStorageDir=statusStorageDir)
    ccInstance.run()


