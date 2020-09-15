from __future__ import print_function

import sys
import json
import matplotlib.pyplot as plt

is_mouse_clicked = False
map_data = None
xs = []
ys = []

def load_json(my_json="data/gremio_map.json"):
    global map_data
    with open(my_json) as data:
        map_data = json.load(data)

def plot_map():
    global ax
    
    ax.clear()
    
    my_map = plt.imread(map_data["map_name"])
    
    ax.set_title('Map')
    ax.set_xlim(map_data["x_min"], map_data["x_max"])
    ax.set_ylim(map_data["y_min"], map_data["y_max"])

    BBox = (map_data["x_min"], map_data["x_max"], map_data["y_min"], map_data["y_max"])

    ax.imshow(my_map, zorder=0, extent=BBox, aspect='equal')

# Events

def save_coords():
    with open("coords.txt", "w") as f:
        for i in range(len(xs)): f.write(str(xs[i]) + "," + str(ys[i]) + "\n")

def onrelease(event):
    global is_mouse_clicked, ax
    is_mouse_clicked = False
    save_coords()
    plot_map()

def onmovement(event):
    if is_mouse_clicked:
        x = event.xdata
        y = event.ydata
        if x is None or y is None: return
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


fig, ax = plt.subplots()
# bind events
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_release_event', onrelease)
fig.canvas.mpl_connect('motion_notify_event', onmovement)

if __name__ == "__main__":
    if len(sys.argv) == 2: 
        my_file = sys.argv[-1]
        if not my_file.endswith(".json"): my_file += ".json"
        if not my_file.startswith("data/"): my_file = "data/" + my_file
        load_json(my_file)
    elif len(sys.argv) == 1: load_json()
    else: raise Exception("Invalid number of parameters")

    plot_map()
    plt.show()