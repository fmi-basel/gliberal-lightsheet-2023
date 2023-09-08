#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
#                                                                            #
##############################################################################


import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import seaborn as sb


plot_save_vio = "path/to/save/Violinplot.pdf"


path_42_1 = "path/to/csv/42h-P1-Spot.csv"
path_42_2 = "path/to/csv/42h-P2-Spot.csv"
path_42_3 = "path/to/csv/42h-P3-Spot.csv"

path_66_1 = "path/to/csv/66h-P1-Spot.csv"
path_66_2 = "path/to/csv/66h-P2-Spot.csv"
path_66_3 = "path/to/csv/66h-P3-Spot.csv"

path_90_1 = "path/to/csv/90h-P1-Spot.csv"
path_90_2 = "path/to/csv/90h-P2-Spot.csv"
path_90_3 = "path/to/csv/90h-P3-Spot.csv"


path_42 = [path_42_1,path_42_2,path_42_3]
path_66 = [path_66_1,path_66_2,path_66_3]
path_90 = [path_90_1,path_90_2,path_90_3]


cell_tracks_42 = []
for path_ in path_42:
    print(path_)
    data_spot = pd.read_csv(path_, skiprows=[1,2], encoding= 'unicode_escape')
    track_ids = data_spot["Spot track ID"].unique()
    frames = data_spot["Spot frame"].unique()
    frames = sorted(frames)
    for ids in track_ids:
        for tp in range(1,len(frames)):
            try:
                tp_0 = data_spot.loc[(data_spot["Spot track ID"] == ids) & (data_spot["Spot frame"] == tp-1)]
                tp_1 = data_spot.loc[(data_spot["Spot track ID"] == ids) & (data_spot["Spot frame"] == tp)]
                
                x_0 = tp_0["Spot position"].values[0]
                y_0 = tp_0["Spot position.1"].values[0]
                z_0 = tp_0["Spot position.2"].values[0]
                
                x_1 = tp_1["Spot position"].values[0]
                y_1 = tp_1["Spot position.1"].values[0]
                z_1 = tp_1["Spot position.2"].values[0]
                
                track_length = np.sqrt((x_1-x_0)**2 + (y_1-y_0)**2 + (z_1-z_0)**2)
                cell_tracks_42.append(track_length*6)
            except:
                continue

cell_tracks_66 = []
for path_ in path_66:
    print(path_)
    data_spot = pd.read_csv(path_, skiprows=[1,2], encoding= 'unicode_escape')
    track_ids = data_spot["Spot track ID"].unique()
    frames = data_spot["Spot frame"].unique()
    frames = sorted(frames)
    for ids in track_ids:
        for tp in range(1,len(frames)):
            try:
                tp_0 = data_spot.loc[(data_spot["Spot track ID"] == ids) & (data_spot["Spot frame"] == tp-1)]
                tp_1 = data_spot.loc[(data_spot["Spot track ID"] == ids) & (data_spot["Spot frame"] == tp)]
                
                x_0 = tp_0["Spot position"].values[0]
                y_0 = tp_0["Spot position.1"].values[0]
                z_0 = tp_0["Spot position.2"].values[0]
                
                x_1 = tp_1["Spot position"].values[0]
                y_1 = tp_1["Spot position.1"].values[0]
                z_1 = tp_1["Spot position.2"].values[0]
                
                track_length = np.sqrt((x_1-x_0)**2 + (y_1-y_0)**2 + (z_1-z_0)**2)
                cell_tracks_66.append(track_length*6)
            except:
                continue

cell_tracks_90 = []
for path_ in path_90:
    print(path_)
    data_spot = pd.read_csv(path_, skiprows=[1,2], encoding= 'unicode_escape')
    track_ids = data_spot["Spot track ID"].unique()
    frames = data_spot["Spot frame"].unique()
    frames = sorted(frames)
    for ids in track_ids:
        for tp in range(1,len(frames)):
            try:
                tp_0 = data_spot.loc[(data_spot["Spot track ID"] == ids) & (data_spot["Spot frame"] == tp-1)]
                tp_1 = data_spot.loc[(data_spot["Spot track ID"] == ids) & (data_spot["Spot frame"] == tp)]
                
                x_0 = tp_0["Spot position"].values[0]
                y_0 = tp_0["Spot position.1"].values[0]
                z_0 = tp_0["Spot position.2"].values[0]
                
                x_1 = tp_1["Spot position"].values[0]
                y_1 = tp_1["Spot position.1"].values[0]
                z_1 = tp_1["Spot position.2"].values[0]
                
                track_length = np.sqrt((x_1-x_0)**2 + (y_1-y_0)**2 + (z_1-z_0)**2)
                cell_tracks_90.append(track_length*6)
            except:
                continue


cell_tracks_42 = np.asarray(cell_tracks_42)
cell_tracks_66 = np.asarray(cell_tracks_66)
cell_tracks_90 = np.asarray(cell_tracks_90)

x = [1,2,3]

fig = plt.figure(figsize=(7,5))                                                               
ax = fig.add_subplot(1,1,1) 
tracks = [cell_tracks_42,cell_tracks_66,cell_tracks_90]

sb.violinplot(data = [cell_tracks_42,cell_tracks_66,cell_tracks_90], inner="quartile", palette=["#d81b60","#1e88e5","#aee64a"])
my_xticks = ['42h','66h','90h']
x = [0,1,2]
plt.xticks(x, my_xticks)
ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
for label in ticklabels:
    label.set_fontsize(25)

plt.ylabel(r"v [$\mu$m/h]", fontsize = 25)

plt.tight_layout()
plt.savefig(plot_save_vio, bbox_inches = "tight")
plt.show()
plt.close()


