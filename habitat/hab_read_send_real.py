import matplotlib.pyplot as plt
import matplotlib.animation as an
import numpy as np
import tkinter as tk
import time
import threading
import serial
import datetime
import sys

# in habitat. simultaneously reads data from GroundStation and sends to astronaut via GS

global fake
fake = 0

port_name = "/dev/ttyACM0"
global ser_port
ser_port = serial.Serial(port_name, 115200)
print(f"port opened: {ser_port.name}")

# now = datetime.datetime.now().strftime('%H:%M:%S')
# f = open(f"log_{now}.log", "a+")


keys_all = ['FROM', 'TO', 'TEXT']
values_init = ['GS', 'HAB', 'INIT TEXT']
dict_out_values = {}
dict_out_time = {}
for i in range(len(keys_all)):
    dict_out_values[keys_all[i]] = values_init[i]
    dict_out_time[keys_all[i]] = 0


def extract_text_data(data):
    data = data.split(',')
    data = [item.split(':') for item in data]
    dict_text = {}
    for item in data:
        dict_text[item[0]] = float(item[1])
    return tuple(dict_text.values())


def extract(data):  # used on raw read_data to put data in dictionary
    if not fake:
        data = (data.split('<')[1].split('>')[0])
    split_data = data.split("#")
    split_data.remove('')
    split1 = [item.split("=") for item in split_data]
    dict_in = {}
    for val in range(len(split1)):
        dict_in[split1[val][0]] = split1[val][1]
    return dict_in


def weather():
    """ TODO
    weather_list = ['wd', 'ws', 'wda', 'wsa', 'h', 't', 'r', 'p', 'b']
    for i in range(0,len(weather_list)+1):
        val = f"{weather_list[i]}_txt"
        print(val, type(val))
        try:
            val.delete(1.0,tk.END)
            val.insert(tk.END, dict_out_values['TEXT'][i])
        except:
            print(f"assigning weather data {val} unsuccesful")
    """
    wd_txt.delete(1.0, tk.END)
    wd_txt.insert(tk.END, dict_out_values['TEXT'][0]*10.0)
    ws_txt.delete(1.0, tk.END)
    ws_txt.insert(tk.END, dict_out_values['TEXT'][1]/10.0)
    wda_txt.delete(1.0, tk.END)
    wda_txt.insert(tk.END, dict_out_values['TEXT'][2]*10.0)
    wsa_txt.delete(1.0, tk.END)
    wsa_txt.insert(tk.END, dict_out_values['TEXT'][3]/10.0)
    h_txt.delete(1.0, tk.END)
    h_txt.insert(tk.END, dict_out_values['TEXT'][4])
    t_txt.delete(1.0, tk.END)
    t_txt.insert(tk.END, dict_out_values['TEXT'][5])
    p_txt.delete(1.0, tk.END)
    p_txt.insert(tk.END, dict_out_values['TEXT'][7]/10.0)
    r_txt.delete(1.0, tk.END)
    r_txt.insert(tk.END, dict_out_values['TEXT'][6])
    b_txt.delete(1.0, tk.END)
    b_txt.insert(tk.END, dict_out_values['TEXT'][8]/100.0)

