#!/usr/bin/env python3
# Copyright (C) 2023 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Franziska Moos              <franziska.moos@fmi.ch>                #
# Author: Petr Strnad                 <petr.strnad@viventis-microscopy.com>  #
# Author: Camille Remy                                                       #
#                                                                            #
##############################################################################

# Fuse views
import os
from scipy import fftpack
import numpy
import tifffile
from scipy.signal import medfilt
import concurrent.futures


physical_size_x = 0.406
crop = 150
crop_pixels = int(crop/physical_size_x)
sig_width = 20
view_change_index = 70

int_factor = 1.3
emisson_wavelength = 0.610


path_data = "/ExampleData/Organoid/"
positions = ["Position 1"]


cache_mask = None
cache_width = None
cache_height = None
cache_r_psf_pxl = None

def dct_generate_mask(width, heigth, r_psf_pxl):
    global cache_width
    global cache_height
    global cache_mask
    global cache_r_psf_pxl

    if (cache_width == width and cache_height == heigth and cache_r_psf_pxl == r_psf_pxl):
        return cache_mask

    mask = numpy.zeros(shape=(heigth,width))
    for x in range(width):
        for y in range(heigth):
            if x+y < int(width/r_psf_pxl):
                mask[y][x] = True
            else: mask[y][x] = False

    cache_width = width
    cache_height = heigth
    cache_r_psf_pxl = r_psf_pxl
    cache_mask = mask

    return mask

def dct_fast(image, mask, r_psf_pxl, bin_factor):
    image = _rebin(image, bin_factor)
    width,_ = numpy.shape(image)

    Fc = fftpack.dct(fftpack.dct(image.T, norm='ortho').T, norm='ortho')
    Fc_masked = numpy.multiply(Fc**2, mask)
    L2 = numpy.sum(Fc_masked)
    L2 = numpy.sqrt(L2)
    FL = Fc/L2
    
    DCTentr = -(2/(width/r_psf_pxl)**2)*numpy.sum(numpy.abs(FL[FL!=0])*(numpy.log2(numpy.abs(FL[FL!=0]))))

    return DCTentr

