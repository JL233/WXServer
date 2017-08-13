import logging
import sys
import traceback
from threading import Thread
import itchat

class ReqWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        logging.info("Thread is %s" % self.name)

    def run(self):
        while True:
            # Get the work from the queue
            # 生成请求登录的二维码
            itchat.auto_login(False)
            #fund = self.queue.get()
            friendList = itchat.get_friends(update=True)[1:]
            for friend in friendList:
                itchat.send(r"此处为发送给好友们的消息，以测试被删好友和黑名单好友",
                    friend['UserName'])
            try:
                itchat.auto_login(False)
            except Exception as ex:
                print("%s!!!%s Unexpected error in %s:" % (fund.code, fund.name, self.getName()), sys.exc_info()[0])
                traceback.print_exc()
                self.queue.put((fund))
            finally:
                # 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
                self.queue.task_done()


if __name__ == "__main__":
    pass
