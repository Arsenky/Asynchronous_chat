import hashlib,  binascii, hmac

class A():

    def __init__(self):
        self.y = 7

    def x(self):
        print(locals()['self'].y)

a = A()

a.x()
