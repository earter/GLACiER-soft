import serial
import threading

# sends only one line from habitat to astronaut

port_name = "/dev/ttyACM0"
ser_port = serial.Serial(port_name, 115200)
print(f"port opened: {ser_port.name}")

payload = "szwajcarskie"

frame = f"<FROM=HAB#TO=AS#TEXT={payload}#>"

for i in range(250-len(frame)):
    frame += "."

def send_serial(ser, data):
            ser.write(str.encode(data))
            print(str.encode(data), f"port: {ser}")
            #time.sleep(0.1)

send_serial(ser_port, frame)
