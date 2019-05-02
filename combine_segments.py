from image_helper import *
from av_helper_v6 import *
#ART350
#combine multiple sections to one video
#extract_combine_video.py
#realtechsupport, april 2019
#-------------------------------------------------------------------------------
datapath = '/home/apath/data/'
#-------------------------------------------------------------------------------
#list the segments you created with extract_proccess_make
v1 = 'video_1_4_blur.mp4'
v2 = 'video_1_4_color.mp4'
v3 = 'video_1_4_grayscale.mp4'
v4 = 'video_1_4_edgedetect.mp4'

#specify your combination sequence
sequence = [v1,v2,v3,v4,v1,v2,v3,v4,v1]
combine_segments_v2(datapath, sequence)
#-------------------------------------------------------------------------------
