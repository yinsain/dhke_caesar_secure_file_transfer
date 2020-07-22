#!/usr/bin/env python3
import minilogger
ml = minilogger.minilogger('crypto.log')

def code(c):
    # single function for coding decoding
    if type(c) == type('a'):
        # perform range based ASCII comparison
        if c >= 'a' and c <= 'z':
            return (ord(c) - ord('a')) + 40
        if c >= 'A' and c <= 'Z':
            return (ord(c) - ord('A')) + 1
        if c >= '0'  and c <= '9':
            return (ord(c) - ord('0')) + 30
        else:
            spl = {' ': 0, ',': 27, '.' : 28, '?' : 29, '!' : 66, ' ' : 67 }
            return spl[c]
    else:
        # perform range based numeric ord() check
        if c >= 1 and c <= 26:
            return chr(c + 64)
        if c >= 40 and c <= 65:
            return chr(c + 57)
        if c >= 30  and c <= 39:
            return chr(c + 18)
        ispl = { 0 : ' ', 27 : ',', 28 : '.', 29 : '?', 66 : '!', 67 : ' '}
        return ispl[c]

def ROT(k, s, delim):
    # encrypt by shift of key
    s = list(s)
    ans = ''
    for c in s:
        if c == delim:
            ans = ans + delim
            continue
        ans = ans + str(code((code(c) + k) % 67))
    return ans

def UNROT(k , s, delim):
    # decrypt by shift of key
    s = list(s)
    ans = ''
    for c in s:
        if c == delim:
            ans = ans + delim
            continue
        ans = ans + str(code((code(c) - k) % 67))
    return ans

def sendSecure(sfd, key, payload, delim='|'):
    # wrapper function over send()
    ml.writer('[+] KEY ' + str(key))
    cipher = ROT(key, payload, delim)
    ml.writer('[+] PAYLOAD : ' + str(payload))
    ml.writer('[+] SHIFTED : ' + str(cipher))
    cipher = bytes(cipher, encoding='UTF-8')
    try:
        sfd.send(cipher)
    except:
        print('[!] Secure connection terminated.')

def recvSecure(sfd, key, delim='|'):
    # wrapper function over recv()
    ml.writer('[-] KEY ' + str(key))
    try:
        resp = sfd.recv(2048)
        resp = str(resp, 'ascii').strip()
        ptext = UNROT(key, resp, delim)
        ml.writer('[-] SHIFTED : ' + str(resp))
        ml.writer('[-] PLNTEXT : ' + str(ptext))
        return ptext
    except:
        print('[!] Secure connection terminated.')
