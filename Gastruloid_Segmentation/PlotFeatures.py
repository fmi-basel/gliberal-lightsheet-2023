#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
#                                                                            #
##############################################################################


import pandas as pd
import matplotlib.pylab as plt
import seaborn as sb


path_csv = "/path/to/data/"
path_save = "/path/save/plots/"



df_lck_42 = pd.read_csv(path_csv + "df_lck_42.csv")
df_lck_66 = pd.read_csv(path_csv + "df_lck_66.csv")
df_lck_90 = pd.read_csv(path_csv + "df_lck_90.csv")


df_area_42 = df_lck_42
df_area_66 = df_lck_66
df_area_90 = df_lck_90


df_area_42["area"] = df_area_42["area"].apply(lambda x: x*(0.406*0.406*1))
df_area_66["area"] = df_area_66["area"].apply(lambda x: x*(0.406*0.406*1))
df_area_90["area"] = df_area_90["area"].apply(lambda x: x*(0.406*0.406*1))


df_area_big_42 = df_area_42[(df_area_42["area"]<20000) & (df_area_42["area"]>3000)]
df_area_big_66 = df_area_66[(df_area_66["area"]<20000) & (df_area_66["area"]>3000)]
df_area_big_90 = df_area_90[(df_area_90["area"]<20000) & (df_area_90["area"]>3000)]

df_area_big_42 = df_area_big_42[(df_area_big_42["minor_axis_length"]>0.1) & (df_area_big_42["major_axis_length"]<150)]
df_area_big_66 = df_area_big_66[(df_area_big_66["minor_axis_length"]>0.1) & (df_area_big_66["major_axis_length"]<150)]
df_area_big_90 = df_area_big_90[(df_area_big_90["minor_axis_length"]>0.1) & (df_area_big_90["major_axis_length"]<150)]


major_big_42 = df_area_big_42["major_axis_length"].values
major_big_66 = df_area_big_66["major_axis_length"].values
major_big_90 = df_area_big_90["major_axis_length"].values

minor_big_42 = df_area_big_42["minor_axis_length"].values
minor_big_66 = df_area_big_66["minor_axis_length"].values
minor_big_90 = df_area_big_90["minor_axis_length"].values



mm_big_42 = major_big_42/minor_big_42
mm_big_66 = major_big_66/minor_big_66
mm_big_90 = major_big_90/minor_big_90



fig = plt.figure(figsize=(7,5))                                                               
ax = fig.add_subplot(1,1,1) 
sb.violinplot(data = [mm_big_42,mm_big_66,mm_big_90], inner="quartile", palette=["#d81b60","#1e88e5","#aee64a"])
x = [0,1,2]
my_xticks = ['42h','66h','90h']
plt.xticks(x, my_xticks, fontsize = 25)
plt.ylabel("Major/Minor-Axis", fontsize = 25)
ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
for labelss in ticklabels:
    labelss.set_fontsize(25)

plt.tight_layout()
plt.savefig(path_save + "Major_Minor_Violin.pdf", bbox_inches = "tight")
plt.show()
plt.close()
