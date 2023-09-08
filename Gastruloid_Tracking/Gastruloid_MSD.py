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

import matplotlib.colors
import matplotlib as mpl



path_save = "/ExampleData/Output/"

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



norm = mpl.colors.Normalize(vmin = 0, vmax = 1)
colors = [mpl.cm.seismic(norm(i)) for i in np.linspace(0, 1, 33)]


cmap = mpl.cm.seismic
norm = mpl.colors.Normalize(0, (33*10)/60)


MSD_cell_42 = []

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



        
fig = plt.figure(figsize = (8,8))
ax = plt.axes(projection='3d')
for i in range(len(ct_42_x)):
    x = ct_42_x[i][0]
    y = ct_42_y[i][0]
    z = ct_42_z[i][0]
    for j in range(len(ct_42_x[i])):
        ct_42_x[i][j] = ct_42_x[i][j] - x
        ct_42_y[i][j] = ct_42_y[i][j] - y
        ct_42_z[i][j] = ct_42_z[i][j] - z




for i in range(len(ct_42_x)):
    for j in range(0,(len(ct_42_x[i])-1)):
        ax.plot(ct_42_x[i][j:j+2], ct_42_y[i][j:j+2], ct_42_z[i][j:j+2], color = colors[j+1])
        
ax.set_ylabel(r"Y-axis [$\mu$m]", fontsize = 20, labelpad=20)
ax.set_xlabel(r"X-axis [$\mu$m]", fontsize = 20, labelpad=15)
ax.zaxis.set_rotate_label(False) 
ax.set_zlabel(r"Z-axis [$\mu$m]", fontsize = 20, labelpad=15, rotation = 90)

ax.set_xlim3d(-50, 50)
ax.set_ylim3d(-50, 50)
ax.set_zlim3d(-50, 50)

ax.set_zticks([-40, 0, 40])
ax.set_yticks([-40, 0, 40])
ax.set_xticks([-40, 0, 40])


ax.zaxis.set_tick_params(labelsize=15)
ax.yaxis.set_tick_params(labelsize=15)
ax.xaxis.set_tick_params(labelsize=15)

ax.set_box_aspect(aspect=None, zoom=0.8)

plt.tight_layout()
plt.savefig(path_save + "42h-Tracjectories.pdf", bbox_inches = "tight")
plt.show()



MSD_cell_66 = []

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


    
fig = plt.figure(figsize = (8,8))
ax = plt.axes(projection='3d')
for i in range(len(ct_66_x)):
    x = ct_66_x[i][0]
    y = ct_66_y[i][0]
    z = ct_66_z[i][0]
    for j in range(len(ct_66_x[i])):
        ct_66_x[i][j] = ct_66_x[i][j] - x
        ct_66_y[i][j] = ct_66_y[i][j] - y
        ct_66_z[i][j] = ct_66_z[i][j] - z
        

 
for i in range(len(ct_66_x)):
    for j in range(0,(len(ct_66_x[i])-1)):
        #print(i,j)
        ax.plot(ct_66_x[i][j:j+2], ct_66_y[i][j:j+2], ct_66_z[i][j:j+2], color = colors[j+1])
    
ax.set_ylabel(r"Y-axis [$\mu$m]", fontsize = 20, labelpad=20)
ax.set_xlabel(r"X-axis [$\mu$m]", fontsize = 20, labelpad=15)
ax.zaxis.set_rotate_label(False) 
ax.set_zlabel(r"Z-axis [$\mu$m]", fontsize = 20, labelpad=15, rotation = 90)

ax.set_xlim3d(-50, 50)
ax.set_ylim3d(-50, 50)
ax.set_zlim3d(-50, 50)

ax.set_zticks([-40, 0, 40])
ax.set_yticks([-40, 0, 40])
ax.set_xticks([-40, 0, 40])


ax.zaxis.set_tick_params(labelsize=15)
ax.yaxis.set_tick_params(labelsize=15)
ax.xaxis.set_tick_params(labelsize=15)

ax.set_box_aspect(aspect=None, zoom=0.8)

plt.tight_layout()
plt.savefig(path_save + "66h-Tracjectories.pdf", bbox_inches = "tight") 
plt.show()
    

 
MSD_cell_90 = []

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
 
    
fig = plt.figure(figsize = (8,8))
ax = plt.axes(projection='3d')
for i in range(len(ct_90_x)):
    x = ct_90_x[i][0]
    y = ct_90_y[i][0]
    z = ct_90_z[i][0]
    for j in range(len(ct_90_x[i])):
        ct_90_x[i][j] = ct_90_x[i][j] - x
        ct_90_y[i][j] = ct_90_y[i][j] - y
        ct_90_z[i][j] = ct_90_z[i][j] - z

