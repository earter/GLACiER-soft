import matplotlib.pyplot as plt
import tkinter as tk
import time
import threading
import serial
import datetime

# in habitat. simulatenously reads data from GroundStation and sends to astronaut via GS

port_name = "/dev/ttyUSB0"
global ser_port
ser_port = serial.Serial(port_name, 115200)
print(f"port opened: {ser_port.name}")

# ----- added flag recognition -----

keys_all = ['FROM', 'TO', 'TEXT', 'GPS', 'DWM']
values_init = ['GS', 'HAB', 'INIT TEXT', '0000.00000,00000.00000', '0,0,0']
dict_out_values = {}
dict_out_time = {}
for i in range(len(keys_all)):
    dict_out_values[keys_all[i]] = values_init[i]
    dict_out_time[keys_all[i]] = 0


def add_dots(frame):        #TODO oneliner
    frame = frame.rstrip()
    for i in range(250-len(frame)):
        frame += "."
    return frame

def nmea2deg(raw):
    def degmin(val):    # splits deg&mins in NMEA data
        valt = val.split('.')
        threshold = 3 if len(valt[0]) == 5 else 2
        return (float(val[0:threshold]), float(val[threshold:]))

    raw = raw.split(',')
    lat = degmin(raw[0])
    lon = degmin(raw[1])
    latdeg = lat[0] + lat[1]/60.0  # *(-1) for W and S
    londeg = lon[0] + lon[1]/60.0  # *(-1) for W and S
    return (latdeg, londeg)

def weather(data):
    data = data.split(',')
    data = [item.split(':') for item in data]
    dict_w = {}
    for item in data:
        dict_w[item[0]] = float(item[1])
    return tuple(dict_w.values())


def extract(data):
    data = (data.split('<')[1].split('>')[0])
    split_data = data.split("#")
    split_data.remove('')
    split1 = [item.split("=") for item in split_data]
    dict_in = {}
    for val in range(len(split1)):
        dict_in[split1[val][0]] = split1[val][1]
    return dict_in


def update_data(dict_in):

    def update_dict_out(key):
        dict_out_values[key] = dict_in[key]
        dict_out_time[key] = datetime.datetime.now().strftime('%H:%M:%S')

    def fro():
        update_dict_out('FROM')
        from_txt.delete(1.0,tk.END)
        from_txt.insert(tk.END, dict_out_values['FROM'])
    def to():
        update_dict_out('TO')
        to_txt.delete(1.0,tk.END)
        to_txt.insert(tk.END, dict_out_values['TO'])
    def text():
        dict_in['TEXT'] = weather(dict_in['TEXT'])
        print(f"dictin we: {dict_in['TEXT']}")
        update_dict_out('TEXT')
        weather_list = ['wd', 'ws', 'wda', 'wsa', 'h', 't', 'r', 'p', 'b']
        """ TODO
        for i in range(0,len(weather_list)+1):
            val = f"{weather_list[i]}_txt"
            print(val, type(val))
            try:
                val.delete(1.0,tk.END)
                val.insert(tk.END, dict_out_values['TEXT'][i])
            except:
                print(f"assigning weather data {val} unsuccesful")
        """             
        wd_txt.delete(1.0,tk.END)
        wd_txt.insert(tk.END, dict_out_values['TEXT'][0])
        ws_txt.delete(1.0,tk.END)
        ws_txt.insert(tk.END, dict_out_values['TEXT'][1])
        wda_txt.delete(1.0,tk.END)
        wda_txt.insert(tk.END, dict_out_values['TEXT'][2])
        wsa_txt.delete(1.0,tk.END)
        wsa_txt.insert(tk.END, dict_out_values['TEXT'][3])
        h_txt.delete(1.0,tk.END)
        h_txt.insert(tk.END, dict_out_values['TEXT'][4])
        t_txt.delete(1.0,tk.END)
        t_txt.insert(tk.END, dict_out_values['TEXT'][5])
        p_txt.delete(1.0,tk.END)
        p_txt.insert(tk.END, dict_out_values['TEXT'][7])
        r_txt.delete(1.0,tk.END)
        r_txt.insert(tk.END, dict_out_values['TEXT'][6])
        b_txt.delete(1.0,tk.END)
        b_txt.insert(tk.END, dict_out_values['TEXT'][8])

    def gps():
        (lat, lon) = nmea2deg(dict_in['GPS'])
        dict_in['GPS'] = (lat, lon) #TODO nie zmieniac dict_in
        update_dict_out('GPS')
        gps_txt.delete(1.0,tk.END)
        gps_txt.insert(tk.END, f"{dict_out_values['GPS'][0]:.7f}\n{dict_out_values['GPS'][1]:.7f}")

    def dwm():
        update_dict_out('DWM')

    options = {'FROM': fro,
                'TO' : to,
                'TEXT' : text,
                'GPS' : gps,
               'DWM' :dwm}

    for key in dict_in:
        try:
            options[key]()
        except:
            pass

    return (dict_out_values, dict_out_time)

def visualise_data(dict_val, dict_time):
    print(f"{dict_val['FROM']}->{dict_val['TO']}\tmessage: {dict_val['TEXT']}\t messagelastupdate: {dict_time['TEXT']}")

def visualise_gui(dv, dt):
    pass

def handle_data(data):
    data = extract(data) # get dict_in
    (dv, dt) = update_data(data)   # get dict out: values and time (last update)
    visualise_data(dv, dt)

# ---- finish flag recognition -----


