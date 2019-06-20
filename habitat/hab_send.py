import serial

port_name = "/dev/ttyACM0"
ser_port = serial.Serial(port_name, 115200)
print(f"port opened: {ser_port.name}")


data = "<FROM=HAB#TO=AS#TEXT=TOMASZMIS#>.........................................................................................................................................................................................................................."

def send_serial(ser, data):
            ser.write(str.encode(data))
            print(str.encode(data), f"port: {ser}")
            #time.sleep(0.1)

send_serial(ser_port, data)
