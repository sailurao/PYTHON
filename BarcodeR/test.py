
"""
This software Runs on RaspBerry PI
This software Reads Barcode reader driver
This software is used to test Cryotouch TESTSTAND2 
@author: namam
"""

#https://iot4beginners.com/how-to-read-and-write-from-serial-port-using-raspberry-pi/#:~:text=Have%20your%20USB-Serial%20adapter%20plugged%20into%20the%20RS232,your%20serial%20connection%20to%20an%20actual%20device%201.
#Programming for Serial Write

#!/usr/bin/env python
import threading
import time

class TEST(threading.Thread):
    ser=0
    live=False
    count=0
    def __init__(self):
        threading.Thread.__init__(self)
        TEST.count=0
        return
    
     
    def EchoFunc():
        TEST.live=True
        while TEST.live: 
            print(f'OM SRI RAM {TEST.live}')
            time.sleep(3)
            TEST.count=TEST.count+1
            if TEST.count >10:
                TEST.live=False

                
    def CLOSE1(self):
        print('called CLOSE')
        TEST.live=False
        return
                
    def run(self):
        try:
            TEST.EchoFunc()
        except:
            print("unable to statt thread..")
