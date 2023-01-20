# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 17:52:30 2023

mbus.py
  responsible to send all Modbus commands
  #https://pypi.org/project/pyModbusTCP/


@author: User1
"""
from pyModbusTCP.client import ModbusClient
import anounce

class MBUS:
    def __init__(self):
      # global status,HOST
       self.status=0 #0-good
       self.HOST="192.168.0.207"
       self.announce=anounce.announce()


    def RTC_INIT(self):
      # global status,HOST
       c = ModbusClient(host=self.HOST, auto_open=True, auto_close=True)
       if c.write_single_register(2, 0x03)==0:  
           self.status=1 #Write fail
           return 0
       if c.write_single_register(1, 0x02)==0:  
           self.status=1 #Write fail
           return 0
       if c.write_single_register(0, 0x01)==0:  #SEC=0x01
           self.status=1 #Write fail
           return 0
       else:
           self.status=0
           return 1
       
    def RTC_TEST(self):
      # global status,HOST
       c = ModbusClient(host=self.HOST, auto_open=True, auto_close=True)
       hr = c.read_holding_registers(2, 1) 
       if(hr):
           self.status=0
       else:
           self.status=1 #read fail
           return 0
       c = ModbusClient(host=self.HOST, auto_open=True, auto_close=True)
       min1 = c.read_holding_registers(1, 1) 
       if(min1):
           self.status=0
       else:
           self.status=1 #read fail
           return 0
       c = ModbusClient(host=self.HOST, auto_open=True, auto_close=True)
       sec = c.read_holding_registers(0, 1) 
       if(sec):
           self.status=0
       else:
           self.status=1 #read fail
           return 0
       if(hr!=3):
           return 2 #RTC fail
       if(min1!=2):
           return 2 #RTC fail
       if(sec!=2):
           return 2 #RTC fail
       else:
           return 0 #RTC test pass
       



    #Locates the LANTRONIX MODULE by sending ANNOUNCE COMMAND
    def LOCATE_DUT(self):
        self.announce.start()
        if(self.announce.bLANT_FOUND):
            self.HOST=self.announce.server
            return 1
        else:
            self.HOST='0.0.0.0'
            #print(type(announce.server))
            #print(announce.server)        
            return 0


    def FORCE_ON(self):
      # global status,HOST
       if(self.announce.bLANT_FOUND==0):
           self.status=1 #Write fail
           return 0
      
       c = ModbusClient(host=self.HOST, auto_open=True, auto_close=True)
       if c.write_single_register(16, 0x01)==0:  
           self.status=1 #Write fail
           return 0
       else:
           self.status=0
           return 1
        
    def FORCE_OFF(self):
      # global status,HOST
       c = ModbusClient(host=self.HOST, auto_open=True, auto_close=True)
       if c.write_single_register(16, 0x00)==0:  
           self.status=1 #Write fail
           return 0
       else:
           self.status=0
           return 1
       
    
    def RELAY_ON(self,indx):
      # global status,HOST
       val=1;
       if indx > 3:
           return
       val = val << indx
       c = ModbusClient(host=self.HOST, auto_open=True, auto_close=True)
       if c.write_single_register(17,val)==0:  
           self.status=1 #Write fail
           return 0
       else:
           self.status=0
           return 1
       
    
    def LED_ON(self,indx):
      # global status,HOST
       val=1;
       if indx > 3:
           return
       val = val << indx+4
       c = ModbusClient(host=self.HOST, auto_open=True, auto_close=True)
       if c.write_single_register(17,val)==0:  
           self.status=1 #Write fail
           return 0
       else:
           self.status=0
           return 1
       
    def ReadInput(self):
      # global status,HOST
       c = ModbusClient(host=self.HOST, auto_open=True, auto_close=True)
       regs = c.read_holding_registers(0, 1) 
       if(regs):
           self.status=0
       else:
           self.status=1 #read fail
       return regs
        
    
        
        
        
        
        

