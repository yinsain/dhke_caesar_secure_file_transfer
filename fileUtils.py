#!/usr/bin/env python

import os

def directoryList(FILE_SERVING_DIR, delim='!'):
    a = os.listdir(FILE_SERVING_DIR)
    if len(a):
        return delim.join(a)
    else:
        return str('!!')
