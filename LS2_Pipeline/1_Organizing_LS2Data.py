#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
#                                                                            #
##############################################################################


import os


path_data = "/ExampleData/Organoid/"
positions = ["Position 1"]

folders_create = ["View1","View2","View2Reg","Fusion"]

for pos in positions:
    path_pos = path_data + pos + "/"
    for folder in folders_create:
        path_newfolder = path_pos + folder + "/" 
        if not os.path.isdir(path_newfolder):
            os.makedirs(path_newfolder)
    path_cropped = path_pos + "/cropped/"
    for file in os.listdir(path_cropped):
        if "View1" in file:
            print(path_pos + folders_create[0] + "/" + file)
            os.rename(path_cropped + file, path_pos + folders_create[0] + "/" + file)
        if "View2" in file:
            print(path_pos + folders_create[1] + "/" + file)
            os.rename(path_cropped + file, path_pos + folders_create[1] + "/" + file)            
            