def _rebin(array, binning_factor):
    # get dimensions of original array
    shape = numpy.shape(array)
    binning_factor = int(binning_factor)
    
    # create square image if necessary
    if shape[0] != shape[1]:
        min_dim = numpy.amin(shape)
        array = array[0:min_dim, 0:min_dim]

    # get new dimensions of array
    shape = numpy.shape(array)
    
    # get new dimensions and potential left over
    new_shape = (int(shape[0]//binning_factor), int(shape[1]//binning_factor))
    leftover = (int(shape[0]%binning_factor), int(shape[1]%binning_factor))

    # remove leftover(s) at the right end of the array
    if leftover[0] != 0 or leftover[1] != 0:
        array = array[0 : -leftover[0], 0 : -leftover[1]]

    # tupple for reshapping
    shape = (new_shape[0], binning_factor, new_shape[1], binning_factor)
    
    return array.reshape(shape).mean(-1).mean(1)

def get_binned_pixel(pixel_size, wavelength = 0.525):
    # microscope parameters 
    # compute rayleigh radius of the microscope
    NA = 0.8

    #wavelength = 0.525
    reality_factor = 1.5 # degradation of the PSF
    r_psf = reality_factor*(0.61*wavelength/NA)

    # compare to pixel size to determine binning factor
    r_psf_pxl = r_psf/pixel_size
    bin_factor = r_psf_pxl//0.5
    r_psf_pxl_bin = r_psf_pxl / bin_factor

    return r_psf_pxl_bin, bin_factor

def update_parameter(line, to_find, length, new_value):
    size_start = line.find(to_find)
    if size_start != -1:
        size_end = line.find('"', size_start + length)
        if isinstance(new_value,str):
            old_line = line[size_start:size_end]
            new_line = new_value
        else:
            old_line = line[size_start:size_end+1]
            new_line = to_find + str(new_value) + '"'
        line = line.replace(old_line, new_line)
        
    return line

def load_files(file_name_view1, file_name_view2):
    img_view1 = tifffile.imread(file_name_view1)
    img_view2 = tifffile.imread(file_name_view2)
    
    return img_view1, img_view2

def sigmoid(x):
    
    return 1.0 / (1.0 + numpy.exp(-x))

def find_changing_plane(imarray_view1, imarray_view2, crop, mask, pixel, bin_factor):
    depth, hight, width = numpy.shape(imarray_view1)
    startx = width//2-(crop//2)
    starty = hight//2-(crop//2)
    imarray_view1_crop = imarray_view1[0:depth,starty:starty+crop,startx:startx+crop]    
    imarray_view2_crop = imarray_view2[0:depth,starty:starty+crop,startx:startx+crop]

    # score images and write the selected on in the tif file
    view1_scores = []
    view2_scores = []
    for z in range(0, depth, 1):
        DCT_score_view1 = dct_fast(imarray_view1_crop[z], mask, pixel, bin_factor)
        view1_scores.append(DCT_score_view1)
        DCT_score_view2 = dct_fast(imarray_view2_crop[z], mask, pixel, bin_factor)
        view2_scores.append(DCT_score_view2)

    # score curve smoothed median filtering
    view1_scores_hat = medfilt(view1_scores, kernel_size=7)
    view2_scores_hat = medfilt(view2_scores, kernel_size=7)

    # substracting both views scores
    views_scores_subst = numpy.subtract(view1_scores_hat, view2_scores_hat)
    
    # integral starting from left
    views_scores_subst_int = []
    for index in range(0, len(view1_scores), 1):
        views_scores_subst_int.append(sum(views_scores_subst[0:index]))

    # max of the integrated data is the crossing point od the data
    view_change_index = numpy.argmax(views_scores_subst_int) + 1 # indexing starts at 0
    
    return view_change_index, depth
    #return view1_scores, view2_scores, view1_scores_hat, view2_scores_hat, views_scores_subst, views_scores_subst_int, view_change_index  
    
def save_fused_with_sigmoidal(imarray_view1, imarray_view2, view_change_index, path_fused, int_factor, width_sigmoidal = 10):
    imarray_view1 = numpy.asarray(imarray_view1)
    imarray_view2 = numpy.asarray(imarray_view2)
    
    dim_z, dim_y, dim_x = imarray_view1.shape
    
    imarray_view1 = imarray_view1.astype(int)
    imarray_view1 = imarray_view1 - 120
    imarray_view1[imarray_view1<0] = 0
    
    imarray_view2 = imarray_view2.astype(int)
    imarray_view2 = imarray_view2 - 120
    imarray_view2[imarray_view2<0] = 0
    
    imarray_view1 = imarray_view1*int_factor
    
    sigmoid_values = numpy.linspace(-9, 9, width_sigmoidal*2)
    sigmoid_values = sigmoid(sigmoid_values)
    sigmoid_values = numpy.round(sigmoid_values,3)

    sigmoid_array = numpy.concatenate((numpy.zeros(view_change_index),numpy.ones(dim_z - view_change_index)))
    
    sigmoid_array[view_change_index-width_sigmoidal:view_change_index+width_sigmoidal] = sigmoid_values
    
    new_stack = []
    for i in range(dim_z):
        
        if sigmoid_array[i] == numpy.float64(0):
            
            new_stack.append(imarray_view1[i])
        elif sigmoid_array[i] == 1.0:
            
            new_stack.append(imarray_view2[i])
        else:
            new_plane = (sigmoid_array[i]*imarray_view2[i]) + ((1-sigmoid_array[i])*imarray_view1[i])
            new_stack.append(new_plane)
               
    new_stack = numpy.asarray(new_stack)
    new_stack = new_stack.astype("uint16")
    tifffile.imwrite(path_fused,new_stack)
    

def calculate_int_match_factor(file_v1,file_v2):
    view1 = tifffile.imread(file_v1)
    view2 = tifffile.imread(file_v2)
    view1 = numpy.asarray(view1)
    view2 = numpy.asarray(view2)
    mean_2 = numpy.mean(view2)
    mean_1 = numpy.mean(view1)
    int_factor = mean_2 / mean_1
    
    return int_factor

def check_change_index(imarray_view1, imarray_view2, crop, mask, pixel, bin_factor, width_sigmoidal):
    idx, depth = find_changing_plane(imarray_view1, imarray_view2, crop, mask, pixel, bin_factor)
    if idx > width_sigmoidal and idx < depth - width_sigmoidal:
        return idx
    else:
        return None
        
def do_pipeline(file_name_view1, file_name_view2, file_path_fused, int_factor, physical_size_x, crop_pixels, wavelength, width_sigmoidal, view_change_index):
    pixel, bin_factor = get_binned_pixel(physical_size_x, wavelength)
    mask = dct_generate_mask(crop_pixels, crop_pixels, pixel)
    mask = _rebin(mask, bin_factor)
    data_view1, data_view2 = load_files(file_name_view1, file_name_view2)
    
    chg_idx = check_change_index(data_view1, data_view2, crop_pixels, mask, pixel, bin_factor, width_sigmoidal)
    if chg_idx is not None:
        view_change_index = chg_idx
    print(view_change_index)
    
    save_fused_with_sigmoidal(data_view1, data_view2, view_change_index, file_path_fused, int_factor, width_sigmoidal)
    



# Generate mask
with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
    futures = []
    for pos in positions:
        
        #path_pos_view2 = os.path.join(path_data,pos,"View2")
        path_pos_view1 = os.path.join(path_data,pos,"View1")
        path_pos_view2 = os.path.join(path_data,pos,"View2Reg")
        path_save_fused = os.path.join(path_data,pos,"Fusion")
    
        for file_name in os.listdir(path_pos_view2): 
            print(pos + file_name)
            file_name_view1 = file_name.replace("View2", "View1")
            savename_fused = file_name.replace("View2", "Fused")
                        
            file_path_fused = os.path.join(path_save_fused,savename_fused)
            file_path_view1 = os.path.join(path_pos_view1, file_name_view1)
            file_path_view2 = os.path.join(path_pos_view2, file_name)
            file_path_fused = os.path.join(path_save_fused,savename_fused)
            e = executor.submit(do_pipeline, file_path_view1, file_path_view2, file_path_fused, int_factor, physical_size_x, crop_pixels, wavelength = emisson_wavelength, width_sigmoidal = sig_width, view_change_index = view_change_index)
            futures.append(e)
    for f in futures:
        f.result()

