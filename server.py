#!/usr/bin/env python

import os
import threading
import socketserver

import caesar
import diffie
import minilogger
import messageUtils
import fileUtils as fdriver
import passwordDBUtils as pdriver

MAX_SIZE = int(80)
MAX_LEN = int(1024)
PASSWORD_DB_FILE = 'password.db'
FILE_SERVING_DIR = 'uploads/'
PORT = int(9191)
HOST = '127.0.0.1'
ml = minilogger.minilogger('server.log')

# using these as global [ in memory hash table ]
passwordDB_d = dict()
# keeps a lock while modifying hash table
password_Mutex = threading.Lock()

class LoginHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # this is a universal target function for our client
        global HOST
        # initialising a blank MSG structure
        msg = messageUtils.Message(self.client_address[0], HOST)
        ml.writer(('[+] Client request : ' + self.client_address[0]))
        self.data = self.request.recv(2048).strip()
        msgString = str(self.data, 'ascii')
        ml.writer(('[+] MSG : ' + msgString))

        if msgString.startswith('DHKE1'):
            # perform DHKE
            key = diffie.performKeyExchg(self.request, msgString)
            ml.writer(('[+] Key derived : ' + str(key)))
            while True:
                msgimp = caesar.recvSecure(self.request, key)
                ml.writer(('[+] MSG : ' + msgimp))

                msgexp = msg.unpackMessage(msgimp)

                if msgexp[0] == '10':
                    # Login Registration
                    print('User registration requests')
                    password_Mutex.acquire()
                    # check whether already existing
                    if pdriver.isUserExist(passdict, msgexp):
                        print('User already registered !')
                        status = 0
                        password_Mutex.release()
                    else:
                        # then add
                        status = 1
                        pdriver.adduserpasswordDB(passdict, msgexp, PASSWORD_DB_FILE)
                        password_Mutex.release()

                    msg.createAuthReply(username=msgexp[4], status=status)
                    m1 = msg.packMessage()
                    ml.writer(('[+] MSG : ' + m1))
                    print(m1)
                    caesar.sendSecure(self.request, key, m1)
                    return

                if msgexp[0] == '30':
                    # login request
                    username = msgexp[4]
                    password_Mutex.acquire()

                    if pdriver.isUserExist(passdict, msgexp):
                        print('User registered !')
                        # check whether entered a bad password
                        if pdriver.testauthpasswordDB(passdict, msgexp):
                            status = 1
                        else:
                            status = 2
                    else:
                        # or if user doesn't exist
                        print('User not registered')
                        status = 3

                    password_Mutex.release()

                    msg.createAuthReply(username, status)
                    m1 = msg.packMessage()
                    ml.writer(('[+] MSG : ' + m1))
                    print(m1)
                    caesar.sendSecure(self.request, key, m1)
                    while True:
                        # if auth correct then drop into a shell
                        msgf = caesar.recvSecure(self.request, key)
                        ml.writer(('[+] MSG : ' + msgf))
                        msgfexp = msg.unpackMessage(msgf)
                        print(msgfexp)

                        # clean exit from shell remote
                        if msgfexp[3].strip() == 'exit':
                            return

                        # send list of served files
                        if msgfexp[3].strip() == 'ls':
                            buf = fdriver.directoryList(FILE_SERVING_DIR)
                            msg.createServiceRequest(username, ' ', buf)
                            msgf = msg.packMessage()
                            ml.writer(('[+] MSG : ' + msgf))
                            caesar.sendSecure(self.request, key, msgf)

                        # initiate download for client
                        if msgfexp[3].strip() == 'dl':
                            fname = msgfexp[8].strip()
                            count = os.stat(FILE_SERVING_DIR + fname).st_size
                            caesar.sendSecure(self.request, key, str(count))
                            ml.writer(('[+] MSG : ' + str(count)))
                            f = open(FILE_SERVING_DIR + fname)
                            while True:
                                l = f.read(1024)
                                if not l:
                                    break
                                caesar.sendSecure(self.request, key, l)
                                count = count - len(l)
                                if count == 0:
                                    break
                            # send service complete request
                            msg.createServiceDone(username, fname, count, ' ')
                            msgd = msg.packMessage()
                            ml.writer(('[+] MSG : ' + msgd))
                            return
                else:
                    return
        else:
            return

class LoginMultiThreadEnable(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    pass

if __name__ == '__main__':
    # check if password file exists or not
    try:
        assert(os.path.isfile(PASSWORD_DB_FILE))
    except:
        print('[!] No password db file exists')
        ml.writer('[!] No password db file exists')
        print('[+] Creating password db file : ', PASSWORD_DB_FILE)
        ml.writer('[+] Creating password db file : ' + PASSWORD_DB_FILE)
        with open(PASSWORD_DB_FILE, 'a') as f:
            # else build an empty one to be write-back
            f.write('{}')

    # try loading the file into our global structure
    passdict = pdriver.loadPasswordDB(PASSWORD_DB_FILE)

    # initiate multi-threaded server
    server = LoginMultiThreadEnable((HOST, PORT), LoginHandler)
    serving_at = server.server_address
    sThread = threading.Thread(target = server.serve_forever)
    sThread.start()
    print(sThread.name, ':', serving_at)
    HOST = serving_at[0]
