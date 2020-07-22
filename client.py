#!/usr/bin/env python3

import sys
import math
import socket
import readline

import diffie
import caesar
import messageUtils
import minilogger

MAX_SIZE = int(80)
MAX_LEN = int(1024)
PORT = int(9191)
HOST = ''
ml = minilogger.minilogger('client.log')

def getlocalip(h):
    # tries to retrieve local ip in respect to server
    try:
        global PORT, HOST
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((h, PORT))
        return s.getsockname()[0]
    except:
        return HOST

def fileDownloader(s, msg, key, username, fname):
    # build a service request package with dl flag
    print('[+] Downloading file : ', fname)
    ml.writer(('[+] Downloading file : ' + fname))
    msg.createServiceRequest(username, fname, 'dl')
    msgr = msg.packMessage()
    ml.writer(('[+] MSG : ' + msgr))
    # handle request start and done
    caesar.sendSecure(s, key, msgr)
    fsize = int(caesar.recvSecure(s, key))
    ml.writer(('[+] MSG RESP : ' + str(fsize)))
    base = float(fsize)
    num = 0

    f = open(fname, 'w')
    while fsize > 0:
        buf = caesar.recvSecure(s, key)
        f.write(buf)
        fsize = fsize - len(buf)

        num = num + len(buf)
        tacks = math.floor((num/base) * 40)
        per = '%.1f' % ((num/base) * 100)
        ml.writer(('[+] MSG RESP : ' + str(per)))
        print('\r[' + ('=' * (tacks - 1)) + '>' + (' ' * (10 - tacks - 1)) + ']' + per, end='')
    print()

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('[!] Provide host to connect')
        exit()

    else:
        # Assigning a global HOST var
        HOST = sys.argv[1]
        LOCAL = getlocalip(HOST)
        ml.writer(("[!] Server : " + HOST + " Client : " + LOCAL), 0)

        # just a banner
        print('[!] Secure File Transfer ')
        while True:
            # single socket fd var needed for most work
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # single msg object, will manipulate this overall
            msg = messageUtils.Message(HOST, LOCAL)

            # main choice op
            mch = input('[-] (L)ogin | (R)egister | (E)xit : ')

            # this will allow login phase
            if mch in ['L','l']:
                print('[+] Enter details (max length : 80, otherwise snipped)')
                username = input('[-] Username : ')[:80]
                password = input('[-] Password : ')[:80]
                try:
                    # try for a connect to server
                    s.connect((HOST, PORT))
                    # returns prime and key after DHKE
                    q, key = diffie.initKeyExchg(s)
                    ml.writer("[!] Prime generated : " + str(q) + " Key : " + str(key))
                    # mould msg object for registeration
                    # and serialize for network op
                    msg.createAuthRequest(username, password)
                    m1 = msg.packMessage()
                    ml.writer("[!] MSG : " + str(m1))
                    # using our wrapper for send
                    caesar.sendSecure(s, key, m1)
                    m1 = caesar.recvSecure(s, key)
                    # unserialize the response
                    ml.writer("[!] MSG RESP: " + str(m1))
                    msgexp = msg.unpackMessage(m1)
                    #print(msgexp)
                    if msgexp[7] in ['1', 1]:
                        print('[!] Login Succseful')
                        ml.writer("[!] Login Succes")
                        while True:
                            global filelist
                            # now infinite prompt for file downloading
                            cmd = input('[ '+ username + '@' + HOST + ' ]$ ')

                            # terminate from both ends cleanly
                            if cmd == 'exit':
                                msg.createServiceRequest(username, ' ', 'exit')
                                m2 = msg.packMessage()
                                ml.writer("[!] MSG : " + str(m2))
                                caesar.sendSecure(s, key, m2)
                                break

                            # needed a good listing support
                            if cmd == 'ls':
                                msg.createServiceRequest(username, ' ', 'ls')
                                m2 = msg.packMessage()
                                ml.writer("[!] MSG : " + str(m2))
                                caesar.sendSecure(s, key, m2)
                                m1 = caesar.recvSecure(s, key)
                                ml.writer("[!] MSG RESP: " + str(m1))
                                # unserialize the response
                                msgexp = msg.unpackMessage(m1)
                                filelist = msgexp[3]
                                if filelist == '!!':
                                    print('[!] Serving no files.')
                                else:
                                    print('[+] Files on server')
                                    for x in filelist.split('!'):
                                        print(x)

                            if cmd.startswith('get'):
                                cmd = cmd.split(' ')
                                if len(cmd) == 1 or cmd[1] == '':
                                    continue
                                else:
                                    fname = cmd[1]
                                    if fname in filelist.split('!'):
                                        fileDownloader(s, msg, key, username, fname)
                                        msg.createServiceDone(username, fname, 1, ' ')
                                        msgd = msg.packMessage()
                                        ml.writer("[!] MSG : " + str(msgd))
                                        break
                                    else:
                                        print('[!] Service failed : file not present')

                    if msgexp[7] in ['3', 3]:
                        ml.writer('[!] Login Failed : username doesn\'t exist')
                        print('[!] Login Failed : username doesn\'t exist')

                    if msgexp[7] in ['2', 2]:
                        ml.writer('[!] Login Failed : bad password')
                        print('[!] Login Failed : bad password')


                except socket.error:
                    print('[!] Server seems offline : ' + HOST)

                finally:
                    # ending registration session and socket
                    print('[+] Closing Session')
                    ml.writer('[+] Session closed')
                    s.close()

            # to directly register
            elif mch in ['R','r']:
                # verify the choice taken else direct back to menu
                ch = input('[-] Initiate user registration (y|n) : ')
                if ch in ['Y', 'y']:
                    # ask for user details
                    print('[+] Enter new details (max length : 80, otherwise snipped )')
                    username = input('[-] Username : ')[:80]
                    password = input('[-] Password : ')[:80]

                    try:
                        # try for a connect to server
                        s.connect((HOST, PORT))
                        # returns prime and key after DHKE
                        q, key = diffie.initKeyExchg(s)
                        ml.writer("[!] Prime generated : " + str(q) + " Key : " + str(key))
                        # mould msg object for registeration
                        # and serialize for network op
                        msg.createLoginRequest(username, password, q)
                        m2 = msg.packMessage()
                        ml.writer("[!] MSG : " + str(m2))
                        # using our wrapper for send
                        caesar.sendSecure(s, key, m2)
                        m2 = caesar.recvSecure(s, key)
                        # unserialize the response
                        ml.writer("[!] MSG RESP : " + str(m2))
                        msgexp = msg.unpackMessage(m2)
                        if msgexp[7] in ['1', 1]:
                            print('[!] Registration Succseful : username :: ' + str(msgexp[4]))
                            ml.writer('[!] Registration Succseful : username :: ' + str(msgexp[4]))
                        if msgexp[7] in ['0', 0]:
                            print('[!] Registration failed : username already exists')
                            ml.writer('[!] Registration failed : username already exists')

                    except socket.error:
                        print('[!] Server seems offline : ' + HOST)
                        ml.writer('[!] Server seems offline : ' + HOST)

                    finally:
                        # ending registration session and socket
                        print('[+] Closing Session')
                        ml.writer('[+] Closing Session')
                        s.close()

                elif ch in ['N', 'n']:
                    continue
                else:
                    continue

            elif mch in ['E','e']:
                exit()

            else:
                print('[!] Wrong input try again')
