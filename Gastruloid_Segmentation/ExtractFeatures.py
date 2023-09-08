#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
#                                                                            #
##############################################################################

import tifffile as tif
from skimage.measure import regionprops_table
import pandas as pd
from skimage.measure import marching_cubes, mesh_surface_area
import numpy as np
import os


path_save = "/ExampleData/Output/"

path_data = "/ExampleData/Gastruloid/42h/"
positions = ["Position 2"]



def surface_area_marchingcube(regionmask):
    regionmask_int = regionmask.astype(np.uint16)
    regionmask_int=np.pad(regionmask_int, 1, 'constant')
    verts, faces, normals, values = marching_cubes(regionmask_int, spacing=(2.463,1,1))
    surface_area = mesh_surface_area(verts, faces)
    return surface_area


for pos in positions:
    path_raw_data = os.path.join(path_data,pos,"Stack")
    path_seg_data = "/ExampleData/Output/Masks/"  

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
        
        
        mem_features = regionprops_table(seg_data, raw_data, spacing = (2.463,1,1), properties = ["label","area", "major_axis_length", "minor_axis_length", "solidity", "max_intensity", "mean_intensity", "min_intensity"], extra_properties=[surface_area_marchingcube])
        mem_features = pd.DataFrame(mem_features)
        
        if "df_lck" not in locals():
            df_lck = pd.DataFrame(mem_features)
        else:
            df_lck = pd.concat([df_lck, mem_features], axis = 0)
        
df_lck.to_csv(path_save + "df_gastruloid.csv")