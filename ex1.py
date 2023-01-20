#import threading
#import ex2
import anounce
#import ser2
import time

"""

"This would create first object of Employee class"
emp1 = ex2.Employee("Zara", 2000)
"This would create second object of Employee class"
emp2 = ex2.Employee("Manni", 5000)
emp1.displayEmployee()
emp2.displayEmployee()
print ("Total Employee %d" % ex2.Employee.empCount)
"""
announce=anounce.announce()
announce.start()
if(announce.bLANT_FOUND):
    #print(type(announce.server))
    print(announce.server)
else:
    print("No response from LANTRONIX module")    

"""
print("opening USB_UART ......")
thread1 = ser2.UsbUart()
thread1.run()
time.sleep(5)
print("closing USB_UART ......")
ser2.UsbUart.live=False
time.sleep(5)
print("closed USB_UART ......")
"""
