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
    path_pos = os.path.join(path_data,pos)
    for folder in folders_create:
        path_newfolder = os.path.join(path_pos,folder)
        if not os.path.isdir(path_newfolder):
            os.makedirs(path_newfolder)
    path_cropped = os.path.join(path_pos,"cropped")
    for file in os.listdir(path_cropped):
        if "View1" in file:
            old_place = os.path.join(path_cropped,file)
            new_place = os.path.join(path_pos,folders_create[0],file)
            print(new_place)
            os.rename(old_place, new_place)

        if "View2" in file:
            old_place = os.path.join(path_cropped,file)
            new_place = os.path.join(path_pos,folders_create[1],file)
            print(new_place)
            os.rename(old_place, new_place)