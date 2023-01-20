# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:42:09 2022
this software runs on the Raspberry PI ,
sends the announce message and reads the MAC ID and IP address from LANTRONIX MODULE.

@author: namam
"""
#https://pymotw.com/2/socket/multicast.html

import socket
import sys
import time

class announce:
    
    bLANT_FOUND=0 # initialize lantronix found variable
                
    #**********************************************************
    #STARTS AOUNCE PROTOCOL and returns MAC ID followed by IP ADDRESS
    def start(self):
        #msg = 'Discovery: Who is out there?'
        #my_msg = msg.encode()+bytes([0x00,0x0a])
        my_msg = bytes([0x01,0x01,0x00,0x00,0x00,0xff,0x00,0x00])
        my_msg1 = bytes([0x00,0x01,0x00,0xf6])
        main_cont = True
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
#        allips = [ip[-1][0] for ip in interfaces]
#        for ip in allips:
#        if main_cont==False:
#           break
        #ip="192.168.0.186"  #NAGA DESKTOP
        #ip="192.168.0.224"  #PI WIFI
        ip="192.168.0.248"  #AGV TESTSTAND
        
#        hostname = socket.gethostname()
 #       IPAddr = socket.gethostbyname(hostname)
 
#        print("Your Computer Name is:" + hostname)
#        print("Your Computer IP Address is:" + IPAddr)        
        
        
        #print(f'sending on {ip}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)# UDP
        sock.settimeout(5)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip,43282))
            sock.sendto(my_msg, ("192.168.0.255",43282))
            sock.sendto(my_msg, ("192.168.0.255",43282))
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)# UDP
            sock.settimeout(5)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip,28673))
            sock.sendto(my_msg1, ("192.168.0.255",30718))
            while True:
                #print(sys.stderr, 'waiting to receive')
                try:
                    data, server = sock.recvfrom(100)
                    self.server = server[0]
                    self.bLANT_FOUND=1
                    break
                    
                except socket.timeout:
                    #print(sys.stderr, 'timed out, no more responses')
                    self.server=0
                    self.bLANT_FOUND=0
                    break
            
        finally:
            sock.close()
        
    
    
    
    
    
    
    