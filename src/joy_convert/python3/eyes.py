#!/usr/bin/env python3

import board
import neopixel
import sys
import signal
import os
import threading
import time

run = True

def sig_handler(sig, frame):
    run = False

class Eyes:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, 32)
        self.eyes_on = True
        self.run = True

    def start(self):
        self.t = threading.Thread(target=self._eyethread, args=())
        self.t.start()
 
    def stop(self):
        self.run = False
        self.t.join()

    def _eyethread(self):
        i = 0
        flip = 0
        while self.run == True:
            if self.eyes_on == False:
                self.pixels.fill((0,0,0))
                time.sleep(0.2)
                continue
            if flip == 0:
                i += 1
                if i >= 50:
                    flip = 1
            else:
                i -= 1
                if i <= 1:
                    flip = 0
            self.pixels.fill((i, 0, 0))
            time.sleep(0.01)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    pipe = '/tmp/eyepipe.fifo'
    try:
        os.mkfifo(pipe)
    except:
        pass

    eyes = Eyes()
    eyes.start()
    while run == True:
        print ("Waiting on pipe")
        with open(pipe, 'r') as fifo:
            for line in fifo:
                if line == 'on':
                    eyes.eyes_on = True
                    print ("Eyes on")
                elif line == 'off':
                    eyes.eyes_on = False
                    print ("Eyes off")
                elif line == 'exit':
                    run = False
                    print ("Exiting")
                else: print (line)
    eyes.stop()
