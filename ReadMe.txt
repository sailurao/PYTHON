AGV TESTSTAND
-------------
Files are located on the PI board "/home/pi/AGV1/TST"

FILE SYSTEM
------------
gui1.py is the main file


IP ADDRESS:
------------
MAKE SURE PI BOARD IS ASSIGNED WITH 192.168.0.248 as ANNOUNCE.py set for this IP ADDRESS





AGV AUTOSTART
---------------
1. open the file "/home/pi/.config/autostart/AGV.desktop" with

[Desktop Entry]
Type=Application
Name=AGV_TESTSTAND
Exec=/usr/bin/python3 /home/pi/AGV1/TST/gui1.py



