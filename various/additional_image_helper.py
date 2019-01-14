from __future__ import print_function
import os, sys
import numpy as np
import cv2
import glob
import getopt
import matplotlib as mpl
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
from scipy.spatial import distance

#------------------------------------------------------------------------------
def adjust_gamma(image, gamma):
	# build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

#-------------------------------------------------------------------------------
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #cv2.circle(rot_img,(x,y),5,(255,0,0),-1)
        cv2.circle(img,(x,y),5,(255,0,0),-1)
        ix,iy = x,y
#-------------------------------------------------------------------------------
def get_rgb(image, x, y):
    [r,g,b] = image[x,y]
    '''
    r /= 255.0
    g /= 255.0
    b /= 255.0
    '''
    return([r,g,b])
#-------------------------------------------------------------------------------
def rename(directory, imagename, imagetype, offset):
    #renames the files in a directory
    '''
    directory = "/home/mrbohlen/data/fakebedrooms/"
    #make sure the directory exists and files are in it
    imagetype = ".jpg" or ".png"
    name = "image"
    offset = 0                  # 0 to start on epoch 0, n after n images
    '''
    files = filter(os.path.isfile, glob.glob(directory + "*"))
    files = list(files)             #for python3
    files.sort(key=lambda x: os.path.getmtime(x))

    for i in range (0, len(files)):
        print (i, files[i])
        newname = directory + imagename + str(i+offset) + imagetype
        os.rename(files[i], newname)
#-------------------------------------------------------------------------------
def renumber(directory, imagetype):
    #python2 only...
    files = filter(os.path.isfile, glob.glob(directory + "*"))
    #files = list(files)             #for python3
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    print(files)

    for i in range (0, len(files)):
        print (i, files[i])
        newname = directory + str(i) + imagetype
        os.rename(files[i], newname)
#-------------------------------------------------------------------------------
def get_date_created(imagename):
    return Image.open(imagename)._getexif()[36867]

#-------------------------------------------------------------------------------
