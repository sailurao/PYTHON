# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:42:09 2022
this software runs on the Raspberry PI unit of the CRYO FREEZER TESTSTAND2,
sends the announce message and reads the MAC ID and IP address.

@author: namam
"""
#https://pymotw.com/2/socket/multicast.html

import socket
import sys
import time

class announce:
    mac_str="ff-ff-ff-ff-ff-ff"
    mac_byte=bytes([0xff,0xff,0xff,0xff,0xff,0xff]) #default mac byte
    ip_byte=bytes([0x00,0x00,0x00,0x00])
    ip_str="0.0.0.0"
    
    temp = int(ip_byte[0])
    mac_str = '%s+%d' % (mac_str,ip_byte[0])
    
    #skips 0d 0a of the given byte array and returns the index
    #returns 0xff if 0d 0a is not found
    def skip0d0a(arr,n):
        z=len(arr)
        for i in range(n,z):
            if i >=(z-2):
                return 0xff  #not found 0d,0a
            if arr[i]==0x0d:
                if arr[i+1]==0x0a:
                    return i+2
        return 0xff # this will not occur
        
                
    #**********************************************************
    #This function extracts the IP and MAC info from the given byte array
    def ExtractIpMac(arr):
        if len(arr)<16:  # not enough char
            return 0x00
        if arr[0]!=0x02: #1st byte type is MAC ADDRESS
            return 0x00 #not found
        mac_byte=bytearray()
        
        for x in range(1,7):
            mac_byte.append(arr[x])
            temp=hex(arr[x])
            if x==1:
                mac_str = '%02X' % (arr[x])
            else:
                mac_str = '%s-%02X' % (mac_str,arr[x])
            
        i=announce.skip0d0a(arr,9) #skip 0d,0a
        if i==0xff:
            return 0x00;
        i=announce.skip0d0a(arr,i) #skip 0d,0a
        if i==0xff:
            return 0x00;
    
        if arr[i] != 0x05: #IP address Type
            return 0x00     
        
        ip_byte=bytearray()
        y=i+1;
        for x in range(y,y+4):
            temp=int(arr[x])
            ip_byte.append(arr[x])
            if x==y:
                ip_str='%d' % (temp)
            else:
                ip_str='%s.%d' % (ip_str,temp)
                
        print("MAC BYTE: ",mac_byte) 
        print("MAC STR: ",mac_str)
        print("IP BYTE: ",ip_byte) 
        print("IP STR: ",ip_str) 
    
        announce.mac_str=mac_str;
        announce.ip_str=ip_str;
    
        return 0x01
    #**********************************************************
    #STARTS AOUNCE PROTOCOL and returns MAC ID followed by IP ADDRESS
    def start(self):
        msg = 'Discovery: Who is out there?'
        my_msg = msg.encode()+bytes([0x00,0x0a])
        main_cont = True
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        allips = [ip[-1][0] for ip in interfaces]
#        while main_cont:
        for ip in allips:
            if main_cont==False:
               break
            print(f'sending on {ip}')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)# UDP
            sock.settimeout(5)
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.bind((ip,30303))
                sock.sendto(my_msg, ("255.255.255.255",30303))
                while True:
                    print(sys.stderr, 'waiting to receive')
                    try:
                        data, server = sock.recvfrom(100)
                    except socket.timeout:
                        print(sys.stderr, 'timed out, no more responses')
                        break
                    else:
                        print(sys.stderr, 'received "%s" from %s' % (data, server))
                        if announce.ExtractIpMac(data)==0x01 :
                            main_cont=False
                            break
                
            finally:
                sock.close()
        return announce.mac_str,announce.ip_str
#            time.sleep(5) 
        
    
    
    
    
    
    
    