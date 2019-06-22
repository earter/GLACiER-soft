#!/usr/bin/env python

import serial
import threading
import time

# test with arduino with "receive_send_to_pc.ino"

f = open("test_data/nmea_itc_3.txt")
ff = [line for line in f]

port_name = "/dev/ttyUSB0"
ser_port = serial.Serial(port_name, 19200)
print(f"port opened: {ser_port.name}")


def nmea2deg(raw):
    def degmin(val):  # splits deg&mins in NMEA data
        valt = val.split('.')
        threshold = 3 if len(valt[0]) == 5 else 2
        return (float(val[0:threshold]), float(val[threshold:]))
    raw = raw[5:27]
    raw = raw.split(',')
    lat = degmin(raw[0])
    lon = degmin(raw[1])
    latdeg = lat[0] + lat[1] / 60.0  # *(-1) for W and S
    londeg = lon[0] + lon[1] / 60.0  # *(-1) for W and S
    return (latdeg, londeg)


def handle_data(data):
    print(data)
    #print(f"raw data: {data}")
    position_deg = nmea2deg(data)
    #print(position_deg[0], position_deg[1])
    #print(f"total degrees data: {position_deg}")


def read_serial(ser):
    while 1:
        readData = ser.readline().decode()
        handle_data(readData)


def send_serial(ser):
    while 1:
        for line in ff:
            ser.write(str.encode(line))
            #print(str.encode(line))
            #time.sleep(0.1)


thread1 = threading.Thread(target=read_serial, args=(ser_port,))
thread1.start()

thread2 = threading.Thread(target=send_serial, args=(ser_port,))
thread2.start()
