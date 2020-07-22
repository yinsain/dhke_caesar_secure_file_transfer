#!/usr/bin/env python3
class minilogger:
    def __init__(self, logfile):
        self.logfile = logfile

    def writer(self, s, flag=1):
        if flag:
            with open(self.logfile, 'a+') as f:
                f.write(s + '\n')
        else:
            with open(self.logfile, 'w') as f:
                f.write(s + '\n')
