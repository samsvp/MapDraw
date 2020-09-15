# MapDraw
Application to draw points on maps

# Table of Contents
1. [Dependencies](#Dependencies)
2. [Usage](#Usage)
3. [Adding new maps](#Adding-new-maps)


# Dependencies
For python 2.7
```
sudo apt install python-matplotlib
```

For python 3
```
pip install matplotlib
```

# Usage
On the command line run
```
python pydraw.py map_json_name
```
Your map should appear on the screen. You can draw points by clicking and dragging your mouse through the map. 
Once the mouse is released a coords.txt file will be created with the latidude and longitude data. If you wish
to draw a new trajectory follow the same steps previously described. Note that your last coordinates will disappear
and that the coords file will be overwritten.
If you do not specify a map then a default map will be loaded. If you specify more than one map json file then an exception
will be raised.

# Adding new maps
To add a new map create a new json file and add it and its correspondent image inside to the data folder. The json should be formated as follows:
```
{
    "x_max" : longitude_max,
    "x_min" : longitude_min,
    "y_max" : latitude_max,
    "y_min" : latitude_min,
    "map_name" : "data/my_map.png"
}
```
The point (longitude_min, latitude_min) is the bottom-left corner of the screen, while the point (longitude_max, latitude_max) is the 
top right corner of the screen.

Then, to use your map run
```
python pydraw.py my_map_json
```
It is recommended to use the same name for the json and image.
