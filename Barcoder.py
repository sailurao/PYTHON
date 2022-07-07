
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
from evdev import InputDevice, categorize, ecodes

class BR(threading.Thread):
    ser=0
    live=False
    count=0
    key_val=""
    br_rdy=False
    BarS=""
    BarS1=""


    
    def __init__(self):
        threading.Thread.__init__(self)
        BR.count=0
        return


#Process Barcode idividual keys
    def MyFunc(str):
      if "SHIFT" in str:
            return False
    
      if "KEY_A" in str:
            return  False
    
      if "KEY_ENTER), up" in str:
        BR.BarS1=BR.BarS
        BR.BarS=""
        return True
    
      if "down" in str:
          if "KEY_" in str:
              sstr=str.partition("KEY_")
              z=sstr[2][0]
              BR.BarS=BR.BarS + z
      return False

    
     
    def EchoFunc():
        BR.live=True
        device = InputDevice("/dev/input/event1") # my keyboard
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                val = categorize(event) 
                mystr = "%s" % val
                res = BR.MyFunc(mystr)
                if res == True:
#                	print(BR.BarS1)
                    BR.br_rdy=True
                    BR.key_val=BR.BarS1
            if BR.live==False:
                break
            
            
    def CLOSE1(self):
        print('called CLOSE')
        BR.live=False
        return
    
    
    def get_br_code(self):
        if BR.br_rdy==False:
             BR.br_rdy=False
             return False,""
        else:
             BR.br_rdy=False
             return True,BR.key_val
         
        
                
    def run(self):
        try:
            BR.EchoFunc()
        except:
            print("unable to statt thread..")
