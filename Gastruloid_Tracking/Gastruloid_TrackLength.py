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


path_save = "/ExampleData/Output/Gastruloid_TrackLength.pdf"

path_data_42_1 = "/ExampleData/Gastruloid/42h/P2-Spot.csv"
path_data_42_2 = "/ExampleData/Gastruloid/42h/P5-Spot.csv"
path_data_42_3 = "/ExampleData/Gastruloid/42h/P6-Spot.csv"

path_data_66_1 = "/ExampleData/Gastruloid/66h/P2-Spot.csv"
path_data_66_2 = "/ExampleData/Gastruloid/66h/P3-Spot.csv"
path_data_66_3 = "/ExampleData/Gastruloid/66h/P4-Spot.csv"

path_data_90_1 = "/ExampleData/Gastruloid/90h/P4-Spot.csv"
path_data_90_2 = "/ExampleData/Gastruloid/90h/P8-Spot.csv"
path_data_90_3 = "/ExampleData/Gastruloid/90h/P9-Spot.csv"


path_42 = [path_data_42_1,path_data_42_2,path_data_42_3]
path_66 = [path_data_66_1,path_data_66_2,path_data_66_3]
path_90 = [path_data_90_1,path_data_90_2,path_data_90_3]


ct_42_x = []
ct_42_y = []
ct_42_z = []


for path_ in path_42:
    data_spot = pd.read_csv(path_, skiprows=[1,2], encoding= 'unicode_escape')
    track_ids = data_spot["Spot track ID"].unique()
    frames = data_spot["Spot frame"].unique()
    frames = sorted(frames)
    t_name = path_.split("/")
    t_name = t_name[-1]
    t_name = t_name.split(".")
    t_name = t_name[0]
    t_name_ = t_name.split("-")
    t_name_1 = t_name_[0]
    t_name_2 = t_name_[1]
    

    for ids in track_ids:
        cell_tracks_42_x = []
        cell_tracks_42_y = []
        cell_tracks_42_z = []
        for tp in range(0,len(frames)):
            try:
                tp_0 = data_spot.loc[(data_spot["Spot track ID"] == ids) & (data_spot["Spot frame"] == tp)]
         
                x_0 = tp_0["Spot position"].values[0]
                y_0 = tp_0["Spot position.1"].values[0]
                z_0 = tp_0["Spot position.2"].values[0]
                
                cell_tracks_42_x.append(x_0)
                cell_tracks_42_y.append(y_0)
                cell_tracks_42_z.append(z_0)
       
            except:
                continue
        cell_tracks_42_x = np.asarray(cell_tracks_42_x)
        cell_tracks_42_y = np.asarray(cell_tracks_42_y)
        cell_tracks_42_z = np.asarray(cell_tracks_42_z)
        

        ct_42_x.append(cell_tracks_42_x)
        ct_42_y.append(cell_tracks_42_y)
        ct_42_z.append(cell_tracks_42_z)




ct_66_x = []
ct_66_y = []
ct_66_z = []


for path_ in path_66:
    data_spot = pd.read_csv(path_, skiprows=[1,2], encoding= 'unicode_escape')
    track_ids = data_spot["Spot track ID"].unique()
    frames = data_spot["Spot frame"].unique()
    frames = sorted(frames)
    t_name = path_.split("/")
    t_name = t_name[-1]
    t_name = t_name.split(".")
    t_name = t_name[0]
    t_name_ = t_name.split("-")
    t_name_1 = t_name_[0]
    t_name_2 = t_name_[1]

    for ids in track_ids:
        cell_tracks_66_x = []
        cell_tracks_66_y = []
        cell_tracks_66_z = []
        for tp in range(0,len(frames)):
            try:
                tp_0 = data_spot.loc[(data_spot["Spot track ID"] == ids) & (data_spot["Spot frame"] == tp)]
                
                x_0 = tp_0["Spot position"].values[0]
                y_0 = tp_0["Spot position.1"].values[0]
                z_0 = tp_0["Spot position.2"].values[0]
                
                cell_tracks_66_x.append(x_0)
                cell_tracks_66_y.append(y_0)
                cell_tracks_66_z.append(z_0)                

            except:
                continue
        cell_tracks_66_x = np.asarray(cell_tracks_66_x)
        cell_tracks_66_y = np.asarray(cell_tracks_66_y)
        cell_tracks_66_z = np.asarray(cell_tracks_66_z)

        ct_66_x.append(cell_tracks_66_x)
        ct_66_y.append(cell_tracks_66_y)
        ct_66_z.append(cell_tracks_66_z)



ct_90_x = []
ct_90_y = []
ct_90_z = []

