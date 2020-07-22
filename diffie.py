#!/usr/bin/env python
import prime
import random

def randomPrime():
    # generates a random prime number
    #return 10007 using static value
    return prime.generate_prime_number()

def generateAlpha(q):
    # generated a primitive root for it
    #return 3 using static value
    return prime.prim_root(q)

def genPrivateKey(q, ap):
    # basic modulo to generate private key
    x = random.randrange(q)
    return (x, ((ap ** x) % q ))

def genKeyDerivation(y, x, q):
    # perform key derivation for session key Kab
    return ((y ** x) % q)

def initKeyExchg(s):
    # slowest task here
    # gain random prime
    q = randomPrime()
    # calculated primitive root
    ap = generateAlpha(q)
    # generate client-side priv-pub key paur
    xa, ya = genPrivateKey(q, ap)
    # build request for initKeyExchg
    req = 'DHKE1|%d|%d|%d' % (ya, q, ap)
    reqb = bytes(req, encoding='UTF-8')
    try:
        # start the key exchange
        s.send(reqb)
        # response
        resp = s.recv(128)
        # sanitizing input
        resp = str(resp, 'ascii').strip()
        # exploding DHKE2 format
        op, yb = resp.split('|')
        # verifiying key exchange op
        if op == 'DHKE2':
            # public key of server to int
            yb = int(yb)
            # derive key
            kab = genKeyDerivation(yb, xa, q)
            # reducing to our cipher set
            return (q, ((kab % 68) + 1))
    except:
        print('[!] Failed init key exchange')
        exit()

def performKeyExchg(req, msg):
    # exploding DHKE1 msg format
    op, ya, q, ap = msg.split('|')
    if op == 'DHKE1':
        # converting string to ints
        ya = int(ya); q = int(q); ap = int(ap)
        # generate server-side priv-pub key pair
        xb, yb = genPrivateKey(q, ap)
        resp = 'DHKE2|%d' % ( yb )
        try:
            req.send(bytes(resp, 'utf-8'))
            # only step left is deriving the key
            kba = genKeyDerivation(ya, xb, q)
            # reducing to our cipher set
            return ((kba % 68) + 1)
        except:
            print('[!] Client disconnected mid key exchange')
            return None
