#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
#                                                                            #
##############################################################################

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib.colors
import matplotlib as mpl


path_data = "/ExampleData/Organoid/MastodonTable-Spot.csv"
path_save =  "/ExampleData/Output/Intensity_over_time.pdf"


df_fucci = pd.read_csv(path_data, skiprows=[1,2], encoding= 'unicode_escape')

track_ids = df_fucci["Spot track ID"].unique()
frames = df_fucci["Spot frame"].unique()
frames = sorted(frames)
max_f = max(frames)/6


df_fucci["norm_vec"] = np.nan


track_ids = [5,24,13]

norm = mpl.colors.Normalize(vmin = 0, vmax = 1)
colors = [mpl.cm.Blues(norm(i)) for i in np.linspace(0.2, 1, len(track_ids))]


fig = plt.figure(figsize = (10,6))
ax = fig.add_subplot(1,1,1)

first_tp = []
lifetime =[]

for idx,ids in enumerate(track_ids):
    sub_df = df_fucci.loc[df_fucci["Spot track ID"] == ids]
    frames = sub_df["Spot frame"].unique()
    frames = sorted(frames)

    ch_0 = []
    ch_1 = []
    
    
    for tp in frames:
        
        tp_1 = sub_df.loc[sub_df["Spot frame"] == tp] 
        ch_0.append(tp_1["Spot intensity"].values[0])
        ch_1.append(tp_1["Spot intensity.6"].values[0])   

    frames = np.asarray(frames)
    frames = (frames*10)/60
    lifetime.append(len(frames)*(1/6))
    first_tp.append(frames[0])
    plt.plot(frames, ch_1, label = str(ids), color = colors[idx])


plt.ylabel("Mean Intensity [a.u.]", fontsize = 20) 
plt.xlabel(r"Time [h]", fontsize = 20)
ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
for labelss in ticklabels:
    labelss.set_fontsize(20)
plt.tight_layout()
plt.savefig(path_save, bbox_inches = "tight")
plt.show()
plt.close()
