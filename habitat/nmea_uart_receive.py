import serial

"""
with serial.Serial('COM22', 19200) as ser:
    s = ser.readline()
    print(s)
"""

ser = serial.Serial('COM22', 19200)

while 1:
    s = str(ser.readline())
    print(s)
    #print(s.split(','))

