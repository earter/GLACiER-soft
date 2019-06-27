import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.animation as an
import numpy as np
import tkinter as tk
import threading
import serial
import datetime
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# in habitat. simultaneously reads data from GroundStation and sends to astronaut via GS

global fake
fake = 0

global xgn, ygn # x gnss new
xgn, ygn = 46.01621833,  7.74833983

port_name = "/dev/ttyACM0"
global ser_port
ser_port = serial.Serial(port_name, 115200)
print(f"port opened: {ser_port.name}")

now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

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

        handle_data(read_data)


thread1 = threading.Thread(target=read_serial)
thread1.start()


# --------- GUI ------------

main = tk.Tk()
main.title("GLACiER Habitat Station")
main.geometry('1000x700')


ROW_NO = 0

# SEND DATA
payload_entry = tk.Entry(main, width=50)
payload_entry.grid(column=0, row=0, columnspan=2, sticky='ew')
# TODO payload_entry.bind('<Return>', func=send_serial)
paybut = tk.Button(main)
paybut.configure(text="send data", command=send_serial)
paybut.grid(column=2, row=ROW_NO)
ROW_NO += 1

msg_height = 6
# SENT MSG TEXT
sent_lbl = tk.Label(main, text="SENT MESSAGES")
sent_lbl.grid(column=0, row=ROW_NO)
ROW_NO += 1
sent_txt = tk.Text(main, height=2, width=100) #h=4
sent_txt.grid(column=0, row=ROW_NO, columnspan=3, sticky='ew')
ROW_NO += 1

# READ MESG TEXT
read_lbl = tk.Label(main, text="READ MESSAGES")
read_lbl.grid(column=0, row=ROW_NO, sticky='ew')
ROW_NO += 1
read_txt = tk.Text(main, height=4, width=100) #h=8
read_txt.grid(column=0, row=ROW_NO, columnspan=3, sticky='ew')
ROW_NO += 1
plot_row = ROW_NO

# telemetry #
tel_width = 20
tel_stick = 'e'

lab_col = 1
txt_col =2
# FROM
from_lbl = tk.Label(main, text="FROM")
from_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
from_txt = tk.Text(main, height=1, width=tel_width)
from_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# TO
to_lbl = tk.Label(main, text="TO")
to_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
to_txt = tk.Text(main, height=1, width=tel_width)
to_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# GNSS
gnss_lbl = tk.Label(main, text="GNSS [lat, long]")
gnss_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
gnss_txt = tk.Text(main, height=2, width=tel_width)
gnss_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# ASUI BUTTONS
bu_lbl = tk.Label(main, text=" ASTRONAUT BUTTON")
bu_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
bu_txt = tk.Text(main, height=2, width=tel_width)
bu_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# WIND DIRECTION
wd_lbl = tk.Label(main, text="WIND DIRECTION [deg]")
wd_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
wd_txt = tk.Text(main, height=1, width=tel_width)
wd_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# WIND SPEED
ws_lbl = tk.Label(main, text="WIND SPEED [m/s")
ws_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
ws_txt = tk.Text(main, height=1, width=tel_width)
ws_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# WIND DIRECTION AVERAGE
wda_lbl = tk.Label(main, text="WIND DIRECTION AVERAGE [deg]")
wda_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
wda_txt = tk.Text(main, height=1, width=tel_width)
wda_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# WIND SPEED AVERAGE
wsa_lbl = tk.Label(main, text="WIND SPEED AVERAGE [m/s]")
wsa_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
wsa_txt = tk.Text(main, height=1, width=tel_width)
wsa_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# HUMIDITY
h_lbl = tk.Label(main, text="HUMIDITY [%]")
h_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
h_txt = tk.Text(main, height=1, width=tel_width)
h_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# TEMPERATURE
t_lbl = tk.Label(main, text="TEMPERATURE [*C]")
t_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
t_txt = tk.Text(main, height=1, width=tel_width)
t_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# PRESSURE
p_lbl = tk.Label(main, text="PRESSURE [hPA]")
p_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
p_txt = tk.Text(main, height=1, width=tel_width)
p_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# RAIN
r_lbl = tk.Label(main, text="RAIN [inch/hour]")
r_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
r_txt = tk.Text(main, height=1, width=tel_width)
r_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1

# BATTERY
b_lbl = tk.Label(main, text="GROUND STATION BATTERY [V]")
b_lbl.grid(column=lab_col, row=ROW_NO, sticky=tel_stick)
b_txt = tk.Text(main, height=1, width=tel_width)
b_txt.grid(column=txt_col, row=ROW_NO)
ROW_NO += 1


# -------- visu
f = open("test_data/gnss_eva_1a_noempytlines.txt").readlines()
gps_x = [float(item) for item in f[1::2]]
gps_y = [float(item) for item in f[::2]]
# data = [(gps_x[i], gps_y[i]) for i in range(len(gps_x))]
x_iter = iter(gps_x)
y_iter = iter(gps_y)

# NW, SW, SE, NE
# bound = [[45.937379, 7.729218], [45.936366, 7.729487], [45.936390, 7.729751], [45.937404, 7.729457],[45.937379, 7.729218]] # glacier
bound = [[46.016134, 7.748301], [46.016026, 7.748325], [46.016056, 7.748508], [46.016159, 7.748470], [46.016134, 7.748301]] # hotel
x_b = [i[1]for i in bound]
y_b = [i[0]for i in bound]


fig = plt.Figure(figsize=(5,5), dpi=100)
ax = fig.add_subplot(111)
ax.grid()
plt.scatter(x_b,y_b,c='y')
ax.plot(x_b,y_b,c='y')
x, y = [] , []
sc = ax.scatter(x,y)

# plt.xlim(min(x_b),max(x_b))
# plt.ylim(min(y_b),max(y_b))

plt.xlim(0.9*min(x_b),1.1*max(x_b))
plt.ylim(0.9*min(y_b),1.1*max(y_b))

plt.gca().set_aspect('equal', adjustable='box')

line2 = FigureCanvasTkAgg(fig, main)
# line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
line2.get_tk_widget().grid(column=0, row=plot_row, rowspan=20)
ROW_NO += 1


def animate(i):
    x.append(xgn)
    y.append(ygn)
    X = np.c_[x,y]
    sc.set_offsets(X)  # if we use ax.scatter instead, all existing points are overwritten
    print(X)
    # xmin=X[:,0].min(); xmax=X[:,0].max()
    # ymin=X[:,1].min(); ymax=X[:,1].max()
    # ax.set_xlim(xmin-0.1*(xmax-xmin),xmax+0.1*(xmax-xmin))
    # ax.set_ylim(ymin-0.1*(ymax-ymin),ymax+0.1*(ymax-ymin))


ani = an.FuncAnimation(fig, animate, frames=3, interval=1000, repeat=True)


# -------- end visu

main.mainloop()


