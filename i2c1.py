# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 16:50:09 2023

@author: namam
"""
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time


class I2C1:
    def __init__(self,addr):
        global DEVICE_ADDR        
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(29, GPIO.OUT, initial=GPIO.HIGH) # Set pin 29 to be an output pin and set initial value to low (off)
        GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH) # Set pin 31 to be an output pin and set initial value to low (off)
        DEVICE_ADDR = addr

    def NOP10(self):
        j=10
        for i in range(0,10):
            j = j+1
   
    #delay 10ms
    def dly10(self):
       start = time.time()
       while(1):
         stop =time.time()
         val = stop-start
         if val > 0.01:
             return


    def scl(self, val):
        if val !=0 :
           GPIO.output(29, GPIO.HIGH) # Turn on
        else:
            GPIO.output(29, GPIO.LOW) # Turn off
        self.NOP10()
        

    def sda(self, val):
        if val !=0 :
           GPIO.output(31, GPIO.HIGH) # Turn on
        else:
            GPIO.output(31, GPIO.LOW) # Turn off
        self.NOP10()
        

    def SendBit(self, val):
         self.sda(val)
         self.scl(1)
         self.scl(0)
         
         
    def starti2c(self):
         GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH) # Set pin 31 to be an output pin and set initial value to low (off)
         self.sda(1)
         self.scl(1)
         self.sda(0)
         self.scl(0)
         
         
    def stopi2c(self):
         GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH) # Set pin 31 to be an output pin and set initial value to low (off)
         self.scl(0)
         self.sda(0)
         self.scl(1)
         self.sda(1)
         
    def txi2c(self, val):
        GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH) # Set pin 31 to be an output pin and set initial value to low (off)
        a=0x80
        for i in range(8):
            if(a & val):
                self.SendBit(1)
            else:
                self.SendBit(0)
            a = a >> 1
        self.sda(0)
        GPIO.setup(31, GPIO.IN) 
        #self.NOP10()
        self.scl(1)
        if GPIO.input(31)==0:
            bb0=1
        else:
            bb0=0;
        self.scl(0)
        
        
        if bb0==1:
          return 1
        else:
          return 0
         
     
    def rxi2ct(self):
        GPIO.setup(31, GPIO.IN) 
        self.NOP10()
        dpl=0x12
        dpl=0
        for i in range(8):
           self.scl(1)
           dpl = dpl << 1
           if GPIO.input(31):
               dpl = dpl | 0x01
           self.scl(0)
        return dpl


    def ACK(self):
        GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH) # Set pin 31 to be an output pin and set initial value to low (off)
        self.sda(0)
        self.scl(1)
        self.scl(0)
        

    def NACK(self):
        GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH) # Set pin 31 to be an output pin and set initial value to low (off)
        self.sda(1)
        self.scl(1)
        self.scl(0)
        


    def WRITE_BYTE(self, addr,data1):
        global DEVICE_ADDR  
        GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH) # Set pin 31 to be an output pin and set initial value to low (off)
        #self.stopi2c()  
        count=10
        while(count != 0):
            self.starti2c()
            if(self.txi2c(DEVICE_ADDR)):
                break;
            self.stopi2c()
            self.dly10() #10ms delay
            count = count-1
        if(count==0):
           return
        self.txi2c(addr)
        self.txi2c(data1)
        self.stopi2c()
        

    def WRITE_BYTES(self, addr, values):
        global DEVICE_ADDR  
        GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH) # Set pin 31 to be an output pin and set initial value to low (off)
        #self.stopi2c()  
        count=10
        while(count != 0):
            self.starti2c()
            if(self.txi2c(DEVICE_ADDR)):
                break;
            self.stopi2c()
            self.dly10() #10ms delay
            count = count-1
        if(count==0):
           return
        self.txi2c(addr)
        for i in values:
            self.txi2c(i)
        self.stopi2c()
        

    def READ_BYTE(self,addr):
        global DEVICE_ADDR  
        val = 0x12
        GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH) # Set pin 31 to be an output pin and set initial value to low (off)
#        self.stopi2c()  
        #1st loop to write Address succesfully
        while(1):
            count=10
            while(count != 0):
                self.starti2c()
                if(self.txi2c(DEVICE_ADDR)):
                    break;
                self.dly10() #10ms delay
                self.stopi2c()
                count = count-1
            if(count==0):
               return
            if(self.txi2c(addr)):
                break
            else:
                self.dly10() #10ms delay
                self.stopi2c()
            
        #2nd loop to read data properly
        count=10
        while(count != 0):
            self.starti2c()
            if(self.txi2c(DEVICE_ADDR+1)):
                break;
            self.dly10() #10ms delay
            self.stopi2c()

        val = self.rxi2ct()
        self.stopi2c()
        #print("RD"+hex(val))
        return val
        