for path_ in path_90:
    data_spot = pd.read_csv(path_, skiprows=[1,2], encoding= 'unicode_escape')
    track_ids = data_spot["Spot track ID"].unique()
    frames = data_spot["Spot frame"].unique()
    frames = sorted(frames)
    t_name = path_.split("/")
    t_name = t_name[-1]
    t_name = t_name.split(".")
    t_name = t_name[0]
    t_name_ = t_name.split("-")
    t_name_1 = t_name_[0]
    t_name_2 = t_name_[1]
    

    for ids in track_ids:
        cell_tracks_90_x = []
        cell_tracks_90_y = []
        cell_tracks_90_z = []
        for tp in range(0,len(frames)):
            try:
                tp_0 = data_spot.loc[(data_spot["Spot track ID"] == ids) & (data_spot["Spot frame"] == tp)]
                
                x_0 = tp_0["Spot position"].values[0]
                y_0 = tp_0["Spot position.1"].values[0]
                z_0 = tp_0["Spot position.2"].values[0]
                
                cell_tracks_90_x.append(x_0)
                cell_tracks_90_y.append(y_0)
                cell_tracks_90_z.append(z_0)
            except:
                continue
        cell_tracks_90_x = np.asarray(cell_tracks_90_x)
        cell_tracks_90_y = np.asarray(cell_tracks_90_y)
        cell_tracks_90_z = np.asarray(cell_tracks_90_z)
        
        ct_90_x.append(cell_tracks_90_x)
        ct_90_y.append(cell_tracks_90_y)
        ct_90_z.append(cell_tracks_90_z)
        
        
for i in range(len(ct_42_x)):
    x = ct_42_x[i][0]
    y = ct_42_y[i][0]
    z = ct_42_z[i][0]
    for j in range(len(ct_42_x[i])):
        ct_42_x[i][j] = ct_42_x[i][j] - x
        ct_42_y[i][j] = ct_42_y[i][j] - y
        ct_42_z[i][j] = ct_42_z[i][j] - z        

for i in range(len(ct_66_x)):
    x = ct_66_x[i][0]
    y = ct_66_y[i][0]
    z = ct_66_z[i][0]
    for j in range(len(ct_66_x[i])):
        ct_66_x[i][j] = ct_66_x[i][j] - x
        ct_66_y[i][j] = ct_66_y[i][j] - y
        ct_66_z[i][j] = ct_66_z[i][j] - z
    
for i in range(len(ct_90_x)):
    x = ct_90_x[i][0]
    y = ct_90_y[i][0]
    z = ct_90_z[i][0]
    for j in range(len(ct_90_x[i])):
        ct_90_x[i][j] = ct_90_x[i][j] - x
        ct_90_y[i][j] = ct_90_y[i][j] - y
        ct_90_z[i][j] = ct_90_z[i][j] - z


mean_90_sum = []
for i in range(len(ct_90_x)):
    c = []
    for j in range(0,len(ct_90_x)-1):  
        x = ct_90_x[i][j+1] - ct_90_x[i][j]
        y = ct_90_y[i][j+1] - ct_90_y[i][j]
        z = ct_90_z[i][j+1] - ct_90_z[i][j]
        c.append(np.linalg.norm([x, y, z]))
    mean_90_sum.append(np.sum(c))
    
    
mean_66_sum = []
for i in range(len(ct_66_x)):
    c = []
    for j in range(0,len(ct_66_x)-1):
        x = ct_66_x[i][j+1] - ct_66_x[i][j]
        y = ct_66_y[i][j+1] - ct_66_y[i][j]
        z = ct_66_z[i][j+1] - ct_66_z[i][j]    
        c.append(np.linalg.norm([x, y, z]))
    mean_66_sum.append(np.sum(c))
    

mean_42_sum = []
for i in range(len(ct_42_x)):
    c = []
    for j in range(0,len(ct_42_x)-1):
        x = ct_42_x[i][j+1] - ct_42_x[i][j]
        y = ct_42_y[i][j+1] - ct_42_y[i][j]
        z = ct_42_z[i][j+1] - ct_42_z[i][j]    
        c.append(np.linalg.norm([x, y, z]))    
    mean_42_sum.append(np.sum(c))


x = [0,1,2]


fig = plt.figure(figsize=(7,5))                                                               
ax = fig.add_subplot(1,1,1) 

sb.violinplot(data = [mean_42_sum,mean_66_sum,mean_90_sum], inner="quartile", palette=["#d81b60","#1e88e5","#aee64a"])
my_xticks = ['42h','66h','90h']
x = [0,1,2]
plt.xticks(x, my_xticks)
ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
for label in ticklabels:
    label.set_fontsize(25)

plt.ylabel(r"Track Length [$\mu$m]", fontsize = 25)

plt.tight_layout()
plt.savefig(path_save, bbox_inches = "tight")
plt.show()
plt.close()


