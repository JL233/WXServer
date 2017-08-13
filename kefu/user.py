import time


class User():
    def __init__(self, name,userMap):
        self.name=name;
        self.timestamp=time.time()
        self.step=0
        userMap[name]=self