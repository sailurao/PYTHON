# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 16:55:19 2023
https://www.instructables.com/Get-Started-With-Raspberry-PI-GUI/#:~:text=A%20powerful%20library%20for%20developing%20graphic%20user%20interface,and%20plenty%20of%20resources%20exist%20on%20the%20internet.
@author: namam
"""

#!/usr/bin/python3
from tkinter import *                 # imports the Tkinter lib
from tkinter import messagebox
import test 
import time


"""RPI
RPI import RPi.GPIO as GPIO               # imports the GPIO lib
import time                           # import time lib
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)               # disable warnings
GPIO.setup(18, GPIO.OUT)              # ServoMotor connected to GPIO 18
GPIO.setup(23,GPIO.OUT)		  	          # LED connected to GPIO 23
pwm = GPIO.PWM(18, 100)               # setup GPIO 18 as PWM and provide starting value (0-100)
pwm.start(5)
RPI"""
my_val=1
my_cnt=1
test_seq=0xff
bTest=0
TST = test.TestProc()
root = Tk()				     # create the root object
root.wm_title("AGV TEST STAND SOFTWARE REV-1.0")			             # sets title of the window
#root.configure(bg="#99B898")		       # change the background color 
root.configure(bg="white")		       # change the background color 

#root.attributes("-fullscreen", True) # set to fullscreen by default
root.geometry("800x500")       		# specify the window dimension 300X300 pixels


# create listbox object
listbox = Listbox(root, height = 10,
                  width = 40,
                  bg = "white",
                  activestyle = 'dotbox',
                  font = "Helvetica",
                  fg = "blue")

# Define a header label for the list. 
hlbl1 = Label(root, text = " AGV TESTS",font="Arial 30 bold ", fg= "blue",bg="white")




# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)

def btnClicked():
    global my_val,my_status,bTest,slabel,ledButton,TST,test_seq
    bTest=bTest^0x01
    if(bTest):
        test_seq=0
        slabel.config(text="Test in process ...") #Test started
        #my_status.set("Test in process ...") #Test started
        ledButton.config(text="STOP ")
        TST.test_seq=0x00 #
        TST.NewTest()
        root.after(10,TEST_MON)
    else:
        ledButton.config(text="START")
        #TST.Run() #  testing
        slabel.config(text="Test stopped ..."+str(TST.test_seq)+","+TST.test_res) #Test stopped
        root.wm_title("AGV - "+TST.GetTmrValstr())	    
        TST.test_seq=0xff
        #my_status.set("Test stopped") #Test stopped        
        
def TEST_MON():
    global TST,my_cnt,bTest,test_seq
    
    if(bTest==0):
        ledButton.config(text="START")
        return
    my_cnt=my_cnt+1
    root.wm_title("AGV TEST STAND - "+str(my_cnt/100))	    
    TST.Run()
    if(TST.test_seq==100): #Test FAIL
        slabel.config(text="Test Failed @ "+str(TST.test_seq)+","+TST.test_res) #Test stopped
        bTest=0
    elif(TST.test_seq==101): #Test PASS
        slabel.config(text="Test Passed ") #Test stopped
        bTest=0
    else:
        slabel.config(text="Test in process ..."+str(TST.test_seq)+","+TST.test_res) #Test stopped
    if(TST.test_seq != 0) and (test_seq != TST.test_seq):
        test_seq=TST.test_seq
        listbox.delete(0,END)
        n=1
        listbox.insert(n,"")
        n=2
        for x in TST.results:
           listbox.insert(n,x) 
           n=n+1
    if(TST.test_seq==4): #LED TEST
        if(TST.ACK==0): #and waiting for USER ACK?
            question = "Is "+TST.GetLedNum()+" On?"
            result=messagebox.askquestion("LED TEST",question)
            if(result=='yes'):
                TST.ACK=1 # TEST PASS
            else:
                TST.ACK=2 # TEST FAIL
    root.after(10,TEST_MON)
    return
    
        
#    my_val = my_val +1
#    my_status.set(str(my_val))

def btnExit():
  	root.destroy()

"""RPI
def update(angle):
        duty = float(angle) / 10.0 +2.5
        pwm.ChangeDutyCycle(duty)
RPI"""       

label_1 = Label(root, text="OM SRI RAM", font="Verdana 26 bold",
			fg="#000",
			bg="white",
			pady = 30,
			padx = 50)
exitButton = Button(root, text="Exit", background = "gray",
      command=btnExit, height=5, width=20, font = "Arial 16 bold", activebackground = "brown")
	


ledButton = Button(root, text="START TEST",background = "gray", 
      command=btnClicked, height=5, width=20, font = "Arial 16 bold", activebackground ="brown")

my_status = StringVar()
my_status.set(str(my_val))

#status label
#slabel = Label(root,textvariable=my_status)
slabel= Label(root, text= "", font=("Helvetica",20), fg= "blue", bg='white')
slabel.config(text="                                                                ") #Test stopped

"""        
ServoC= Scale(root, from_=0, to=180,
     orient=HORIZONTAL, command=update, background = "#C06C84",
     width =80, label = "ServoMotorAngleController",length = 500,  activebackground = "#C06C84",font = "Arial 16 bold")
"""
#label_1.grid(row=0, column=0)
hlbl1.grid(row=0,column=0)
#exitButton.grid(row = 4 ,column = 1)
ledButton.grid(row = 1 ,column = 1)
listbox.grid(row = 1 ,column = 0)
slabel.grid(row=5,column=0)
#slabel.pack(pady= 10)

#ServoC.grid(row=2 , column = 1)
root.after(10,TEST_MON)
root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
