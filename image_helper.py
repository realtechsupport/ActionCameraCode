#!/usr/bin/env python
#image_helper.py (python3)
#general single image processing routines
#ART 350
#jan - april 2019
#author: realtechsupport
#------------------------------------------------------------------------------
from __future__ import print_function
import os, sys
from os import environ, path
import numpy as np
import cv2
import glob
import getopt
import matplotlib as mpl
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import subprocess
import psutil
import signal, wave
import contextlib
import feedparser
import random
import pytesseract

#------------------------------------------------------------------------------

def convert2rgb(input_image):
    output_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    return(output_image)

#-------------------------------------------------------------------------------

def shift_image(image, xshift, yshift):
    h,w,d = image.shape
    M = np.float32([[1,0,xshift],[0,1,yshift]])
    #hird argument of the cv2.warpAffine() is the size of the output image,
    #which should be in the form of (width, height)
    #width = number of columns, and height = number of rows
    shifted_image = cv2.warpAffine(image,M,(w,h))
    return(shifted_image)

#-------------------------------------------------------------------------------

def overlay(image1, v1, image2, v2, v3):
#image1 and image2 must have same dimensions
#v1 and v2 are weights (for each of the images) and must add to 1.0; v3 usually 0
    background = cv2.imread(image1)
    overlay = cv2.imread(image2)
    result = cv2.addWeighted(background, v1, overlay, v2, v3)
    return(result)
#-------------------------------------------------------------------------------

def create_image(height, width, channels, color):
    blank_image = np.zeros((height,width,channels), np.uint8)
    blank_image[:] = color
    return(blank_image)
#------------------------------------------------------------------------------

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

#-------------------------------------------------------------------------------

def adjust_gamma(image, gamma):
	# build a lookup table mapping the pixel values [0, 255] to adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

#-------------------------------------------------------------------------------

def crop_image(image, xmin, xmax, ymin, ymax):
    cropped = image[ymin:ymax, xmin:xmax]
    return(cropped)

#-------------------------------------------------------------------------------

def get_rgb(image, x, y):
    [r,g,b] = image[x,y]
    #r /= 255.0; g /= 255.0; b /= 255.0
    return([r,g,b])

#-------------------------------------------------------------------------------

def get_date_created(imagename):
    return Image.open(imagename)._getexif()[36867]

#-------------------------------------------------------------------------------

def adjust_brightness(input_image, inpath):
    all_v=[]; all_v_median=0;
    filename = "ave_brightness.txt"
    try:
        all_v_median = int(readfromfile(filename))
        print("got the info from the stored file: ", all_v_median)
    except:
        print("...reading all images in the inputpath...this will take a moment....")
        for imagename in os.listdir(inpath):
            img = cv2.imread(inpath + imagename)
            if img is None:
                print("Failed to load")
            else:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert it to hsv
                h, s, v = cv2.split(hsv)
                all_v.append(v)

        #simple test version #all_v_mean = int(np.mean(all_v))
        all_v_median = int(np.median(all_v))
        store_avebrighness(all_v_median, filename)
    #----------------------------------------
    # now adjust the given image
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    median_v = int(np.median(v))
    #dif_v = mean_v - all_v_mean            #ratio_v = (mean_v / all_v_mean)
    ratio_v = (median_v / all_v_median)     #ratio_v2 = ratio_v * ratio_v
    rounded_ratio = np.round(ratio_v, decimals=3)
    gamma_fix = np.round((1 / rounded_ratio), decimals=3)
    if (gamma_fix > 2):
        gamma_fix = 2.0
    elif(gamma_fix < 0.5):
        gamma_fix = 0.5
    else:
        pass
    print("all images median brighness, this image brightness, gamma_fix: ", all_v_median, median_v,  gamma_fix)
    adjusted_img = adjust_gamma(input_image, gamma=gamma_fix)
    #norm_img = cv2.normalize(img, dst=None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return(adjusted_img)

#-------------------------------------------------------------------------------

def addtext_to_image(datapath, fontpath, imagename, message, fontchoice, fontsize, color, x, y):
	im = Image.open(datapath+imagename)
	width, height = im.size
	font = ImageFont.truetype(fontpath+fontchoice, fontsize)
	draw = ImageDraw.Draw(im)
	draw.text((x*width, y*height), message, font=font, fill=color)
	imcv = np.array(im)
	imcv_rgb = cv2.cvtColor(imcv, cv2.COLOR_BGR2RGB)
	return(imcv_rgb)

#-------------------------------------------------------------------------------

def recognize_text(datapath, imagename, configuration, filter):
    temp = 'temp.jpg'
    image = cv2.imread(datapath+imagename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if(filter):
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        gray = cv2.medianBlur(gray, 3)

    cv2.imwrite(temp, gray)
    text = pytesseract.image_to_string(Image.open(temp), config=configuration)
    os.remove(temp)
    return(text)

#------------------------------------------------------------------------------
