# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 14:33:48 2022

@author: namam
"""
import i2c1

class PPAC1720:
    
    def __init__(self):
        global myI2C,ch1_val,ch2_val
        ch1_val=0x1234
        ch2_val=0x1234
        PAC1720_CHIP_ADDR = 0x9A  #based 100 OHM resistor selection between pins 6 & 5 
        #PAC1720_CHIP_ADDR = PAC1720_CHIP_ADDR >> 1 # #7 bit address (will be left shifted to add the read write bit)
        myI2C = i2c1.I2C1(PAC1720_CHIP_ADDR)

        ch1_val = myI2C.READ_BYTE(0x00) #CH1 Sense Sampling config
        ch1_val=0x00;
        myI2C.WRITE_BYTE(0x00,ch1_val)
        ch1_val = myI2C.READ_BYTE(0x00) #CH1 Sense Sampling config
        
        ch1_val = myI2C.READ_BYTE(0x0b) #CH1 Sense Sampling config
        ch1_val=0x53
        myI2C.WRITE_BYTE(0x0B,ch1_val)
        ch2_val = myI2C.READ_BYTE(0x0b) #CH1 Sense Sampling config
        ch1_val = myI2C.READ_BYTE(0x0C) #CH1 Sense Sampling config
        ch1_val=0x53
        myI2C.WRITE_BYTE(0x0C,ch1_val)
        ch2_val = myI2C.READ_BYTE(0x0C) #CH2 Sense Sampling config
        return
    
    def ReadCurrent(self,ch):
        global myI2C,ch1_val,ch1_val,ch2_val
        Pac1720_val =0x1234
        if ch == 0:
            myI2C.READ_BYTE(0x04) #read conversion done status
            while 1:
                ch2_s = myI2C.READ_BYTE(0x04) #read conversion done status
                if ch2_s & 0x80 != 0: #//wait until the next conversion
                    break
            Pac1720_val = myI2C.READ_BYTE(0x0D); #high byte of CH1 Sense voltage
            #print("1):"+hex(Pac1720_val))
            if ((Pac1720_val & 0x80)==0x80) : #{ //if MSB is set then it is 0mA Current
                return 0
            ch1_val = Pac1720_val & 0x7f
            ch1_val = ch1_val << 4
            #print("2):"+hex(ch1_val))
                
            Pac1720_val = myI2C.READ_BYTE(0x0E) #//low byte of CH1 Sense voltage
            #print("3):"+hex(Pac1720_val))
            Pac1720_val = Pac1720_val >> 4
            ch1_val = ch1_val | Pac1720_val
            #print("4):"+hex(ch1_val))
            temp_f = 39.0 #CH1_CUR_PER_LSB;
            temp_f = (float)(ch1_val) * temp_f
            #Sub_mA = temp_f
            temp_f = temp_f/1000 #mA value , as resistor is 1 OHM
            return temp_f
        
        else:
            myI2C.READ_BYTE(0x04) #read conversion done status
            while 1:
                ch2_s = myI2C.READ_BYTE(0x04) #read conversion done status
                if ch2_s & 0x80 != 0: #//wait until the next conversion
                    break
            Pac1720_val = myI2C.READ_BYTE(0x0F); #high byte of CH1 Sense voltage
            if ((Pac1720_val & 0x80)==0x80) : #{ //if MSB is set then it is 0mA Current
                #Sub_mA = 0
                #Ch1CurVal = 0
                return 0
            ch1_val = Pac1720_val & 0x7f
            ch1_val = ch1_val << 4
                
            Pac1720_val = myI2C.READ_BYTE(0x10) #//low byte of CH1 Sense voltage
            Pac1720_val = Pac1720_val >> 4
            ch1_val = ch1_val | Pac1720_val
            temp_f = 39.0 #CH1_CUR_PER_LSB;
            temp_f = (float)(ch1_val) * temp_f
            #Sub_mA = temp_f
            temp_f = temp_f/1000 #mA value , as resistor is 1 OHM
            return temp_f
            