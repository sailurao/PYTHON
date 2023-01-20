# -*- coding: utf-8 -*-
"""
Test.py - consists of all the tests
"""
import TS
import mbus
import time

class TestProc:
    def __init__(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb,bTest,TR
        self.test_seq=0xff
        self.test_tmp=0
        test_tmr=0 #increments every time run is called
        test_tmr_set=0 #set value
        TS1=TS.TEST_STAND()
        mb = mbus.MBUS()
        self.test_res=""
        test_sub=0
        self.ACK=0
        bTest=0
        
        self.results=[]
        TR=1#test result pass
        
        
    def TEST_PASS(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb,bTest,TR
        if(TR==0):
            self.TEST_FAIL()
            return
        self.test_seq=101 #TEST PASS
        test_tmr=0 #increments every time run is called
        test_tmr_set=0 #set value
        self.test_res="TEST PASS"
        test_sub=0
        self.ACK=0
        bTest=0
        TR=1#TEST PASSED
        return
        
    def TEST_FAIL(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb,bTest,TR
        self.test_seq=100 #TEST PASS
        test_tmr=0 #increments every time run is called
        test_tmr_set=0 #set value
        test_sub=0
        self.ACK=0
        bTest=0
        TR=0 #test result failed
        return
        
    def Failed(self,msg):
        global TR
        TR=0 #test result failed
        self.results.append(self.test_res+"-"+msg)
        return
    
    #get ready for LED TEST
    def LED_TEST_INIT(self): 
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        test_sub=0
        self.test_seq=4 #LED TEST
        mb.LED_ON(test_sub)
        self.ACK=0
        self.test_res="LED TEST"
        return
    

    def RTC_CHK_INIT(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        self.test_seq=1
        test_tmr_set=110 #100X10ms= 1.1sec delay
        test_sub=0
        self.test_res="RTC TEST"
        if mb.RTC_INIT()==0:
            self.Failed("MODBUS RTC WRITE FAILED")
            return 0
        else:
            test_tmr_set=110 #100X10ms= 1.1sec delay
            return 1

        
    def RLY_CHK_INIT(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        self.test_seq=3
        test_tmr_set=110 #100X10ms= 1.1sec delay
        test_sub=0
        self.test_res="RELAY TEST"
        if(mb.RELAY_ON(test_sub)==0):
                self.Failed("MODBUS RELAY WRITE FAILED")
                self.LED_TEST_INIT()
                return

    def RLY_CHK(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        if(TS1.DUT_RLY_MON(test_sub)): #relay test fail
                self.Failed(str(test_sub)+"FAILED")
                self.LED_TEST_INIT()
                return
        test_sub=test_sub+1
        if(test_sub < 4):
            test_tmr_set=110 #100X10ms= 1.1sec delay
            if(mb.RELAY_ON(test_sub)==0):
                self.Failed("MODBUS RELAY WRITE FAILED")
                self.LED_TEST_INIT()
                return
        else:
            self.results.append("RELAY TEST - PASSED")
            self.LED_TEST_INIT()
            return

    #CURRENT @ 24V DC
    def CURRENT_TEST(self):
        self.test_seq=5 #CURRENT TEST
        self.test_res="Current Test"
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        val = TS1.PAC1720.ReadCurrent(0)
        if(val < 55):
           self.Failed("24VDC CURRENT < 50mA")
           self.TEST_FAIL()

        elif(val > 85):
           self.Failed("24VDC CURRENT > 85mA")
           self.TEST_FAIL()
        else:
           self.results.append("CURRENT TEST - PASSED %dmA" % (val))
           #TS1.DUT_PWR_JUMP_OFF()
           #TS1.DUT_ON(0)
           self.test_seq=6 #CURRENT TEST
           self.test_res="Battery Curent Test"
           test_tmr_set=200 #100X10ms= 2sec delay
        return

        

    #CURRENT @ 3.3V RTC BAT
    def BAT_CURRENT_TEST(self):
        self.test_seq=6 #CURRENT TEST
        self.test_res="Battery Curent Test"
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        val = TS1.PAC1720.ReadCurrent(1)
        if(val > 4):
           self.Failed("CURRENT > 4uA")
        else:
           self.results.append("BAT CURRENT TEST - PASSED %duA" % (val))
        self.SLEEP_TEST_INIT()
        return
    
      #delay 10ms X count
    def dly10(self,cnt):
        while(cnt):
            cnt =cnt-1
            start = time.time()
            while(1):
              stop =time.time()
              val = stop-start
              if val > 0.01:
                  return

    #SLEEP TEST INIT
    def SLEEP_TEST_INIT(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        self.test_seq=7 #CURRENT TEST
        self.test_res="Sleep Test1"
        if mb.FORCE_OFF()==0:
            self.Failed("MODBUS FORCE MODE WRITE FAILED")
        TS1.DUT_PWR_JUMP_OFF() # REMOVE JUMPER to disable FORCE POWER ON
        self.dly10(5) #50ms delay
        if(TS1.IS_DUT_VDD()==0):
            self.Failed("NO VDD DETECTED")
        self.test_tmp=0
        test_tmr_set=100 # #100X10ms= 1.1sec delay
        return        

        
    #SLEEP TEST 
    def SLEEP_TEST(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        self.test_seq=7 #CURRENT TEST
        self.test_res="Sleep Test2 -" + str(self.test_tmp)
        self.test_tmp=self.test_tmp+1
        test_tmr_set=100
        if(TS1.IS_DUT_VDD()==0):
           self.results.append("SLEEP TEST - PASSED %d" % (self.test_tmp))
           self.TEST_PASS()
        else:
           # return
            self.Failed("Failed, VDD ACTIVE")
            self.TEST_FAIL()
            #self.test_seq=8 #CURRENT TEST
        return        

        



    def LED_CHK(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        
        if(self.ACK==0): #LED TEST NO self.ACK YET
           return
        elif(self.ACK==2): #LED TEST FAILED
            self.Failed(str(test_sub)+"FAILED")
            self.CURRENT_TEST() #TEST_FAIL()
            return
        elif(self.ACK==1): #LED TEST PASSED
            test_sub=test_sub+1
            if(test_sub < 4):
                test_tmr_set=110 #100X10ms= 1.1sec delay
                mb.LED_ON(test_sub)
                self.ACK=0
                return
            else:
                self.results.append("LED TEST - PASSED")
                self.CURRENT_TEST() #TEST_PASS()
                return
            
            
            

    #useful to see if RUN process is running or not
    def GetTmrValstr(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb 
        my_s = str(test_tmr)
        my_s1 = str(test_tmr_set)
        my_s2 = "TMR:"+my_s+","+my_s1
        return my_s2
    
    #useful to initalise timers
    def NewTest(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb,TR
        test_tmr = 0
        test_tmr_set = 10
        self.results=[]
        TR=1#test result pass
        TS1.DUT_PWR_JUMP_OFF()
        TS1.DUT_ON(0)
        TS1.BAT_ON(0)
        self.test_res=""
        return
    
    
    #useful to initalise timers
    def TmrInit(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb,TR
        test_tmr = 0
        test_tmr_set = 10
        self.results=[]
        TR=1#test result pass

    def GetLedNum(self):
        msg="LED"+str(test_sub+1)
        return msg
   
#RUNS periodically from GUI                  
    def Run(self):
        global test_tmr,test_tmr_set,TS1,test_sub,mb,bTest,TR
        bTest = bTest ^ 0x01
        '''
        if(bTest):
          TS1.DUT_HIGH()
        else:
          TS1.DUT_LOW()  
        '''
        
        if(self.test_seq==0xff): #INVALID state?
            return
        test_tmr = test_tmr+1
        if(test_tmr < test_tmr_set):
            return
        test_tmr=0
        if self.test_seq==0:
            TS1.DUT_PWR_JUMP_ON()
            TS1.DUT_ON(1)
            TS1.BAT_ON(1)
            self.test_seq=1
            test_tmr_set=500 #100X10ms= 2sec delay
            return
        
        if self.test_seq==1: #VDD TEST, MODBUS WRITE
            self.test_res="VDD TEST"
            if(TS1.IS_DUT_VDD()==0):
                self.Failed("NO VDD DETECTED")
            else:
                self.results.append(self.test_res+"-PASSED")

            if(mb.LOCATE_DUT()==0):
                self.Failed("LANTRONIX MODULE NOT FOUND")

            if mb.FORCE_ON()==0:
                if mb.FORCE_ON()==0:
                    self.Failed("MODBUS FORCE MODE WRITE FAILED")
                
            self.test_res="RTC TEST"    
            if mb.RTC_INIT()==0:
                self.Failed("MODBUS RTC WRITE FAILED")
                self.RLY_CHK_INIT()
                return
            else:
                self.test_seq=2
                test_tmr_set=110 #100X10ms= 1.1sec delay
                return
            
        if self.test_seq==2:  #RTC
            test_sub=0
            if mb.RTC_TEST()==0:
                self.Failed("MODBUS RTC TEST FAILED")
            else:
                self.results.append(self.test_res+"-PASSED")
            self.RLY_CHK_INIT()
            return
        
        if self.test_seq==3: #RLY CHECK
            self.RLY_CHK()
            return
        
        if self.test_seq==4: #LED TEST
            self.LED_CHK()
            return
        if self.test_seq==5: #CURRENT TEST
            self.CURRENT_TEST()
            return
        if self.test_seq==6: #BAT CURRENT TEST
            self.BAT_CURRENT_TEST()
            return
        
        if self.test_seq==7: #SLEEP TEST
            self.SLEEP_TEST()
            return
        
        
        
        
                     
            
            
            

