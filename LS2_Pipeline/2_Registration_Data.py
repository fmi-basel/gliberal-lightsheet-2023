#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
#                                                                            #
##############################################################################


from dipy.align.imaffine import (transform_centers_of_mass,
                                 AffineMap,
                                 MutualInformationMetric,
                                 AffineRegistration)

from dipy.align.transforms import (TranslationTransform3D,
                                   RigidTransform3D,
                                   AffineTransform3D)

import tifffile as tif
import numpy as np
import os
import concurrent.futures
import sys


# Specify one stack of View1 and View2 to calculate the registration matrix
view1 = "/path/to/View1/View1.tif"
view2 = "/path/to/View2/View2.tif"


path_data = "path/to/data/"
positions = ["Position 1","Position 2"]


static = tif.imread(view1)
moving = tif.imread(view2)


nbins = 32
sampling_prop = None


level_iters = [10, 5, 4]
sigmas = [10.0,5.0,0.0]
factors = [20, 10, 2]
metric = MutualInformationMetric(nbins, sampling_prop)
params0 = None

identity = np.eye(4)

affreg = AffineRegistration(metric=metric,
                            level_iters=level_iters,
                            sigmas=sigmas,
                            factors=factors)

transform = TranslationTransform3D()


translation = affreg.optimize(static, moving, transform, params0,
                              identity, identity)
xformed_img = translation.transform(moving)

transform = RigidTransform3D()
starting_affine = translation.affine
rigid = affreg.optimize(static, moving, transform, params0,
                        identity, identity,
                        starting_affine=starting_affine)

xformed_img = rigid.transform(moving)


def regsave(path_pos_view2,file,path_pos_view2_save):
        to_transform = tif.imread(path_pos_view2 + file)
        xformed_img = rigid.transform(to_transform)
        xformed_img = xformed_img.astype("uint16")
        tif.imwrite(path_pos_view2_save + file, xformed_img)
    
        
with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
    futures = []
    for pos in positions:
        print(pos)
        path_pos_view2 = path_data + pos + "/View2/"
        path_pos_view2_save = path_data + pos + "/View2Reg/"
        for file in os.listdir(path_pos_view2):
            e = executor.submit(regsave, path_pos_view2, file, path_pos_view2_save)
            futures.append(e)
    for f in futures:
        f.result()  

   