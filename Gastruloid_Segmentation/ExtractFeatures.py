#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
#                                                                            #
##############################################################################

import tifffile as tif
from skimage.measure import regionprops
import pandas as pd
from skimage.measure import marching_cubes, mesh_surface_area
import numpy as np
import os
from math import sqrt


path_save = "/ExampleData/Output/"

path_data = "/ExampleData/Gastruloid/42h/"
positions = ["Position 2"]


prop_list = ["label","area", "major_axis_length", "solidity", "max_intensity", "mean_intensity", "min_intensity"]

def axis_minor_length_fixed(labeled_obj):
    if labeled_obj._ndim == 2:
        l2 = labeled_obj.inertia_tensor_eigvals[-1]
        return 4 * sqrt(l2)
    elif labeled_obj._ndim == 3:
        # equivalent to _inertia_eigvals_to_axes_lengths_3D(ev)[-1]
        ev = labeled_obj.inertia_tensor_eigvals
        try:
            return sqrt(10 * (-ev[0] + ev[1] + ev[2]))
        except ValueError:
            return 0
    else:
        raise ValueError("axis_minor_length only available in 2D and 3D")



df_lck = pd.DataFrame()

for pos in positions:
    path_raw_data = os.path.join(path_data,pos,"Stack")
    path_seg_data = os.path.join(path_save,"Masks")


    # generating file list
    file_list = sorted(os.listdir(path_raw_data))
    file_list_Lck = []
    for ele in file_list:
        if "Lck" in ele:
            file_list_Lck.append(ele)
    
    file_list_masks = []
    for ele in file_list_Lck:
        name = ele.replace(".tif", "_cp_masks.tif")
        file_list_masks.append(name)
    
    for i in range(len(file_list_Lck)):
        
        raw_data = tif.imread(os.path.join(path_raw_data,file_list_Lck[i]))
        seg_data = tif.imread(os.path.join(path_seg_data,file_list_masks[i]))

        tmp_dic = {}
        for prop in regionprops(seg_data, raw_data, spacing = (2.463,1,1)):

            tmp_dic.update({p: prop[p] for p in prop_list})
            tmp_dic.update({"minor_axis_length": axis_minor_length_fixed(prop)})
        
            mem_features = pd.DataFrame(tmp_dic, index = [0])
            df_lck = pd.concat([df_lck, mem_features], axis = 0)

df_lck.to_csv(path_save + "df_gastruloid.csv")