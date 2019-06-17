#!/usr/bin/env python
import serial
import time

f = open("nmea_itc_3.txt")
ff = [line for line in f]
#print(ff)
ser = serial.Serial('COM22', 19200)
print(f"port opened: {ser.name}")

#while 1:
for line in ff:
    ser.write(str.encode(line))
    print(str.encode(line))
    #time.sleep(0.1)
    while ser.in_waiting:  # Or: while ser.inWaiting():
        print(ser.readline())