def prepare_frame(msg):
    frame = f"<FROM=HAB#TO=AS#TEXT={msg}#>"
    for i in range(250-len(frame)):
        frame += "."
    return frame

def send_serial():
    payload = payload_entry.get()
    if not payload:
        print("nothing sent")
    # data = prepare_frame(payload) # just for writingwhat you want
    data = add_dots(payload)        # for fake incoming data
    ser_port.write(str.encode(data))
    # print(f"sent: {data}")
    sent_txt.delete(1.0, tk.END)
    sent_txt.insert(tk.END, data)
    #print(f"send: {str.encode(data)}") #, f"port: {ser}")
    payload_entry.delete(0, tk.END)

def read_serial():
    while 1:
        readData = ser_port.read(250).decode("latin-1")# TODO change
        read_txt.delete(1.0, tk.END)
        read_txt.insert(tk.END, readData)
        # print(f"read: {readData}")
        handle_data(readData) #for fake incomigndata

thread1 = threading.Thread(target=read_serial)
thread1.start()

#--------- GUI ------------

main = tk.Tk()
main.title("GLACiER Habitat Station")
main.geometry('1000x600')

ROW_NO = 0

# SEND DATA
payload_entry = tk.Entry(main, width=90)
payload_entry.grid(column=0, row=0)
# TODO payload_entry.bind('<Return>', func=send_serial)
paybut = tk.Button(main)
paybut.configure(text="send data", command=send_serial)
paybut.grid(column=1, row=ROW_NO)
ROW_NO +=1

# SENT MSG TEXT
sent_lbl = tk.Label(main, text="LAST SENT MESSAGE")
sent_lbl.grid(column=0, row=ROW_NO)
ROW_NO +=1
sent_txt = tk.Text(main, height=3, width=100)
sent_txt.grid(column=0, row=ROW_NO, columnspan=6, sticky='ew')
ROW_NO +=1

# READ MESG TEXT
read_lbl = tk.Label(main, text="LAST READ MESSAGE")
read_lbl.grid(column=0, row=ROW_NO)
ROW_NO +=1
read_txt = tk.Text(main, height=3, width=100)
read_txt.grid(column=0, row=ROW_NO, columnspan=6, sticky='ew')
ROW_NO +=1

# SCROLLBAR
# sc = tk.Scrollbar(main)
# sc.pack(side=tk.RIGHT, fill=tk.Y)
# sent_msgs.pack(side=tk.LEFT, fill=tk.Y)
# sc.config(command=sent_msgs.yview)
# sent_msgs.config(yscrollcommand=sc.set)

## telemetry ##
tel_width = 20
# FROM
from_lbl = tk.Label(main, text="FROM")
from_lbl.grid(column=0, row=ROW_NO, sticky='we')
from_txt = tk.Text(main, height=1, width=tel_width)
from_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# TO
to_lbl = tk.Label(main, text="TO")
to_lbl.grid(column=0, row=ROW_NO)
to_txt = tk.Text(main, height=1, width=tel_width)
to_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# GPS
gps_lbl = tk.Label(main, text="GPS")
gps_lbl.grid(column=0, row=ROW_NO)
gps_txt = tk.Text(main, height=2, width=tel_width)
gps_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# BUTTONS
bu_lbl = tk.Label(main, text=" ASTRONAUT BUTTON")
bu_lbl.grid(column=0, row=ROW_NO)
bu_txt = tk.Text(main, height=2, width=tel_width)
bu_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# WIND DIRECTION
wd_lbl = tk.Label(main, text="WIND DIRECTION")
wd_lbl.grid(column=0, row=ROW_NO)
wd_txt = tk.Text(main, height=1, width=tel_width)
wd_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# WIND SPEED
ws_lbl = tk.Label(main, text="WIND SPEED")
ws_lbl.grid(column=0, row=ROW_NO)
ws_txt = tk.Text(main, height=1, width=tel_width)
ws_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# WIND DIRECTION AVERAGE
wda_lbl = tk.Label(main, text="WIND DIRECTION AVERAGE")
wda_lbl.grid(column=0, row=ROW_NO)
wda_txt = tk.Text(main, height=1, width=tel_width)
wda_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# WIND SPEED AVERAGE
wsa_lbl = tk.Label(main, text="WIND SPEED AVERAGE")
wsa_lbl.grid(column=0, row=ROW_NO)
wsa_txt = tk.Text(main, height=1, width=tel_width)
wsa_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# HUMIDITY
h_lbl = tk.Label(main, text="HUMIDITY")
h_lbl.grid(column=0, row=ROW_NO)
h_txt = tk.Text(main, height=1, width=tel_width)
h_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# TEMPERATURE
t_lbl = tk.Label(main, text="TEMPERATURE")
t_lbl.grid(column=0, row=ROW_NO)
t_txt = tk.Text(main, height=1, width=tel_width)
t_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# PRESSURE
p_lbl = tk.Label(main, text="PRESSURE")
p_lbl.grid(column=0, row=ROW_NO)
p_txt = tk.Text(main, height=1, width=tel_width)
p_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# RAIN
r_lbl = tk.Label(main, text="RAIN")
r_lbl.grid(column=0, row=ROW_NO)
r_txt = tk.Text(main, height=1, width=tel_width)
r_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

# BATTERY
b_lbl = tk.Label(main, text="BATTERY")
b_lbl.grid(column=0, row=ROW_NO)
b_txt = tk.Text(main, height=1, width=tel_width)
b_txt.grid(column=1, row=ROW_NO)
ROW_NO +=1

main.mainloop()
