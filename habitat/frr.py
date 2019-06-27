import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

fig, ax = plt.subplots()

data = np.cumsum(np.random.normal(size=10)) #some list of data

ax.grid()
sc = ax.scatter(data[::2], data[1::2], c=data[1::2])

def plot(a, data):
    data += np.cumsum(np.random.normal(size=10)+3e-2)
    X = np.c_[data[::2], data[1::2]]
    print(X)
    sc.set_offsets(X)

    # manually relim:
    xmin=X[:,0].min(); xmax=X[:,0].max()
    ymin=X[:,1].min(); ymax=X[:,1].max()
    ax.set_xlim(xmin-0.1*(xmax-xmin),xmax+0.1*(xmax-xmin))
    ax.set_ylim(ymin-0.1*(ymax-ymin),ymax+0.1*(ymax-ymin))

ani = matplotlib.animation.FuncAnimation(fig, plot, fargs=(data,),
            frames=4, interval=1000, repeat=True)
plt.show()
