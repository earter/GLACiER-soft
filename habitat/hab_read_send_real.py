import serial
import threading

port_name = "/dev/ttyACM0"
ser_port = serial.Serial(port_name, 115200)
print(f"port opened: {ser_port.name}")

payload = "szwajcarskie chuje"

frame = f"<FROM=HAB#TO=AS#TEXT={payload}#>"

for i in range(250-len(frame)):
    frame += "."

def send_serial(ser, data):
            ser.write(str.encode(data))
            print(str.encode(data), f"port: {ser}")
            #time.sleep(0.1)

def read_serial(ser):
    while 1:
        #readData = ser.read(250).decode()
        readData = ser.readline().decode()
        print(f"read line: {readData}")


thread1 = threading.Thread(target=read_serial, args=(ser_port,))
thread1.start()

#thread2 = threading.Thread(target=send_serial, args=(ser_port,))
#thread2.start()
