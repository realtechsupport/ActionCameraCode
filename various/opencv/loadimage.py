#! /usr/bin/env python
# mediaroboticsII - getting started with opencv on python under ubuntu (7.04)
# loadimage.py
# load an image from disk and display on screen
# ---------------------------------------------------------
# minimum required imports
import sys
from opencv.cv import *
from opencv.highgui import *

# which version are we running?
print "OpenCV Python testing simple test"
print "OpenCV version: %s" % (CV_VERSION)

#create a window
cvNamedWindow ('test', CV_WINDOW_AUTOSIZE)

#load an image
img = cvLoadImage("images/purple.jpg", 1)

#make sure you found the image; give a warning otherwise
if(img):
	print "found image"
else:
	print "cant get image"

#show the image
cvShowImage ('test', img)

#wait for a key
cvWaitKey(0)


