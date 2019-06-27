import matplotlib.pyplot as plt
import matplotlib.animation as an
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

f = open("test_data/gnss_eva_1a_noempytlines.txt").readlines()
gps_x = [float(item) for item in f[1::2]]
gps_y = [float(item) for item in f[::2]]
# data = [(gps_x[i], gps_y[i]) for i in range(len(gps_x))]
x_iter = iter(gps_x)
y_iter = iter(gps_y)

# NW, SW, SE, NE
bound = [[45.937379, 7.729218], [45.936366, 7.729487], [45.936390, 7.729751], [45.937404, 7.729457],[45.937379, 7.729218]]
x_b = [i[1]for i in bound]
y_b = [i[0]for i in bound]

main = tk.Tk()

fig, ax = plt.subplots()
ax.grid()
plt.scatter(x_b,y_b,c='y')
ax.plot(x_b,y_b,c='y')
x, y = [] , []
sc = ax.scatter(x,y)

plt.xlim(min(x_b),max(x_b))
plt.ylim(min(y_b),max(y_b))
plt.gca().set_aspect('equal', adjustable='box')

line2 = FigureCanvasTkAgg(fig, main)
line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

def animate(i):
    x.append(next(x_iter))
    y.append(next(y_iter))
    X = np.c_[x,y]
    sc.set_offsets(X)  # if we use ax.scatter instead, all existing points are overwritten

    # xmin=X[:,0].min(); xmax=X[:,0].max()
    # ymin=X[:,1].min(); ymax=X[:,1].max()
    # ax.set_xlim(xmin-0.1*(xmax-xmin),xmax+0.1*(xmax-xmin))
    # ax.set_ylim(ymin-0.1*(ymax-ymin),ymax+0.1*(ymax-ymin))


ani = an.FuncAnimation(fig, animate, frames=3, interval=1000, repeat=True)
# plt.show()
main.mainloop()
