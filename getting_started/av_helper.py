#!/usr/bin/env python
#av_helper.py (python3)
#utilities for audio and video processing
#participatory data practices project
#jan 2019
#author: realtechsupport
#-------------------------------------------------------------------------------
import sys, os, time, datetime
from os import environ, path
import subprocess
import psutil, shutil
import signal, wave
import contextlib
#------------------------------------------------------------------------------
def get_video_length(filename):
    result = subprocess.Popen(["ffprobe", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    return [x for x in result.stdout.readlines() if b'Duration' in x]
#------------------------------------------------------------------------------
def hms_to_seconds(t):
    h, m, s = [float(i) for i in t.split(':')]
    return 3600*h + 60*m + s
#-------------------------------------------------------------------------------
def mic_info(mic):
    command = 'arecord -l | grep ' + mic
    result = (subprocess.check_output(command, shell=True)).decode('utf-8')
    cpos = result.find('card'); dpos = result.find('device')
    devicen = result[(len('device')) + dpos + 1]; cardn = result[(len('card')) + cpos + 1]
    return(cardn, devicen)
#-------------------------------------------------------------------------------
def get_fps(videofile):
    command = 'ffprobe -v 0 -of csv=p=0 -select_streams 0 -show_entries stream=r_frame_rate ' + videofile
    result = (subprocess.check_output(command, shell=True)).decode('utf-8')
    r = result.split('/')
    result = round(int(r[0]) / int(r[1]))
    return (result)
#-------------------------------------------------------------------------------
def slice_video(datapath, videofile, duration):
    #sloppy slice... not reencoding...
    #operate in place... 
    os.chdir(datapath)
    vname = videofile.split('.')
    name = vname[0]
    command = 'ffmpeg -i ' + videofile + ' -c copy -map 0 -segment_time ' + str(duration) + ' -f segment -reset_timestamps 1 ' + name+ '%02d.mp4'
    subprocess.call(command, shell=True)
#-------------------------------------------------------------------------------
def get_audio_info(audiofile):
    with contextlib.closing(wave.open(audiofile,'r')) as f:
        rate = f.getframerate()
        frames = f.getnframes()
        duration = frames / float(rate)
    return( rate, frames, duration)
#-------------------------------------------------------------------------------
