from __future__ import print_function

import sys
import json
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent, KeyEvent

from typing import *
from getpointGPS import save_gps


is_mouse_clicked = False
map_data = None
xs = []
ys = []
zs = [] # altitude
key_buffer = ""
cur_altitude = 5


def load_json(my_json="data/gremio_map.json") -> None:
    global map_data
    with open(my_json) as data:
        map_data = json.load(data)


def get_color(altitude: float) -> Tuple[float, float, float]:
    """
    Returns a RGB color value for the given altitude
    """
    r = 0
    g = 0.8
    b = altitude / 15
    if b > 1: b = 1
    return (r, g, b)


def plot_map(reset=False) -> None:
    global ax
    
    if reset: ax.clear()
    
    my_map = plt.imread(map_data["map_name"])
    
    ax.set_title("Map Altitude = " + str(cur_altitude))
    ax.set_xlim(map_data["x_min"], map_data["x_max"])
    ax.set_ylim(map_data["y_min"], map_data["y_max"])

    BBox = (map_data["x_min"], map_data["x_max"], map_data["y_min"], map_data["y_max"])

    ax.imshow(my_map, zorder=0, extent=BBox, aspect='equal')


# Events
def save_coords() -> None:
    with open("coords.txt", "w") as f:
        for i in range(len(xs)): 
            f.write(str(xs[i]) + "," + str(ys[i]) + "," + str(zs[i]) + "\n")


def onrelease(event: MouseEvent) -> None:
    global is_mouse_clicked, ax
    is_mouse_clicked = False
    save_coords()
    save_gps()
    plot_map()


def onmovement(event: MouseEvent) -> None:
    if is_mouse_clicked:
        x = event.xdata
        y = event.ydata
        if x is None or y is None: return
        xs.append(x)
        ys.append(y)
        zs.append(cur_altitude)
        
        plt.plot(x, y, ',', marker='o', color=get_color(cur_altitude))
        if len(xs) < 2: return
        plt.plot((xs[-2], xs[-1]), (ys[-2], ys[-1]), linestyle='--', color=get_color(cur_altitude))
        fig.canvas.draw()


def on_press(event: KeyEvent) -> None:
    """
    Listens to keyboard to change altitude
    """
    global key_buffer, xs, ys, zs, ax, fig, cur_altitude
    
    print(event.key)
    if event.key in "1234567890":
        key_buffer += event.key
    elif event.key == "enter" and len(key_buffer) > 0:
        ax.set_title("Map Altitude = " + key_buffer)
        # set altitude to the value of the buffer and clear buffer
        cur_altitude = int(key_buffer)
        key_buffer = ""
    # remove last element of the buffer
    elif event.key == "backspace" and len(key_buffer) > 0:
        key_buffer = key_buffer[:-1]
    elif event.key == "escape":
        xs, ys, zs = [], [], []
        plot_map(True)
    else: return
    
    fig.canvas.draw()
        


def onclick(event: MouseEvent) -> None:
    global is_mouse_clicked
    
    is_mouse_clicked = True


fig, ax = plt.subplots()
# bind events
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_release_event', onrelease)
fig.canvas.mpl_connect('motion_notify_event', onmovement)
fig.canvas.mpl_connect('key_press_event', on_press)


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