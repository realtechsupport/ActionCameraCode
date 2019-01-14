#!/usr/bin/env python
#bigsmall
#small screen with big ambitions
#dms events display
#feb2017
#-------------------------------------------------------------------
import os, sys, time, string
from time import strftime
from urllib2 import urlopen
import glob
import pygame
from pygame.locals import *
import random
from bigsmallclasses import *

flags = DOUBLEBUF
os.environ["DISPLAY"] = ":0"
game_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
path2icons = os.path.join(game_dir, 'assets_bs/')
screen = pygame.display.set_mode((0,0), pygame.NOFRAME)
screen.set_alpha(None)
#------------------------------------------------------------------------------
d_width=480;d_height=270;black=(0,0,0)
#-------------------------------------------------------------------------------
def get_current_events(filepath, filename):
    current_events = []
    off = 3
    tbl_1 = string.maketrans(',', ' ')

    try:
        data_object = urlopen(filepath+filename)
        print('got file from server')
    except:
        print('...cant access web...using local file ...')
        data_object = get_local_version(filename)

    for line in data_object:
        line = line.translate(None, '\t\n')
        line = line.translate(tbl_1)
        line = line.decode('utf_8')
        line += ' '*off
        current_events.append(line)

    return (current_events)
#-----------------------------------------------------
def get_local_version(filename):
    with open(os.path.join(game_dir, filename)) as f:
        lines = f.readlines()
    return(lines)
#-----------------------------------------------------
def load_background(name, backgrounds):
    for i in range(0, len(backgrounds)):
        if(name in backgrounds[i]):
            backgroundfile = path2icons + backgrounds[i]
            break
    thisbackground = pygame.image.load(backgroundfile)
    return(thisbackground)

#------------------------------------------------------
def load_black(color):
    blackback = pygame.Surface(screen.get_size())
    blackback = blackback.convert()
    blackback.fill(color)
    return(blackback)

#-------------------------------------------------------
def load_font(fontname, fontsize):
    sel_font = pygame.font.SysFont(fontname, fontsize)
    return(sel_font)

#-------------------------------------------------------
def display_texts(texts, fcolor, bcolor, position, fontname, fontsize1, fontsize2, offset1, offset2, wait):
    blackback = load_black(bcolor)
    pygame.font.init()
    screen.fill(bcolor)
    #first two lines: title
    for i in range(0, 3):
        sel_font = load_font(fontname, fontsize1)
        text = sel_font.render(texts[i], True, fcolor, bcolor)
        textrect = text.get_rect()
        textrect.centerx = d_width/2
        textrect.centery = d_height/2 - (0.5*position[1]-offset2*i)
        screen.blit(text, textrect)
        pygame.display.update()
        time.sleep(wait*0.5)

    time.sleep(wait*2)
    screen.fill(bcolor)
    pygame.display.update()
    time.sleep(wait*0.5)

    #dates and names after the title ------------------------------------------
    shifted=0;limit=35;space=2;loc=0;diff=0;height_limit=220;diff_limit=5;reset=1
    sel_font = load_font(fontname, fontsize2)

    for i in range(3, len(texts)):
        j = i-diff
        if(diff > diff_limit):
            reset = 1
        #reset if at end of screen height
        if((d_height/2 - (position[1]-offset1*j) > height_limit) & (reset == 1)):
            j=2
            diff = i-j
            screen.fill(bcolor)
            pygame.display.update()
            time.sleep(wait*0.5)
            reset = 0

        #name too long?
        num_chars = len(texts[j])
        try:
            loc = texts[j].index('&')
        except:
            pass
        if(loc > 0):
            limit = loc + space
        #usually name has space on one line
        if(num_chars < limit):
            text = sel_font.render(texts[i], True, fcolor, bcolor)
            textrect = text.get_rect()
            textrect.centerx = d_width/2

            if (shifted != 1):
                textrect.centery = d_height/2 - (position[1]-offset1*j)
            else:
                textrect.centery = d_height/2 - (position[1]-offset1*(j+1))

            screen.blit(text, textrect)
        #if name extends across two lines
        else:
            text1 = sel_font.render(texts[i][:limit], True, fcolor, bcolor)
            text2 = sel_font.render(texts[i][limit:], True, fcolor, bcolor)
            textrect1 = text1.get_rect()
            textrect2 = text2.get_rect()
            textrect1.centerx = d_width/2
            textrect2.centerx = d_width/2
            textrect1.centery = d_height/2 - (position[1]-offset1*j)
            textrect2.centery = d_height/2 - (position[1]-offset1*(j+1))
            screen.blit(text1, textrect1)
            screen.blit(text2, textrect2)
            shifted = 1
        #update and wait a bit
        pygame.display.update()
        time.sleep(wait*1)

#-------------------------------------------------------
def get_servicelog(servicelog):
    with open(servicelog) as f:
        last = None
        for last in (line for line in f if line.rstrip('\n')):
            pass
    return(last.strip())

#-------------------------------------------------------
def create_episode(current_events, num_images):
    e = Episode()
    selected_images = []
    fcolor=(200,200,200);bcolor=(0,0,0);fontsize1=44;fontsize2=24;fontname='liberationmono'	#'dejavuserif','freemono'
    position=[100,120];offset1=30;offset2=60;wait=3.0;time=0.3;longwait=6.0
    #add text
    alltext = Text(current_events, fcolor, bcolor, position, fontname, fontsize1, fontsize2, offset1, offset2, wait)
    e.add_texts(alltext)
    #add Images
    selected_images = select_images(num_images)
    allimages = Images(selected_images,longwait)
    e.add_images(allimages)
    return(e)

#-------------------------------------------------------
def do_episode(e):
    blackback = load_black(black)
    time.sleep(1)
    #do text display
    if(len(e.texts) > 0):
        display_texts(e.texts[0].texts, e.texts[0].fcolor, e.texts[0].bcolor, e.texts[0].position, e.texts[0].fontname, \
        e.texts[0].fontsize1, e.texts[0].fontsize2, e.texts[0].offset1, e.texts[0].offset2, e.texts[0].wait)

    if(len(e.images) > 0):
        display_images(e.images[0].names, e.images[0].wait)
    else:
        pass

#--------------------------------------------------------
def select_images(num_images):
    #take only a few
    some_images = int(num_images/2)
    n = choose_number(some_images)
    indeces = random.sample(range(1, num_images), n)
    #print(indeces)
    names = os.listdir(path2icons)
    selected_names = []
    for i in range (0, n):
        selected_names.append(names[indeces[i]])

    return(selected_names)

#--------------------------------------------------------
def display_images(names, wait):
    for i in range (0, len(names)):
        current_image = pygame.image.load(path2icons + names[i])
        screen.blit(current_image, (0,0))
        pygame.display.flip()
        time.sleep(wait)

#--------------------------------------------------------
def choose_number(limit):
    n = random.randint(1,limit)
    return(n)
#----------------------------------------------------------
