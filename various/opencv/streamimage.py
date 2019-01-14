#! /usr/bin/env python

# mediaroboticsII - getting started with opencv on python under ubuntu (7.04)
# streamimage.py
# continuously grab an image from a ieee1394 IIIDC compliant firewire camera and display result to the screen
# ---------------------------------------------------------
# minimum required imports
import sys
from opencv.cv import *
from opencv.highgui import *

if __name__ == '__main__':

    print "OpenCV Python testing simple image capture"
    print "OpenCV version: %s" % (CV_VERSION)

    # create  windows
    cvNamedWindow ('Camera', CV_WINDOW_AUTOSIZE)
    # move the new window
    cvMoveWindow ('Camera', 10, 40)

    # no device number on the command line, assume we want the 1st device
    device = 0

    if len (sys.argv) == 1:
        # no argument on the command line, try to use the camera
        capture = cvCreateCameraCapture (device)
        # set the image size from the camera
        cvSetCaptureProperty (capture, CV_CAP_PROP_FRAME_WIDTH, 640)
        cvSetCaptureProperty (capture, CV_CAP_PROP_FRAME_HEIGHT, 480)
    else:
        # we have an argument on the command line, we can assume this is a file name, so open it
        capture = cvCreateFileCapture (sys.argv [1])

    # check that capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit (1)

    while 1:
        # 1. capture the current image
        frame = cvQueryFrame (capture)
        if frame is None:
            # no image captured... end the processing
            break
        # mirror the captured image and show it
        cvFlip (frame, None, 1)
	cvShowImage ('Camera', frame)
        # handle events
        k = cvWaitKey (10)
        if k == '\x1b':
            # user has press the ESC key, so exit
            break
