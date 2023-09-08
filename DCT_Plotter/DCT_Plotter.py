#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
# Author: Petr Strnad                 <petr.strnad@viventis-microscopy.com>  #
# Author: Camille Remy                                                       #
#                                                                            #
##############################################################################

import numpy
from scipy import fftpack
import tifffile as tif
import os
import matplotlib.pyplot as plt


def rebin(array, binning_factor):
    shape = numpy.shape(array)
    binning_factor = int(binning_factor)

    new_shape = (int(shape[0]//binning_factor), int(shape[1]//binning_factor))
    leftover = (int(shape[0]%binning_factor), int(shape[1]%binning_factor))
    if leftover[0] != 0 or leftover[1] != 0:
        #print("Yes")
        array = array[0 : -leftover[0], 0 : -leftover[1]]
     
    shape = (new_shape[0], binning_factor, new_shape[1], binning_factor)
    return array.reshape(shape).mean(-1).mean(1)

"""
Image sharpness metric based on entropy of Discret Cosine Transform.

Parameters
----------
image : ndarray
    2 dimensional array containing image.
pixel_size : float
    pixel size of the microscope.

Returns
-------
float
    Sharpness mesure of the image.
"""


NA = 0.8
wavelength = 0.610
pixel_size = 0.406
reality_factor = 1.5 
r_psf = reality_factor*(0.61*wavelength/NA)


path_data = "/ExampleData/DCT/"
path_save = "/ExampleData/Output/"

dct_1 = []
dct_2 = []
dct_f = []

for stack in os.listdir(path_data):
    view1 = os.path.join(path_data, stack)
    stack_img_1 = tif.imread(view1)
    plot_save = stack.replace(".tif", ".png")
    plot_save = os.path.join(path_save, plot_save)

     
    dims = stack_img_1.shape
    
    y_dim = dims[1]
    x_dim = dims[2]
    
    if y_dim > x_dim:
        y_mid = round(y_dim / 2)
        y_pm = round(x_dim / 2)
        if y_pm % 2 == 1:
            y_upper = y_mid + y_pm - 1
        else:
            y_upper = y_mid + y_pm
        y_lower = y_mid - y_pm
        
        if y_upper-y_lower > x_dim:
            y_upper = y_upper - 1
        if y_upper -y_lower < x_dim:
            y_upper = y_upper + 1
        
        
        stack_img_1_calc = stack_img_1[0:dims[0],y_lower:y_upper, 0:x_dim]
    
        
    if x_dim > y_dim:
        x_mid = round(x_dim / 2)
        x_pm = round(y_dim / 2)
        if x_pm % 2 == 1:
            x_upper = x_mid + x_pm - 1
        else:
            x_upper = x_mid + x_pm
        x_lower = x_mid - x_pm
        
        if x_upper-x_lower > y_dim:
            x_upper = x_upper - 1
        if x_upper -x_lower < y_dim:
            x_upper = x_upper + 1
        
        stack_img_1_calc = stack_img_1[0:dims[0],0:y_dim,x_lower:x_upper]
    
    if x_dim == y_dim:
        stack_img_1_calc = stack_img_1
    
    
    for frame in range(dims[0]):  

        stopper = 1
        r_psf_pxl = r_psf/pixel_size
        bin_factor = r_psf_pxl//0.5
        r_psf_pxl_bin = r_psf_pxl / bin_factor
        
        binned_image = rebin(stack_img_1_calc[frame], bin_factor)
        width, _ = numpy.shape(binned_image)
    
        Fc = fftpack.dct(fftpack.dct(binned_image.T, norm='ortho').T, norm='ortho')
        
        L2 = 0
        for x in range(width):
            for y in range(width):
                if x+y < int(width/r_psf_pxl_bin):
                    L2 += Fc[x,y]**2
        L2 = numpy.sqrt(L2)
        FL = Fc/L2
        DCTentr = -(2/(width/r_psf_pxl_bin)**2)*numpy.sum(numpy.abs(FL)*(numpy.log2(numpy.abs(FL))))
        if "View1" in stack:
            dct_1.append(DCTentr)
        if "View2" in stack:
            dct_2.append(DCTentr)
        if "Fused" in stack:
            dct_f.append(DCTentr)
             
            


dct_1 = numpy.asarray(dct_1)
dct_1 = dct_1 * 1000
dct_2 = numpy.asarray(dct_2)
dct_2 = dct_2 * 1000
dct_f = numpy.asarray(dct_f)
dct_f = dct_f * 1000

x = []
for i in range(len(dct_1)):
    x.append(i*2)



fig = plt.figure(figsize=(8,7))                                                               
ax = fig.add_subplot(1,1,1)  
plt.plot(x,dct_1, linewidth = 4, color = "black", label = "View 1")
ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
for label in ticklabels:
    label.set_fontsize(30)

plt.xlabel(r"Z Section [$\mu$m]", fontsize = 30)
plt.ylabel(r"DCT Score [$\cdot10^3$]", fontsize = 30)
plt.tight_layout()
plt.savefig(path_save + "DCT_View1.pdf", bbox_inches = "tight")
plt.show()
plt.close()

fig = plt.figure(figsize=(8,7))                                                               
ax = fig.add_subplot(1,1,1)  
plt.plot(x,dct_2, linewidth = 4, color = "black", label = "View 2")
ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
for label in ticklabels:
    label.set_fontsize(30)

plt.xlabel(r"Z Section [$\mu$m]", fontsize = 30)
plt.ylabel(r"DCT Score [$\cdot10^3$]", fontsize = 30)
plt.tight_layout()
plt.savefig(path_save + "DCT_View2.pdf", bbox_inches = "tight")
plt.show()
plt.close()
    
fig = plt.figure(figsize=(8,7))                                                               
ax = fig.add_subplot(1,1,1)  
plt.plot(x,dct_f, linewidth = 4, color = "black", label = "Fused")
ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
for label in ticklabels:
    label.set_fontsize(30)

plt.xlabel(r"Z Section [$\mu$m]", fontsize = 30)
plt.ylabel(r"DCT Score [$\cdot10^3$]", fontsize = 30)
plt.tight_layout()
plt.savefig(path_save + "DCT_Fused.pdf", bbox_inches = "tight")
plt.show()
plt.close()



