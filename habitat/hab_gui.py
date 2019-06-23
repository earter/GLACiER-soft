import tkinter as tk


def hab_gui():
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
    ROW_NO += 1

    # SENT MSG TEXT
    sent_lbl = tk.Label(main, text="LAST SENT MESSAGE")
    sent_lbl.grid(column=0, row=ROW_NO)
    ROW_NO += 1
    sent_txt = tk.Text(main, height=3, width=100)
    sent_txt.grid(column=0, row=ROW_NO, columnspan=6, sticky='ew')
    ROW_NO += 1

    # READ MESG TEXT
    read_lbl = tk.Label(main, text="LAST READ MESSAGE")
    read_lbl.grid(column=0, row=ROW_NO)
    ROW_NO += 1
    read_txt = tk.Text(main, height=3, width=100)
    read_txt.grid(column=0, row=ROW_NO, columnspan=6, sticky='ew')
    ROW_NO += 1

    # SCROLLBAR
    # sc = tk.Scrollbar(main)
    # sc.pack(side=tk.RIGHT, fill=tk.Y)
    # sent_msgs.pack(side=tk.LEFT, fill=tk.Y)
    # sc.config(command=sent_msgs.yview)
    # sent_msgs.config(yscrollcommand=sc.set)

    # telemetry #
    tel_width = 20
    stick = 'e'
    # FROM
    from_lbl = tk.Label(main, text="FROM")
    from_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    from_txt = tk.Text(main, height=1, width=tel_width)
    from_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # TO
    to_lbl = tk.Label(main, text="TO")
    to_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    to_txt = tk.Text(main, height=1, width=tel_width)
    to_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # GPS
    gps_lbl = tk.Label(main, text="GPS")
    gps_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    gps_txt = tk.Text(main, height=2, width=tel_width)
    gps_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # BUTTONS
    bu_lbl = tk.Label(main, text=" ASTRONAUT BUTTON")
    bu_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    bu_txt = tk.Text(main, height=2, width=tel_width)
    bu_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # WIND DIRECTION
    wd_lbl = tk.Label(main, text="WIND DIRECTION")
    wd_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    wd_txt = tk.Text(main, height=1, width=tel_width)
    wd_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # WIND SPEED
    ws_lbl = tk.Label(main, text="WIND SPEED")
    ws_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    ws_txt = tk.Text(main, height=1, width=tel_width)
    ws_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # WIND DIRECTION AVERAGE
    wda_lbl = tk.Label(main, text="WIND DIRECTION AVERAGE")
    wda_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    wda_txt = tk.Text(main, height=1, width=tel_width)
    wda_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # WIND SPEED AVERAGE
    wsa_lbl = tk.Label(main, text="WIND SPEED AVERAGE")
    wsa_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    wsa_txt = tk.Text(main, height=1, width=tel_width)
    wsa_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # HUMIDITY
    h_lbl = tk.Label(main, text="HUMIDITY")
    h_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    h_txt = tk.Text(main, height=1, width=tel_width)
    h_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # TEMPERATURE
    t_lbl = tk.Label(main, text="TEMPERATURE")
    t_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    t_txt = tk.Text(main, height=1, width=tel_width)
    t_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # PRESSURE
    p_lbl = tk.Label(main, text="PRESSURE")
    p_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    p_txt = tk.Text(main, height=1, width=tel_width)
    p_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # RAIN
    r_lbl = tk.Label(main, text="RAIN")
    r_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    r_txt = tk.Text(main, height=1, width=tel_width)
    r_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    # BATTERY
    b_lbl = tk.Label(main, text="BATTERY")
    b_lbl.grid(column=0, row=ROW_NO, sticky=stick)
    b_txt = tk.Text(main, height=1, width=tel_width)
    b_txt.grid(column=1, row=ROW_NO)
    ROW_NO += 1

    main.mainloop()
