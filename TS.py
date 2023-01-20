# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 14:09:30 2023

TS.py
TEST_STAND driver functions

@author: namam
"""
import RPi.GPIO as GPIO# Import Raspberry Pi GPIO library
import PAC1720




class TEST_STAND:
   def __init__(self):
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) # opto3 sim
        GPIO.setup(13, GPIO.IN) # START_TEST
        GPIO.setup(15, GPIO.IN) # DUT_PROGRAM
        GPIO.setup(33, GPIO.OUT, initial=GPIO.LOW) # OPTO2 sim
        GPIO.setup(35, GPIO.OUT, initial=GPIO.LOW) # DUT_ON
        GPIO.setup(37, GPIO.IN) # RELAY1
        GPIO.setup(40, GPIO.IN) # RELAY4
        GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW) # BAT_ON
        GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW) # opto1 sim
        GPIO.setup(22, GPIO.IN) # RELAY2
        GPIO.setup(18, GPIO.IN) # RELAY3
        GPIO.setup(16, GPIO.IN) # RELAY4
        GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) # opto3 sim
        GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW) # opto4 sim
        self.PAC1720=PAC1720.PPAC1720()
       
       
       
       
   def DUT_HIGH(self):
        GPIO.output(11, GPIO.HIGH) # Turn on# DUT_PWR_JUMPER
        
   def DUT_LOW(self):
        GPIO.output(11, GPIO.LOW) # Turn on# DUT_PWR_JUMPER

   def DUT_PWR_JUMP_ON(self):
        GPIO.output(11, GPIO.HIGH) # Turn on# DUT_PWR_JUMPER

   def DUT_PWR_JUMP_OFF(self):
       GPIO.output(11, GPIO.LOW) # Turn off # DUT_PWR_JUMPER
        
    
   def IS_PROGRAM(self):
       if GPIO.input(15):
           return 0x01 # Program mode
       else:
           return 0x00 #  RUN Mode

   #simulates OPTO signal to DUT
   def DUT_OPTO_SIM(self,indx,val):
       if indx >3:
           return
       #OPTO ON
       if(val==1):
            if indx==0:
               GPIO.output(32, GPIO.HIGH) # Turn on# DUT_PWR_JUMPER 
            elif indx==1:
               GPIO.output(33, GPIO.HIGH) # Turn on# DUT_PWR_JUMPER 
            elif indx==2:
               GPIO.output(8, GPIO.HIGH) # Turn on# DUT_PWR_JUMPER 
            elif indx==1:
               GPIO.output(10, GPIO.HIGH) # Turn on# DUT_PWR_JUMPER 
       else:
            if indx==0:
               GPIO.output(32, GPIO.LOW) # Turn on# DUT_PWR_JUMPER 
            elif indx==1:
               GPIO.output(33, GPIO.LOW) # Turn on# DUT_PWR_JUMPER 
            elif indx==2:
               GPIO.output(8, GPIO.LOW) # Turn on# DUT_PWR_JUMPER 
            elif indx==1:
               GPIO.output(10, GPIO.LOW) # Turn on# DUT_PWR_JUMPER 
               
               
   #DUT RELAY SIGNAL MONITOR
   def DUT_RLY_MON(self,indx):
         if(indx==0):
            return GPIO.input(37)               
         elif(indx==1):
            return GPIO.input(22)               
         elif(indx==2):
            return GPIO.input(18)               
         else:            
            return GPIO.input(16)
        
   def DUT_ON(self,val):
       if(val==1):
           GPIO.output(35, GPIO.HIGH) # Turn on# DUT_ON
       else:
           GPIO.output(35, GPIO.LOW) # Turn on# DUT_OFF
           
   def BAT_ON(self,val):
       if(val==1):
           GPIO.output(36, GPIO.HIGH) # Turn on# DUT_ON
       else:
           GPIO.output(36, GPIO.LOW) # Turn on# DUT_OFF
           
   def IS_DUT_VDD(self):
       if(GPIO.input(40)):
           return 1
       else:
           return 0