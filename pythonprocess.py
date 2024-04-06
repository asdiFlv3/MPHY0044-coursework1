# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 00:45:41 2023

@author: admin
"""

import matplotlib.pyplot as plt
from skimage import io, color, filters, measure, morphology
from skimage.color import label2rgb
import numpy as np

def analyze_microscope_image(image_path, tolerance, na):
    #read the image
    image = io.imread(image_path)
    
    #denoise image
    
    #grayscale+blurr to denoise
    gray_image = color.rgb2gray(image)
    blurred_image = filters.gaussian(gray_image, sigma= 1)

    #plot a graylevel historgram to obtain suitable tolerance
    histogram, bin_edges = np.histogram(blurred_image, bins=256, range=(0.0, 1.0))
    plt.plot(bin_edges[0:-1], histogram)
    plt.title("Graylevel histogram")
    plt.xlabel("gray value")
    plt.ylabel("pixel count")
    plt.xlim(0, 1.0)
    plt.xticks(np.arange(0,1,0.1))
    plt.show()
    plt.imshow(gray_image)
    plt.imshow(blurred_image, cmap='gray')

    tol=tolerance

    #convert into binary filtered image
    binary_mask = blurred_image <tol

    fig, ax = plt.subplots()
    plt.imshow(binary_mask, cmap='gray')
    
    my_x_ticks = np.arange(0,300,10)#set unit length on x axis
    plt.xticks(my_x_ticks)
    
    plt.show()

    labeled_image, count = measure.label(binary_mask, connectivity=2, return_num=True)

    io.imshow(labeled_image)

    coloured_labeled_image = color.label2rgb(labeled_image, bg_label=0)

    #find object size
    properties = measure.regionprops(labeled_image)
    object_sizes = [prop.area for prop in properties]

    # find the image size
    from PIL import Image
     
    img = Image.open(image_path)
    w = img.width       #图片的宽
    h = img.height      #图片的高
    imgSize = w*h
    
    # Count and measure size of objects
    properties = measure.regionprops(labeled_image)
    object_sizes = [prop.area for prop in properties]
    
    #Calculate theoretical resolution with Rayleigh's criterion
    lamb=5.5e-7
    r_theo=1.22*lamb/(2*na)

    #show the created image in the viewer and number of objects counted
    io.imshow(coloured_labeled_image)
    print("dtype:", labeled_image.dtype)
    print("min:", np.min(labeled_image))
    print("max:", np.max(labeled_image))
    print('object size:',object_sizes)
    print('image size:', imgSize)  
    print('theoretical resolution:',r_theo)

image_path = "humanblood_4x_mag.jpg" #adjust with evry image
# Adjust t value based on graylevel curve to denoise unnessecary object
tolerance = 0.47
# Adjust na value with different objectives
na=0.1

analyze_microscope_image(image_path, tolerance, na)

