#import threading
#import ex2
import anounce
import time
import ping
import Barcoder
import test
"""

"This would create first object of Employee class"
emp1 = ex2.Employee("Zara", 2000)
"This would create second object of Employee class"
emp2 = ex2.Employee("Manni", 5000)
emp1.displayEmployee()
emp2.displayEmployee()
print ("Total Employee %d" % ex2.Employee.empCount)
"""


"""
#anounce class testing
announce=anounce.announce()
my_list = announce.start()

print('mac_id: ', my_list[0])
print('IP: ', my_list[1])

"""


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

"""
#IP2MAC class testing
mac = ping.GetMac("192.168.0.235")
mac_str=mac.decode('utf-8')
print(f"MAC: {mac_str.upper()}")
"""

"""
#checking USB-TTL P12303 
print("opening USB_TTL ......")
thread1 = ser1.UartTtl()
thread1.run()
time.sleep(5)
print("closing USB_TTL ......")
ser1.UartTtl.live=False
time.sleep(5)
print("closed USB_TTL ......")
"""


#checking Barcode Reader
thread2 = test.TEST()
thread1 = Barcoder.BR()
thread2.start()
thread1.start()

while(thread2.live):
    x=1
    flag,kkey=thread1.get_br_code()
    if flag==True:
       print("KEY: "+kkey) 

    
print("Closed Thread2")
thread1.CLOSE1()

thread1.join()
thread2.join()


