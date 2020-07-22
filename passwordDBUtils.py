#!/usr/bin/env python
import json
import random
import hashlib

def isUserExist(passdict, msgexp):
    # verifies whether user exists in registered list
    if msgexp[4] == '' or msgexp[4] == ' ':
        return False
    if msgexp[4] in passdict:
        return True
    else:
        False

def adduserpasswordDB(passdict, msgexp, passfile):
    # adds users to registry
    salt     = str(random.randint(1111,9999))
    username = str(msgexp[4].strip())
    q        = str(msgexp[5].strip())
    password = str(msgexp[6].strip())

    hashptext = password + salt + q
    hashx = hashlib.sha1(hashptext.encode()).hexdigest()
    passdict[username] = [salt, hashx, q]

    print(passdict)
    dumpPasswordDB(passdict, passfile)

    return

def testauthpasswordDB(passdict, msgexp):
    # compare hashes
    username = str(msgexp[4].strip())
    password = str(msgexp[6].strip())
    salt     = str(passdict[username][0].strip())
    hash     = str(passdict[username][1].strip())
    q        = str(passdict[username][2].strip())

    hashptext = password + salt + q
    hashx = hashlib.sha1(hashptext.encode()).hexdigest()
    if hash == hashx:
        return True
    else:
        return False

def loadPasswordDB(passfile):
    # load password file on server start
    try:
        with open(passfile) as f:
            d = json.load(f)
        return d
    except:
        print('[!] PasswordDB file not present')

def dumpPasswordDB(passdict, passfile):
    # flushed password hash table to file at intervals
    try:
        with open(passfile, 'w') as f:
            json.dump(passdict, f)
    except:
        print('[!] PasswordDB file write permission denied.')
