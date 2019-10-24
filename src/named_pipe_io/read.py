#!/usr/bin/env python

import os

PIPE = '/tmp/xy'

try:
    os.mkfifo(PIPE)
except Exception as ex:
    print ex
    exit()

with open('PIPE') as fifo:
    print "FIFO open"
    while True:
        data = fifo.read()
	if len(data) > 0:
	        print data

