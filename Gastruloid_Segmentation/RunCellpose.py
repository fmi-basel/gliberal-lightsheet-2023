#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
#                                                                            #
##############################################################################

from cellpose import models, io
import os


def do_cellpose(datapath, savepath):
    # generating file list
    file_list = sorted(os.listdir(datapath))
    file_list_Lck = []
    for ele in file_list:
        if "Lck" in ele:
            file_list_Lck.append(ele)

    # generating masks
    for file in file_list_Lck:
        print(file)
        img_3D = io.imread(os.path.join(datapath,file))
        masks_stitched, flows_stitched, styles_stitched = model.eval(img_3D, channels = [0,0], diameter=28, flow_threshold=0.4, cellprob_threshold = 0.0, do_3D=False, stitch_threshold=0.5)
        io.save_masks(img_3D, masks_stitched, flows_stitched, savedir = savepath, file_names = file, tif = True)
            
    

path_data = "/ExampleData/Gastruloid/42h/"
positions = ["Position 2"]


path_model = "/ExampleData/Gastruloid/Lck_membrane_42h66h90h"
model = models.CellposeModel(gpu=True, pretrained_model = path_model)


for pos in positions:
    path_pos_data = os.path.join(path_data,pos,"Stack")
    path_pos_save = "/ExampleData/Output/Masks/"   
    do_cellpose(path_pos_data, path_pos_save)
