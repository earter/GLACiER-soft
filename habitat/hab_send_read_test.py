import serial
import threading
import time
import datetime

# test with an uart-usb converter with rx tx pins connected

port_name = f"/dev/ttyUSB0"
ser_port = serial.Serial(port_name, 115200)
print(f"port opened: {ser_port.name}")

keys_all = ['FROM', 'TO', 'TEXT', 'GPS', 'DWM']
values_init = ['GS', 'HAB', 'INIT TEXT', '0000.00000,00000.00000', '0,0,0']
dict_out_values = {}
dict_out_time = {}
for i in range(len(keys_all)):
    dict_out_values[keys_all[i]] = values_init[i]
    dict_out_time[keys_all[i]] = 0


f = open("test_data/hab_test1.txt")
ff = [line for line in f]

#frame = "<FROM=GS#TO=HAB#TEXT=TOMASZMIS#GPS=\"5213.19563,02100.57196\"#DWM=3482342874,234234234,12434234#CNT=20#RSSI=-20#>"

def add_dots(frame):        #TODO oneliner
    frame = frame.rstrip()
    for i in range(250-len(frame)):
        frame += "."
    frame = frame + "\n"
    return frame

def extract(data):
    #print(f"read raw data: {data}")
    data = (data.split('<')[1].split('>')[0])
    #print(data)
    #print(f"raw1 data: {data}")
    split_data = data.split("#")
    split_data.remove('')
    split1 = [item.split("=") for item in split_data]
    dict_in = {}
    for val in range(len(split1)):
        dict_in[split1[val][0]] = split1[val][1]
    #print(dict_in)

    return dict_in


def update_data(dict_in):

    def update_dict_out(key):
        dict_out_values[key] = dict_in[key]
        dict_out_time[key] = datetime.datetime.now().strftime('%H:%M:%S')

    def fro():
        update_dict_out('FROM')
    def to():
        update_dict_out('TO')
    def text():
        update_dict_out('TEXT')
    def gps():
        update_dict_out('GPS')
    def dwm():
        update_dict_out('DWM')

    options = {'FROM': fro,
                'TO' : to,
                'TEXT' : text,
                'GPS' : gps,
               'DWM' :dwm}

    for key in dict_in:
        options[key]()

    #print(dict_out_values)
    return (dict_out_values, dict_out_time)

def visualise_data(dict_val, dict_time):
    print(f"{dict_val['FROM']}->{dict_val['TO']}\tmessage: {dict_val['TEXT']}\t messagelastupdate: {dict_time['TEXT']}")

def handle_data(data):
    data = extract(data) # get dict_in
    (dv, dt) = update_data(data)   # get dict out: values and time (last update)
    visualise_data(dv, dt)

def read_serial(ser):
    while 1:
        readData = ser.readline().decode()
        print(f"read line: {readData}")
        handle_data(readData)


def send_serial(ser):
    while 1:
        for line in ff:     # TODO expand file?
            line = add_dots(line)
            #print(f"dotted line: {line}")
            ser.write(str.encode(line))
            #print(f"sent line:{str.encode(line)}")
            time.sleep(1)

thread1 = threading.Thread(target=send_serial, args=(ser_port,))
thread1.start()

thread2 = threading.Thread(target=read_serial, args=(ser_port,))
thread2.start()
