#!/usr/bin/env python
#utlities.py (python3)
#additional helper functions
#ART350
#jan - april 2019
#author: realtechsupport
#-------------------------------------------------------------------------------
import sys, os, time, datetime
from os import environ, path
import json as simplejson
import subprocess
import psutil, shutil
import signal, wave
import contextlib
#import geocoder
#------------------------------------------------------------------------------
def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()
#-------------------------------------------------------------------------------
def write2file(filename, comment):
    file = open(filename, "a")
    value = file.write(comment)
    file.close()
#-------------------------------------------------------------------------------
def get_context():
    print('add contextual information for the video annotation')
    context = {}
    context['videomaker']  = input("who shot the video? ")
    context['annotator'] = input("who is making the annotations? ")
    context['location'] = input("where was the video made? ")
    context['content'] = input("what content does the video show? ")
    context['projecthistory'] = input("mention the project history, if applicable ")
    context['comments'] = input("other comments ? ")
    return(context)
#-------------------------------------------------------------------------------
def get_location(namedlocation):
    if (namedlocation == 'ip'):
        loc = geocoder.ip('me')
    else:
        loc = geocoder.google(namedlocation)
        print(loc)
    return(loc.latlng)
#-------------------------------------------------------------------------------