for i in range(len(ct_90_x)):
    for j in range(0,(len(ct_90_x[i])-1)):
        #print(i,j)
        ax.plot(ct_90_x[i][j:j+2], ct_90_y[i][j:j+2], ct_90_z[i][j:j+2], color = colors[j+1])
    
ax.set_ylabel(r"Y-axis [$\mu$m]", fontsize = 20, labelpad=20)
ax.set_xlabel(r"X-axis [$\mu$m]", fontsize = 20, labelpad=15)
ax.zaxis.set_rotate_label(False) 
ax.set_zlabel(r"Z-axis [$\mu$m]", fontsize = 20, labelpad=15, rotation = 90)


ax.set_xlim3d(-50, 50)
ax.set_ylim3d(-50, 50)
ax.set_zlim3d(-50, 50)

ax.set_zticks([-40, 0, 40])
ax.set_yticks([-40, 0, 40])
ax.set_xticks([-40, 0, 40])


ax.zaxis.set_tick_params(labelsize=15)
ax.yaxis.set_tick_params(labelsize=15)
ax.xaxis.set_tick_params(labelsize=15)

ax.set_box_aspect(aspect=None, zoom=0.8)

plt.tight_layout()
plt.savefig(path_save + "90h-Tracjectories.pdf",  bbox_inches = "tight")
plt.show()



speed_90 = []
for i in range(len(ct_90_x)):
    speed_cell = []
    for j in range(0,(len(ct_90_x[i])-1)):
        vec_3D = [ct_90_x[i][j+1]-ct_90_x[i][j], ct_90_y[i][j+1]-ct_90_y[i][j], ct_90_z[i][j+1]-ct_90_z[i][j]]
        speed_cell.append(np.linalg.norm(vec_3D)*6)
    speed_90.append(speed_cell)

max_speed = np.max(speed_90)
min_speed = np.min(speed_90)

## MSD ensemble average
MSD_42 = []
for i in range(len(ct_42_x)):
    r = [((ct_42_x[i][j]-ct_42_x[i][0])**2 + (ct_42_y[i][j]-ct_42_y[i][0])**2 + (ct_42_z[i][j]-ct_42_z[i][0])**2) for j in range(1,len(ct_42_x[i]))]
    MSD_42.append(r)

MSD_42_sum = np.asarray(np.sum(MSD_42, axis = 0)/len(ct_42_x))

MSD_66 = []
for i in range(len(ct_66_x)):
    r = [((ct_66_x[i][j]-ct_66_x[i][0])**2 + (ct_66_y[i][j]-ct_66_y[i][0])**2 + (ct_66_z[i][j]-ct_66_z[i][0])**2) for j in range(1,len(ct_66_x[i]))]
    MSD_66.append(r)


MSD_66_sum = np.asarray(np.sum(MSD_66, axis = 0)/len(ct_66_x))

MSD_90 = []
for i in range(len(ct_90_x)):
    r = [((ct_90_x[i][j]-ct_90_x[i][0])**2 + (ct_90_y[i][j]-ct_90_y[i][0])**2 + (ct_90_z[i][j]-ct_90_z[i][0])**2) for j in range(1,len(ct_90_x[i]))]
    MSD_90.append(r)

MSD_90_sum = np.asarray(np.sum(MSD_90, axis = 0)/len(ct_90_x))


x_val = [(i/6) for i in range(0,len(MSD_42_sum))]



fig = plt.figure(figsize=(7,5)) 
ax = fig.add_subplot(1,1,1) 


plt.plot(x_val, MSD_42_sum/1000, ".", ms = 10, color = "#d81b60", label = "42h")
plt.plot(x_val, MSD_66_sum/1000, ".", ms = 10, color = "#1e88e5", label = "66h")
plt.plot(x_val, MSD_90_sum/1000, ".", ms = 10, color = "#aee64a", label = "90h")


plt.xlabel("t [h]", fontsize = 25) 
plt.ylabel(r"MSD$_{3D}$ [$\mu$m$^{2} \cdot 10^{3}$]", fontsize = 25)
ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
for labelss in ticklabels:
    labelss.set_fontsize(25)

plt.legend(fontsize = 25)

plt.tight_layout()
plt.savefig(path_save + "Ensemble_MSD.pdf",  bbox_inches = "tight")
plt.show()