def update_data(dict_in):

    def update_dict_out(key):
        dict_out_values[key] = dict_in[key]
        dict_out_time[key] = datetime.datetime.now().strftime('%H:%M:%S')

    def fro():
        update_dict_out('FROM')
        from_txt.delete(1.0, tk.END)
        from_txt.insert(tk.END, dict_out_values['FROM'])

    def to():
        update_dict_out('TO')
        to_txt.delete(1.0, tk.END)
        to_txt.insert(tk.END, dict_out_values['TO'])

    def text():
        if dict_in['FROM'] == 'ASGNSS' or  dict_in['FROM'] == 'ASGNSSGS':
            gnss()
            # dict_in['TEXT'] = gnss()
            gnss_txt.delete(1.0, tk.END)
            gnss_txt.insert(tk.END, f"{dict_out_values['TEXT'][0]:.7f}\n{dict_out_values['TEXT'][1]:.7f}")

        elif dict_in['FROM'] == 'GSWEA':
            dict_in['TEXT'] = extract_text_data(dict_in['TEXT'])  # TODO nie zmieniac dictin. poprawic upadte dic()
            update_dict_out('TEXT')
            weather()

        elif (dict_in['FROM'] == 'ASUI' or dict_in['FROM'] == 'ASUIGS'):
            dict_in['TEXT'] = extract_text_data(dict_in['TEXT'])  # TODO nie zmieniac dictin. poprawic upadte dic()
            if dict_in['TEXT'] == "1.0":
                dict_in['TEXT'] = "1\n YES"
            elif dict_in['TEXT'] == 2.0:
                dict_in['TEXT'] = "2\n NO"
            elif dict_in['TEXT'] == 3.0:
                dict_in['TEXT'] = "3\n I'M IN DANGER"
            elif dict_in['TEXT'] == 4.0:
                dict_in['TEXT'] = "4\n CONFIRMED"
            update_dict_out('TEXT')
            bu_txt.delete(1.0, tk.END)
            bu_txt.insert(tk.END, dict_out_values['TEXT'][0])

    def gnss():
        def nmea2deg(raw):
            def degmin(val):    # splits deg&mins in NMEA data
                valt = val.split('.')
                threshold = 3 if len(valt[0]) == 5 else 2
                return float(val[0:threshold]), float(val[threshold:])
            raw = raw.split(',')
            lat = degmin(raw[0])
            lon = degmin(raw[1])
            latdeg = lat[0] + lat[1]/60.0  # *(-1) for W and S
            londeg = lon[0] + lon[1]/60.0  # *(-1) for W and S
            return latdeg, londeg

        (lat, lon) = nmea2deg(dict_in['TEXT'])
        dict_in['TEXT'] = (lat, lon)  # TODO nie zmieniac dict_in
        print(lat, lon)
        update_dict_out('TEXT')



    options = {'FROM': fro,
               'TO': to,
               'TEXT': text,
               'GNSS': gnss}

    for key in dict_in:
        try:
            options[key]()
        except:
            pass

    return dict_out_values, dict_out_time


def write_console_data(dict_val, dict_time):
    print(f"{dict_val['FROM']}->{dict_val['TO']}\tmessage: {dict_val['TEXT']}\t messagelastupdate: {dict_time['TEXT']}")


def handle_data(data):
    data = extract(data)  # get dict_in
    (dv, dt) = update_data(data)   # get dict out: values and time (last update)
    # write_console_data(dv, dt)

def prepare_frame(msg):
    frame = f"<FROM=HAB#TO=AS#TEXT={msg}#>"
    bare_frame = frame
    for i in range(250-len(frame)):
        frame += "."
    frame += '\n'
    return frame, bare_frame


def add_dots(frame):        # TODO oneliner
    frame = frame.rstrip()
    for i in range(250-len(frame)):
        frame += "."
    frame += '\n'
    return frame


def send_serial():
    payload = payload_entry.get()
    if not payload:
        print("nothing sent")
    if fake:
        send_data = add_dots(payload)          # for fake incoming <data> (fake/tests)
    else:
        send_data, bare_frame = prepare_frame(payload)     # just for writing what you want(real action)

    ser_port.write(str.encode(send_data))
    send_date = datetime.datetime.now().strftime('%H:%M:%S')
    print_send_data = f"[{send_date}] {bare_frame}\n"
    # sent_txt.delete(1.0, tk.END)
    sent_txt.insert(tk.END, print_send_data)
    sent_txt.see(tk.END)
    payload_entry.delete(0, tk.END)


def read_serial():
    while 1:
        read_data = ser_port.readline().decode()
        # read_data = ser_port.read(250).decode()
        if fake:
            # print(f"ugabuga: {read_data.split('>',1)[0]}")
            read_data = (read_data.split('<')[1].split('>')[0])
        read_date = datetime.datetime.now().strftime('%H:%M:%S')
        print_read_data = f"[{read_date}] {read_data}"
        # read_txt.delete(1.0, tk.END)
        # print(f"read: {print_read_data}")
        read_txt.insert(tk.END, print_read_data)
        read_txt.see(tk.END)

        # f = open(f"log_{now}.log", "w")
        # f.seek(0)
        # f.write(f"{print_read_data}\n")
        # f.close()
        handle_data(read_data)


thread1 = threading.Thread(target=read_serial)
thread1.start()

