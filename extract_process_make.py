#!/usr/bin/env python
#extract_process_make.py
#(python3)
#extract segments of a video
#manipulate the video data
#speed up - slow slowdown - reverse timeline
#add text, color etc
#overlay two different video streams
#process to a single video

#realtechsupport april 2019
#-------------------------------------------------------------------------------
from av_helper import *
#-------------------------------------------------------------------------------
datapath = '/home/apath/data/'
videofile = 'v1.mp4'
duration = get_video_length(datapath+videofile)
d = hms_to_seconds(duration)
#-------------------------------------------------------------------------------
#select two times (in seconds; both less than the duration of the video, end > start)
start = 1; end = 4
#-------------------------------------------------------------------------------
time_s = time.strftime("%H:%M:%S", time.gmtime(start))
time_e = time.strftime("%H:%M:%S", time.gmtime(end))
info = videofile.split('.')
segmentname = info[0] + '_' + str(start) + '_' + str(end) + '.' + info[1]
t1 = 'temp/'
t2 = 'temp2/'
tpath1 = datapath+t1
tpath2 = datapath+t2
#-------------------------------------------------------------------------------
#set these flags to activate the individual sections below
#example A: pick a section from a video and convert all images to grayscale
#CLEAN=1; EXTRACT=1; PROCCESS_single_segment=1; OVERLAY_two_segments=0; MAKEVIDEO=1
# and uncomment: type = process_images_grayscale (tpath1, datapath)

#example B: overlay two previously created video segments
#CLEAN=0; EXTRACT=0; PROCCESS_single_segment=0; OVERLAY_two_segments=1; MAKEVIDEO=1
#------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
CLEAN=0
EXTRACT=0
PROCCESS_single_segment=0
OVERLAY_two_segments=1
MAKEVIDEO=1
#------------------------------------------------------------------------------
if(CLEAN):
    tempok = os.path.isdir(tpath1)
    if(tempok):
        shutil.rmtree(tpath1)
    tempok = os.path.isdir(tpath2)
    if(tempok):
        shutil.rmtree(tpath2)

if(EXTRACT):
    if(start > end):
        print('start should be smaller than end')
        start = 0
    if(d < end):
        print('end exceeds duration!')
        end = d

    extract_segment(datapath, videofile, time_s, time_e, segmentname)
    framerate1 = get_fps(datapath+videofile)
    print('\n', framerate1, '\n')
    create_images_from_video(datapath, t1, segmentname, framerate1)

if(PROCCESS_single_segment):
    #change these values
    kernel = (11,11)
    fontchoice = "verdana.ttf"
    fontpath =  datapath
    sigma = 0.33
    fontsize = 70
    space = 25
    text = ' not on my watch '
    kernel = (11,11)
    dw = 0.25
    dh = 0.4
    color = (0, 0, 0)
    tcolor = (255,255,255)
    img_contrib = 0.3
    backimg_contrib = 1 - img_contrib
    #type = process_images_blur (tpath1, datapath, kernel)
    #type = process_images_addtext (tpath1, datapath, fontpath, text, fontchoice, fontsize, dw, dh, space, tcolor)
    #type = process_images_coloroverlay (tpath1, datapath, color, img_contrib, backimg_contrib)
    #type = process_images_edgedetect (tpath1, datapath, sigma)
    type = process_images_grayscale (tpath1, datapath)
    #for this choice - set all flags to ZERO except 'Process_single_segment' --------------------------------------
    height = 1080; width = 1920; duration = 3
    text = ' temporary autonomous zone '
    transition = 'transition.mp4'
    #type = create_video_from_singlecolorimage_withtext(datapath, height, width, duration, color, transition, text, fontpath, fontchoice, fontsize, dw, dh, space, tcolor)

if(OVERLAY_two_segments):
    #set switches above to zero except:OVERLAY_two_segments=1  and MAKEVIDEO=1
    #assumes you alread extracted these two segments with process single segment
    #resulting segment will be the size of the smaller of the two inputs if not equal
    #input video segments must have the same resolution !
    segment1 = 'v1_1_4_blur.mp4'
    segment2 = 'v1_1_4_edgedetect.mp4'
    seg1_contrib = 0.3
    seg2_contrib = 1 - seg1_contrib
    type = process_images_videooverlay(datapath, t1, t2, segment1, segment2, seg1_contrib, seg2_contrib)

if(MAKEVIDEO):
    # factor less than one: slowdown...greater than one: speedier
    factor = 1.0
    reverse = False
    framerate1 = 30
    framerate2 = int(framerate1*factor)
    if(OVERLAY_two_segments == True):
        output = segment1.split('.')[0] + '_' + segment2.split('.')[0] + '_' + type  +'.mp4'
    else:
        output = segmentname.split('.')[0] + '_' + type +'.mp4'

    create_video_from_images(datapath, tpath1, framerate2, reverse, output)

#-------------------------------------------------------------------------------
