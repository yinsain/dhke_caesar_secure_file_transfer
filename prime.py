#!/usr/bin/env python3

from random import randrange, getrandbits

def is_prime(n, k = 6):
    # runs and check if prime or not
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

def generate_prime_candidate(length):
    # this makes sure we get a tight bound prime generated
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length = 20):
    p = 4
    # only running for 4,128 to keep bounds
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p


def prim_root(value):
    # geneates primitive root for the value field
    exp = value - 1
    for x in range(2, value):
        y = 1
        check = set()
        for y in range(1, value):
            abc = pow(x, y, value)
            if abc in check:
                break
            check.add(abc)
            if abc == 1:
                if y == exp:
                    return x
                else:
                    break
