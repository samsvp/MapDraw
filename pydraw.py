from __future__ import print_function

import json
import matplotlib.pyplot as plt


with open("data/map.json") as data:
    map_data = json.load(data)

my_map = plt.imread(map_data["map_name"])

fig, ax = plt.subplots()

ax.set_title('Map')
ax.set_xlim(map_data["x_min"], map_data["x_max"])
ax.set_ylim(map_data["y_min"], map_data["y_max"])

BBox = (map_data["x_min"], map_data["x_max"], map_data["y_min"], map_data["y_max"])

ax.imshow(my_map, zorder=0, extent=BBox, aspect='equal')

# Events
is_mouse_clicked = False
xs = []
ys = []

def onrelease(event):
    global is_mouse_clicked
    is_mouse_clicked = False

def onmovement(event):
    if is_mouse_clicked:
        x = event.xdata
        y = event.ydata
        if x is None or y is None: return
        print('longitude:', x, '\nlatitude:', y)
        xs.append(x)
        ys.append(y)
        plt.plot(x, y, ',', marker='o')
        if len(xs) < 2: return
        plt.plot((xs[-2], xs[-1]), (ys[-2], ys[-1]), linestyle='--')
        fig.canvas.draw()

def onclick(event):
    global is_mouse_clicked, xs, ys
    xs = []
    ys = []
    is_mouse_clicked = True

fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_release_event', onrelease)
fig.canvas.mpl_connect('motion_notify_event', onmovement)
plt.show()
