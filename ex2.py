# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:33:56 2023
ex2.py - to test VDD
@author: namam
"""
import TS
import RPi.GPIO as GPIO# Import Raspberry Pi GPIO library


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(40, GPIO.IN) # VDD
print(GPIO.input(40))

"""
def IS_DUT_VDD():
    if(GPIO.input(40)):
        return 1
    else:
        return 0

if(IS_DUT_VDD()==1):
  print("HIGH")
elif (IS_DUT_VDD()==0):
    print("LOW")
else:
    print("unknown")
    """