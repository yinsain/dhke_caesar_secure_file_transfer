#!/usr/bin/env python3

OP = {
    'LOGINCREATE':     10,
    'LOGINREPLY' :     20,
    'AUTHREQUEST':     30,
    'AUTHREPLY'  :     40,
    'SERVICEREQUEST' : 50,
    'SERVICEDONE' :    60
}

class Message:
    def __init__(self, HOST, LOCAL):
        # empty msg structure with all None
        self.msgbody = [None] * 10
        self.msgbody[2] = str(HOST)
        self.msgbody[1] = str(LOCAL)

    def createLoginRequest(self, username, password, q):
        self.msgbody[0] = str(OP['LOGINCREATE'])
        # self.msgbody[1] = str('localhost')
        # self.msgbody[2] = str('localhost')
        self.msgbody[3] = str(None)
        self.msgbody[4] = str(username)
        self.msgbody[5] = str(q)
        self.msgbody[6] = str(password)
        self.msgbody[7] = str(None)
        self.msgbody[8] = str(None)
        self.msgbody[9] = str(None)

    def createLoginReply(self, username, status):
        self.msgbody[0] = str(OP['LOGINREPLY'])
        self.msgbody[1], self.msgbody[2] = self.msgbody[2], self.msgbody[1]
        self.msgbody[3] = str(None)
        self.msgbody[4] = str(username)
        self.msgbody[5] = str(None)
        self.msgbody[6] = str(None)
        self.msgbody[7] = str(status)
        self.msgbody[8] = str(None)
        self.msgbody[9] = str(None)

    def createAuthRequest(self, username, password):
        self.msgbody[0] = str(OP['AUTHREQUEST'])
        # self.msgbody[1] = str('localhost')
        # self.msgbody[2] = str('localhost')
        self.msgbody[3] = str(None)
        self.msgbody[4] = str(username)
        self.msgbody[5] = str(None)
        self.msgbody[6] = str(password)
        self.msgbody[7] = str(None)
        self.msgbody[8] = str(None)
        self.msgbody[9] = str(None)

    def createAuthReply(self, username, status):
        self.msgbody[0] = str(OP['AUTHREPLY'])
        self.msgbody[1], self.msgbody[2] = self.msgbody[2], self.msgbody[1]
        self.msgbody[3] = str(None)
        self.msgbody[4] = str(username)
        self.msgbody[5] = str(None)
        self.msgbody[6] = str(None)
        self.msgbody[7] = str(status)
        self.msgbody[8] = str(None)
        self.msgbody[9] = str(None)

    def createServiceRequest(self, username, fname, buf, dummy=' '):
        self.msgbody[0] = str(OP['SERVICEREQUEST'])
        # self.msgbody[1] = str('localhost')
        # self.msgbody[2] = str('localhost')
        self.msgbody[3] = str(buf)
        self.msgbody[4] = str(username)
        self.msgbody[5] = str(None)
        self.msgbody[6] = str(None)
        self.msgbody[7] = str(None)
        self.msgbody[8] = str(fname)
        self.msgbody[9] = str(dummy)

    def createServiceDone(self, username, fname, buf, dummy=' '):
        self.msgbody[0] = str(OP['SERVICEDONE'])
        self.msgbody[1], self.msgbody[2] = self.msgbody[2], self.msgbody[1]
        self.msgbody[3] = str(buf)
        self.msgbody[4] = str(username)
        self.msgbody[5] = str(None)
        self.msgbody[6] = str(None)
        self.msgbody[7] = str(None)
        self.msgbody[8] = str(fname)
        self.msgbody[9] = str(dummy)

    def packMessage(self):
        # does a string concat for data
        return '|'.join(self.msgbody)

    def unpackMessage(self, msg):
        # splits into list
        return msg.split('|')
