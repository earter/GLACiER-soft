import matplotlib.pyplot as plt
import gui
import tkinter as tk
import os

# https://github.com/pratikguru/Instructables/blob/master/uart_visualizer.py

main = tk.Tk()

main.title("GLACiER Habitat Station")
main.geometry('600x400')

asui_payload = tk.StringVar()
paylbl = tk.Label(main, text="send data")
paylbl.grid(column=0, row=0)
payload_entry = tk.Entry(main, textvariable=asui_payload)
payload_entry.grid(column=1, row=0)

main.mainloop()
#
# from tkinter import *
#
# window = tk.Tk()
#
# window.title("Welcome to LikeGeeks app")
#
# window.geometry('350x200')
#
# lbl = Label(window, text="Hello")
#
# lbl.grid(column=0, row=0)
#
# def clicked():
#
#     lbl.configure(text="Button was clicked !!")
#
# btn = Button(window, text="Click Me", command=clicked)
#
# btn.grid(column=1, row=0)
#
# window.mainloop()
#
#