# -------- visu
#
# f = open("test_data/gnss_eva_1a_noempytlines.txt").readlines()
# gps_x = [float(item) for item in f[1::2]]
# gps_y = [float(item) for item in f[::2]]
# # data = [(gps_x[i], gps_y[i]) for i in range(len(gps_x))]
#
# fig, ax = plt.subplots()
# ax.grid()
# sc = ax.scatter(x_gnss,y_gnss,c='r')
# # plt.xlim(min(gps_x),max(gps_x))
# # plt.ylim(min(gps_y),max(gps_y))
# plt.xlim(7,8)
# plt.ylim(43,44)
#
# def animate(i,gnss_data_new):
#     print(f"gnss new animation: {gnss_data_new}")
#     x_gnss.append(gnss_data_new[0])
#     y_gnss.append(gnss_data_new[1])
#     sc.set_offsets(np.c_[x_gnss, y_gnss])
#     # print(np.c_[x_gnss,y_gnss])
#
# ani = an.FuncAnimation(fig, animate, fargs=(gnss_data_new,), frames=3, interval=1000, repeat=True)
# plt.show()

# -------- end visu

# --------- GUI ------------

main = tk.Tk()
main.title("GLACiER Habitat Station")
main.geometry('1000x700')

ROW_NO = 0

# SEND DATA
payload_entry = tk.Entry(main, width=90)
payload_entry.grid(column=0, row=0)
# TODO payload_entry.bind('<Return>', func=send_serial)
paybut = tk.Button(main)
paybut.configure(text="send data", command=send_serial)
paybut.grid(column=1, row=ROW_NO)
ROW_NO += 1

msg_height = 6
# SENT MSG TEXT
sent_lbl = tk.Label(main, text="SENT MESSAGES")
sent_lbl.grid(column=0, row=ROW_NO)
ROW_NO += 1
sent_txt = tk.Text(main, height=4, width=100)
sent_txt.grid(column=0, row=ROW_NO, columnspan=6, sticky='ew')
ROW_NO += 1

# READ MESG TEXT
read_lbl = tk.Label(main, text="READ MESSAGES")
read_lbl.grid(column=0, row=ROW_NO)
ROW_NO += 1
read_txt = tk.Text(main, height=8, width=100)
read_txt.grid(column=0, row=ROW_NO, columnspan=6, sticky='ew')
ROW_NO += 1

# telemetry #
tel_width = 20
tel_stick = 'e'

# FROM
from_lbl = tk.Label(main, text="FROM")
from_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
from_txt = tk.Text(main, height=1, width=tel_width)
from_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# TO
to_lbl = tk.Label(main, text="TO")
to_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
to_txt = tk.Text(main, height=1, width=tel_width)
to_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# GNSS
gnss_lbl = tk.Label(main, text="GNSS [lat, long]")
gnss_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
gnss_txt = tk.Text(main, height=2, width=tel_width)
gnss_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# ASUI BUTTONS
bu_lbl = tk.Label(main, text=" ASTRONAUT BUTTON")
bu_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
bu_txt = tk.Text(main, height=2, width=tel_width)
bu_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# WIND DIRECTION
wd_lbl = tk.Label(main, text="WIND DIRECTION [deg]")
wd_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
wd_txt = tk.Text(main, height=1, width=tel_width)
wd_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# WIND SPEED
ws_lbl = tk.Label(main, text="WIND SPEED [m/s")
ws_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
ws_txt = tk.Text(main, height=1, width=tel_width)
ws_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# WIND DIRECTION AVERAGE
wda_lbl = tk.Label(main, text="WIND DIRECTION AVERAGE [deg]")
wda_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
wda_txt = tk.Text(main, height=1, width=tel_width)
wda_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# WIND SPEED AVERAGE
wsa_lbl = tk.Label(main, text="WIND SPEED AVERAGE [m/s]")
wsa_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
wsa_txt = tk.Text(main, height=1, width=tel_width)
wsa_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# HUMIDITY
h_lbl = tk.Label(main, text="HUMIDITY [%]")
h_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
h_txt = tk.Text(main, height=1, width=tel_width)
h_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# TEMPERATURE
t_lbl = tk.Label(main, text="TEMPERATURE [*C]")
t_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
t_txt = tk.Text(main, height=1, width=tel_width)
t_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# PRESSURE
p_lbl = tk.Label(main, text="PRESSURE [hPA]")
p_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
p_txt = tk.Text(main, height=1, width=tel_width)
p_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# RAIN
r_lbl = tk.Label(main, text="RAIN [inch/hour]")
r_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
r_txt = tk.Text(main, height=1, width=tel_width)
r_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

# BATTERY
b_lbl = tk.Label(main, text="GROUND STATION BATTERY [V]")
b_lbl.grid(column=0, row=ROW_NO, sticky=tel_stick)
b_txt = tk.Text(main, height=1, width=tel_width)
b_txt.grid(column=1, row=ROW_NO)
ROW_NO += 1

main.mainloop()


