#!/usr/bin/env python
#av_helper.py
#version 7
#utilities for audio and video processing
#ART 350
#jan - april 2019
#author: realtechsupport
#-------------------------------------------------------------------------------
from utilities import *
from image_helper import *
from datetime import datetime, timedelta
#------------------------------------------------------------------------------

def remove_audio_from_video(videofile):
    videoname = videofile.split('.')
    videofile_new = videoname[0] + '_noaudio.' + videoname[1]
    command = 'ffmpeg -loglevel panic -i ' + videofile + ' -y -vcodec copy -an ' + videofile_new
    subprocess.call(command, shell=True)
    print('new video without audio is now in the same directory as the original')
#------------------------------------------------------------------------------

def extract_audio_from_video(videofile, encoding):
    videoname = videofile.split('.')
    audiofile = videoname[0] + '.' + encoding
    command = 'ffmpeg -i ' + videofile  + ' -f ' + encoding + ' -ab 192000 -vn ' +  audiofile
    subprocess.call(command, shell=True)
    print('audio track is now in the same directory as the video')

#-------------------------------------------------------------------------------

def get_video_length(filename):
    result = subprocess.Popen(["ffprobe", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    info  =  [x for x in result.stdout.readlines() if b'Duration' in x]
    duration = info[0].decode('utf-8')
    duration = duration.split(', ')
    time_s = duration[0].split('Duration: ')
    time_t = str(time_s[1])
    return (time_t)
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
    result = (int(r[0]) / int(r[1]))
    return (result)

#-------------------------------------------------------------------------------

def get_videoresolution(videofile):
    command = 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1:nk=1 ' + videofile
    result = (subprocess.check_output(command, shell=True)).decode('utf-8')
    r = result.split('\n')
    return (r[0], r[1])

#-------------------------------------------------------------------------------

def extract_segment(datapath, videofile, time_s, time_e, segmentname):
    command = 'ffmpeg -loglevel panic -y -i '+ datapath+videofile +  ' -ss ' + time_s + ' -to ' + time_e + ' -c copy ' +  datapath+segmentname
    subprocess.call(command, shell=True)
#-------------------------------------------------------------------------------

def combine_segments(datapath, segment1, segment2, outputname):
    listname = 'list.txt'
    list = open(listname, 'w')
    list.write('file ' + datapath+segment1)
    list.write('\n')
    list.write('file ' + datapath+segment2)
    list.close()

    command = 'ffmpeg -f concat -safe 0 -i ' + listname + ' -c copy ' + datapath+outputname
    #command = 'ffmpeg -f concat -safe 0 -i ' + listname + ' -c:v libvpx-vp9 -c:a libopus ' + datapath+outputname
    subprocess.call(command, shell=True)
    #os.remove(listname)

#------------------------------------------------------------------------------

def combine_segments_v2(datapath, s):
    offset = 1
    for i in range (0, (len(s)-offset), offset):
        if(i==0):
            source = datapath+s[i]
        else:
            source = datapath+output

        print(i+offset, s[i+offset])
        command = 'ffmpeg -loglevel panic -y -i ' + source + ' -c copy -bsf:v h264_mp4toannexb -f mpegts i1.ts'
        subprocess.call(command, shell=True)
        command = 'ffmpeg -loglevel panic -y -i ' + datapath+s[i+offset] + ' -c copy -bsf:v h264_mp4toannexb -f mpegts i2.ts'
        subprocess.call(command, shell=True)
        output = 'output_'+ str(i+offset) + '.mp4'
        command = 'ffmpeg -loglevel panic -y -i "concat:i1.ts|i2.ts" -c copy -bsf:a aac_adtstoasc ' + datapath+output
        subprocess.call(command, shell=True)
        time.sleep(2)
        try:
            os.remove('i1.ts')
            os.remove('i2.ts')
        except:
            pass

#-------------------------------------------------------------------------------

def extract_image(datapath, videofile, moment, quality, imagename):
    os.chdir(datapath)
    command = 'ffmpeg -loglevel panic -ss ' + moment + ' -i ' + videofile + ' -vframes 1 -q:v 1 ' + imagename
    subprocess.call(command, shell=True)
#-------------------------------------------------------------------------------

def process_images_blur(tpath, datapath, kernel):
    files = glob.glob(tpath+'*.*')
    files.sort()
    for i in files:
        img =  cv2.imread(i)
        change =  cv2.blur(img,kernel)
        cv2.imwrite(i, change)

    return("blur")

#-------------------------------------------------------------------------------

def process_images_addtext(tpath, datapath, fontpath, text, fontchoice, fontsize, dw, dh, space, tcolor):
    files = glob.glob(tpath+'*.*')
    files.sort()
    for i in files:
        img =  cv2.imread(i)
        cv2_im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        width, height = pil_im.size
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype(fontpath+fontchoice, fontsize)
        draw.text((int(dw*width), int(dh*height)), text, font=font, fill=tcolor)
        change = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        cv2.imwrite(i, change)

    return("addtext")

#-------------------------------------------------------------------------------

def process_images_coloroverlay(tpath, datapath, color, img_contrib, backimg_contrib):
    files = glob.glob(tpath+'*.*')
    files.sort()
    for i in files:
        img =  cv2.imread(i)
        height, width, dim = img.shape
        backimg = create_image(height, width, dim, color)
        change = cv2.addWeighted(img, img_contrib, backimg, backimg_contrib, 0)
        cv2.imwrite(i, change)

    return("coloroverlay")
#-------------------------------------------------------------------------------

def process_images_edgedetect(tpath, datapath, sigma):
    files = glob.glob(tpath+'*.*')
    files.sort()
    for i in files:
        img =  cv2.imread(i)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        v = np.median(gray)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        change = cv2.Canny(gray, lower, upper)
        cv2.imwrite(i, change)

    return("edgedetect")
#-------------------------------------------------------------------------------

def process_images_grayscale(tpath, datapath):
    files = glob.glob(tpath+'*.*')
    files.sort()
    for i in files:
        img =  cv2.imread(i)
        change = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(i, change)

    return("grayscale")
#-------------------------------------------------------------------------------

def process_images_none(tpath, datapath):
    files = glob.glob(tpath+'*.*')
    files.sort()
    for i in files:
        img =  cv2.imread(i)
        change = img
        cv2.imwrite(i, change)

    return("none")
#-------------------------------------------------------------------------------

def process_images_videooverlay(datapath, t1, t2, segment1, segment2, seg1_contrib, seg2_contrib):

    framerate1 = get_fps(datapath+segment1)
    framerate2 = get_fps(datapath+segment2)
    tpath1 = datapath+t1
    tpath2 = datapath+t2
    create_images_from_video(datapath, t1, segment1, framerate1)
    create_images_from_video(datapath, t2, segment2, framerate2)
    files1 = glob.glob(tpath1+'*.*')
    files2 = glob.glob(tpath2+'*.*')

    if(len(files1)!= len(files2)):
        l = min(len(files1), len(files2))
    else:
        l = len(files1)

    files1 = files1[:l]
    files2 = files2[:l]

    files1.sort()
    files2.sort()

    for k in range(0, l-1):
        img1 = cv2.imread(files1[k])
        img2 = cv2.imread(files2[k])
        #check sizes
        s1 = img1.shape
        s2 = img2.shape
        if(s1 != s2):
            print('video size missmatch....')
            break
        else:
            change = cv2.addWeighted(img1, seg1_contrib, img2, seg2_contrib, 0)
            cv2.imwrite(files1[k], change)

    return("videooverlay")
#-------------------------------------------------------------------------------

def create_images_from_video(datapath, t, videofile, framerate):
    os.chdir(datapath)
    dir_t = datapath+t
    tempok = os.path.isdir(dir_t)
    if(tempok):
        pass
    else:
        os.mkdir(dir_t)

    end_set = " -f image2 "
    out = t + '%04d.jpg'
    s1 = "ffmpeg -y -i "

    command = s1 + videofile + ' -r ' + str(framerate) + end_set + out
    subprocess.call(command, shell=True)
#-------------------------------------------------------------------------------

def get_audio_info(audiofile):
    with contextlib.closing(wave.open(audiofile,'r')) as f:
        rate = f.getframerate()
        frames = f.getnframes()
        duration = frames / float(rate)
    return( rate, frames, duration)
#-------------------------------------------------------------------------------

def create_difference_images(datapath, loc):
    os.chdir(datapath)

    dir_t = datapath + loc
    tempok = os.path.isdir(dir_t)
    if(tempok):
        pass
    else:
        os.mkdir(dir_t)

    path, dirs, files = next(os.walk(datapath))
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    f_count = len(files)

    for i in range(0, (f_count-1)):
            img1 =  cv2.imread(datapath + files[i])
            img2 =  cv2.imread(datapath + files[i+1])
            diff =  cv2.subtract(img2, img1)
            result = 'diff_' + str(i) + '.jpg'
            cv2.imwrite(dir_t + result, diff)

#-------------------------------------------------------------------------------

def create_video_from_images(dpath, tpath, framerate, reverse, outputname):
    os.chdir(tpath)
    if(reverse == True):
        command = 'ffmpeg -framerate ' + str(framerate) + ' -f image2 -i %04d.jpg -c:v h264 -crf 1 -vf reverse ' + outputname
    else:
        command = 'ffmpeg -framerate ' + str(framerate) + ' -f image2 -i %04d.jpg -c:v h264 -crf 1 ' + outputname

    subprocess.call(command, shell=True)
    shutil.move(tpath+outputname, dpath+outputname)

#-------------------------------------------------------------------------------

def create_video_from_singlecolorimage(datapath, height, width, duration, color, outputname):
    img = create_image(height, width, 3, color)
    imgname = 'transition.jpg'
    cv2.imwrite(datapath+imgname, img)
    loadedimg = cv2.imread(datapath+imgname)
    command = 'ffmpeg -loop 1 -i ' + datapath+imgname + ' -c:v libx264 -t ' + str(duration) + ' -pix_fmt yuv420p ' + datapath+outputname
    subprocess.call(command, shell=True)

#-------------------------------------------------------------------------------

def create_video_from_singlecolorimage_withtext(datapath, height, width, duration, color, transition, text, fontpath, fontchoice, fontsize, dw, dh, space,tcolor):
    img = create_image(height, width, 3, color)
    imgname = 'transition.png'
    cv2.imwrite(datapath+imgname, img)
    img = cv2.imread(datapath+imgname)

    cv2_im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im_rgb)
    width, height = pil_im.size
    font = ImageFont.truetype(fontpath+fontchoice, fontsize)
    draw = ImageDraw.Draw(pil_im)
    draw.text((int(dw*width), int(dh*height)), text, font=font, fill=tcolor)
    change = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    cv2.imwrite(datapath+imgname, change)

    command = 'ffmpeg -loop 1 -y -i ' + datapath+imgname + ' -c:v libx264 -t ' + str(duration) + ' -pix_fmt yuv420p ' + datapath+transition
    subprocess.call(command, shell=True)

    return('colorback+txt')
#-------------------------------------------------------------------------------
