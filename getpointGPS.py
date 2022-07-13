#!/usr/bin/env python3
#%%
import numpy as np
import pymap3d as pm

from numpy import linalg as LA


def save_gps():
    with open("coords.txt") as f:
        data = f.readlines()

    data = np.array(
        # swap axis 0 and 1 and keep axis 2 inplace
        [d.split(",")[:-1][::-1] + [d.split(",")[-1]] 
        for d in data], dtype=float)

    p0 = data[0,:]
    wsg84 = pm.Ellipsoid("wgs84")

    enus = []
    for d in data:
        x, y, z = pm.geodetic2enu(*d, *p0, wsg84) 
        enus.append([x, y, -z])

    enus = np.array(enus)


    w = 4
    # takes average of every w points
    enusf = np.array([np.sum(enus[a:a+w,:], axis=0) / w
        for a in range(0, enus.shape[0] - w, w)])

    ## GenerateTraj.m
    offset = np.array([[5, -10, 0]])
    p = enusf + offset
    # remove points less than 4 meters apart
    new_p = []
    _p = p[0]
    new_p.append(_p)
    for i in range(1, p.shape[0]):
        if LA.norm(_p - p[i]) > 4:
            _p = p[i]
            new_p.append(_p)

    p = np.array(new_p)

    # remove colinear points
    p = np.array([p[0]] + [_p
        for i, _p in enumerate(p[1:-1]) 
        if LA.matrix_rank([p[i] - _p, p[i] - p[i+2]]) != 1
    ] + [p[-1]])


    # # why is p1_ == p2_? no idea
    p1_, p2_, p3_ = p[0,:-1], p[0,:-1], p[1,:-1]

    upa=p1_-p2_ # 0 because p1_ == p2_
    nua=np.sqrt(upa@upa)
    upb=p1_-p3_
    nub=np.sqrt(upb@upb)

    if nua >= 1e-1:
        if nub < 1e-1:
            p = p[1:]
        else:
            c = upa@upb / (nua@nub + 1e-10)
            if abs(c) < (1-2e-4):
                p = np.array([p[0]] + [p])

    with open("points_py.yaml", "w") as f:
        f.write(f"px: {p[:,0].tolist()}\n")
        f.write(f"py: {p[:,1].tolist()}\n")
        f.write(f"pz: {p[:,2].tolist()}\n")


# %%
