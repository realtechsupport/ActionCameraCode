#!/usr/bin/env python3
#plot_helper.py
#pachube project test module - python3+
#mb/jd, oct/nov 2011
#creates simple plots from the pachube feedlist
#---------------------------------------------------------------------------------
import os, sys
from time import strftime
from datetime import datetime,timedelta
import dateutil.parser
import matplotlib.pyplot as p
import matplotlib as mpl
from math_helper import *

#--------------------------------------------------------------------------------- 
#another function, this one to plot feed data for one selected feed but include mean data from all feeds
def printfig(fig,date,titlecomment,sensordata,timestamps,feed,unit,weathersource,\
        filename='',addmean=0,meandict={},weather=0,tt=[],vv=[]):
    


    #if the big fig isn't created yet, create it. 
    if (fig == None):
        font = {'size'   : 12}
        mpl.rc('font', **font)
        #define figure and size
        fig = p.figure(figsize=(18,6))
        #add the title
        p.title(titlecomment)

    numdatapoints = len(sensordata)

    #color settings
    if(unit == 'C'):
        linecolor = (1,0,0,0.6)
        dotcolor =  (1,0,0,0.6)
        weather_color = (.55,.27,.07)
    elif(unit == 'W'):
        linecolor = (1,.5,0,0.6) 
        dotcolor = (1,.5,0,0.6)
    else:
        linecolor = (1,0,0,0.6)
        dotcolor =  (1,0,0,0.9)
    mean_color = (1,1,0)

    #use the plot_date function to neatly handle dates 
    time_ax = fig.add_subplot(111)
    thisplot = time_ax.plot_date(mpl.dates.date2num(timestamps),sensordata,color=linecolor,fmt='.-',lw=2.0,label=str(feed),tz=None, xdate=True, ydate=False,zorder=2)
    #thisplot = time_ax.plot_date(mpl.dates.date2num(timestamps),sensordata,color=dotcolor,fmt='o',tz=None xdate=True, ydate=False,alpha=0.8,zorder=2)
    
    #plot lines in a different color. play with line thickness. (.2?)
    #different colors for outside (brown), inside (red), and avg color (light yellow)
    #orange for power graph, light yellow for avg
    #lighter gray background.
    #different shade/color for line and 
   
    #time_ax.plot_date(mpl.dates.date2num(timestamps),sensordata, fmt='r.', tz=None, xdate=True, ydate=False)

    #formatting stuff to make the date axis pretty
    dateFmt = mpl.dates.DateFormatter('%m-%d-%Y')
    timeFmt = mpl.dates.DateFormatter('%H:%M %a %m-%d-%Y')

    time_ax.xaxis.set_major_formatter(dateFmt)
    daysLoc = mpl.dates.DayLocator(interval=1)
    hoursLoc = mpl.dates.HourLocator(interval=6)
    time_ax.xaxis.set_major_locator(daysLoc)
    time_ax.xaxis.set_minor_locator(hoursLoc)

    fig.autofmt_xdate(bottom=0.18)
    p.grid(True)
    time_ax.set_axis_bgcolor('#aaaaaa')
    
     #add our mean line if it's activated
    if(addmean):
        fig = addmeanline(fig,meandict,unit,mean_color)
    #similarly, add weatherline
    if(weather):
        fig = addweather(fig,tt,vv, weathersource,weather_color)
        print("Adding weather data...")            
    
    if(unit == 'C'):
        leg = p.legend(loc=4, borderaxespad=0.)    
    elif(unit == 'W'):
        leg = p.legend(loc=2, borderaxespad=0.)
    else:
        leg = p.legend(loc=4, borderaxespad=0.)

    frame = leg.get_frame()
    frame.set_facecolor('#999999')
    for t in leg.get_texts():
        t.set_fontsize('small')    # the legend text fontsize
    #SETTING Y-AXIS LIMITS -- CHANGE THIS TO ADJUST SCALING OF DATA
    if(unit == 'C'):
        p.ylim([0,30])
        feedstr = "temperature" + filename
        time_ax.set_ylabel("Temperature [C]")
    elif(unit == 'W'):
        p.ylim([0,5500])
        feedstr = "ccpower" + filename
        time_ax.set_ylabel("Power Usage [W]")
    else:
        feedstr = "multifeedplot" + filename
        time_ax.set_ylabel("Units")
    #p.subplots_adjust(left=0.1,right=.82)
    imagefile = feed+feedstr+ ".png"
    p.savefig(imagefile,facecolor='#dddddd',edgecolor='#eeeeee')
    #p.savefig(imagefile,dpi=150,facecolor='gray')
    print("SAVED ", imagefile)

    p.close()

    return fig


#one-size-fits all function (it'll plot one feed or twenty just the same)
#   ...well, more or less the same. it'd be nice to implement a function that scales the figsize depending on the number of feeds.
   
def stackfig (fig,date,titlecomment,sensordata,timestamps,feed,feednum,feedlen,color,unit,weathersource,\
        filename='',addmean=0,meandict={},weather=0,tt=[],vv=[]):
    #our iterator starts at 0 but our figures start at 1
    feednum = feednum+1

    #if the big fig isn't created yet, create it. 
    if (fig == None):
        font = {'size'   : 8}
        mpl.rc('font', **font)
        #define figure and size
        params = mpl.figure.SubplotParams(wspace=0.1,hspace=0.1)
        fig = p.figure(figsize=(20,20),subplotpars=params)

        #remove the damned big-figure axes once and for all
        #fig.subplots_adjust(wspace=0.6)
        bigAxes = p.axes(frameon=False,xticks=[], yticks=[])     # hide frame

    #add a subplot to our figure -- we can plot multiple data sets side-by-side this way
    print ("Adding figure: ",feednum,"of ",feedlen)
    time_ax = fig.add_subplot(feedlen,1,feednum)
    
    #use the plot_date function to neatly handle dates 
    time_ax.plot_date(mpl.dates.date2num(timestamps),sensordata, color=color,fmt='-',label=str(feed),tz=None, xdate=True, ydate=False,zorder=1,alpha=0.7)

    #plot the mean right after you plot the data!
    #issue: can't calculate the mean for all of the feeds before we've parsed all feeds. (hence the array index error) 
    if(addmean):
        fig = addmeanline(fig,meandict, unit,feednum,feedlen)
    if(weather):
        print("Adding weather data...")
        fig = addweather(fig,tt,vv,feednum,feedlen, weathersource)
    
    #formatting stuff to make the date axis pretty
    dateFmt = mpl.dates.DateFormatter('%m-%d-%Y')
    timeFmt = mpl.dates.DateFormatter('%H:%M %a %m-%d-%Y')

    #different formatting for different durations
    if (filename[1:4].find('30') != -1):
        time_ax.xaxis.set_major_formatter(dateFmt)
        daysLoc = mpl.dates.DayLocator(interval=1)
        hoursLoc = mpl.dates.HourLocator(interval=3)
        time_ax.xaxis.set_major_locator(daysLoc)
        time_ax.xaxis.set_minor_locator(hoursLoc)
    elif (filename[1:4].find('7') != -1):
        time_ax.xaxis.set_major_formatter(timeFmt)
        hoursLoc = mpl.dates.HourLocator(interval=6)
        minsLoc = mpl.dates.MinuteLocator(interval=30)
        time_ax.xaxis.set_major_locator(hoursLoc)
        time_ax.xaxis.set_minor_locator(minsLoc)
    elif (filename[1:4].find('1') != -1):
        time_ax.xaxis.set_major_formatter(timeFmt)
        hoursLoc = mpl.dates.HourLocator(interval=1)
        minsLoc = mpl.dates.MinuteLocator(interval=10)
        time_ax.xaxis.set_major_locator(hoursLoc)
        time_ax.xaxis.set_minor_locator(minsLoc)
    else:
        time_ax.xaxis.set_major_formatter(dateFmt)
        daysLoc = mpl.dates.DayLocator(interval=1)
        hoursLoc = mpl.dates.HourLocator(interval=6)
        time_ax.xaxis.set_major_locator(daysLoc)
        time_ax.xaxis.set_minor_locator(hoursLoc)
   
    fig.autofmt_xdate(bottom=0.18)
    p.grid(True)
    p.setp(p.getp(p.gca(), 'yticklabels'), fontsize=6) 
    time_ax.set_ylabel("Feed "+feed)
    time_ax.yaxis.set_label_coords(-0.05, 0.5)
    time_ax.set_axis_bgcolor('#999999')
    
    
    #SETTING Y-AXIS LIMITS -- CHANGE THIS TO ADJUST SCALING OF DATA
    if (unit == 'C'):
        time_ax.set_ylim(0,25)
    elif (unit == 'W'):
        time_ax.set_ylim(0,5500)
    
    
    #if we just input our last feed, it's time to save the image.
    if (feednum == feedlen):
        #add the title
        fig.suptitle(titlecomment,fontsize=24)       
        
        if(unit == 'C'):
            feedstr = "stacked_temperature" + filename
            #p.ylabel("Temperature [C]")
        elif(unit == 'W'):
            feedstr = "stacked_sccpower" + filename
            #p.ylabel("Power Usage [W]")
        else:
            feedstr = "stacked" + filename
            #p.ylabel("Units")
        #p.subplots_adjust(left=0.05,right=.82)
        imagefile = feedstr + date + ".png"
        p.savefig(imagefile,facecolor='#dddddd',edgecolor='#eeeeee')
        print("SAVED ", imagefile)
    return fig

#---------------------------------------------------------------------------------     

#this version of the function plots multiple datasets in one figure.

def multifig (fig,date,titlecomment,sensordata,timestamps,feed,feednum,feedlen,color,unit,weathersource,          \
                filename='',addmean=0,meandict={},weather=0,tt=[],vv=[]):
    #our iterator starts at 0 but our figures start at 1
    feednum = feednum+1

    #if the big fig isn't created yet, create it. 
    if (fig == None):
        font = {'size'   : 12}
        mpl.rc('font', **font)
        #define figure and size
        fig = p.figure(figsize=(16,8))
        #add the title
        p.title(titlecomment)

    numdatapoints = len(sensordata)

    #here we're adding each dataset to one subplot
    print ("Adding figure: ",feednum,"of ",feedlen)
    
    #use the plot_date function to neatly handle dates 
    time_ax = fig.add_subplot(111)
    thisplot = time_ax.plot_date(mpl.dates.date2num(timestamps),sensordata,color=color,fmt='o-',label=str(feed),tz=None, xdate=True, ydate=False,zorder=1,alpha=0.7)
    #plot lines in a different color. play with line thickness. (.2?)
    #different colors for outside (brown), inside (red), and avg color (light yellow)
    #orange for power graph, light yellow for avg
    #lighter gray background.
    
    
    #different shade/color for line and 
   
    #time_ax.plot_date(mpl.dates.date2num(timestamps),sensordata, fmt='r.', tz=None, xdate=True, ydate=False)

    
    #formatting stuff to make the date axis pretty -- only need to do this once! 
    if (feednum == 1):
        #formatting stuff to make the date axis pretty
        dateFmt = mpl.dates.DateFormatter('%m-%d-%Y')
        timeFmt = mpl.dates.DateFormatter('%H:%M %a %m-%d-%Y')

        #different formatting for different durations
        '''if (filename[1:4].find('30') != -1):
            time_ax.xaxis.set_major_formatter(dateFmt)
            daysLoc = mpl.dates.DayLocator(interval=2)
            hoursLoc = mpl.dates.HourLocator(interval=3)
            time_ax.xaxis.set_major_locator(daysLoc)
            time_ax.xaxis.set_minor_locator(hoursLoc)
        elif (filename[1:4].find('7') != -1):
            time_ax.xaxis.set_major_formatter(timeFmt)
            hoursLoc = mpl.dates.HourLocator(interval=12)
            minsLoc = mpl.dates.MinuteLocator(interval=60)
            time_ax.xaxis.set_major_locator(hoursLoc)
            time_ax.xaxis.set_minor_locator(minsLoc)
        elif (filename[1:4].find('1') != -1):
            time_ax.xaxis.set_major_formatter(timeFmt)
            hoursLoc = mpl.dates.HourLocator(interval=2)
            minsLoc = mpl.dates.MinuteLocator(interval=10)
            time_ax.xaxis.set_major_locator(hoursLoc)
            time_ax.xaxis.set_minor_locator(minsLoc)
        else:'''
        time_ax.xaxis.set_major_formatter(dateFmt)
        daysLoc = mpl.dates.DayLocator(interval=1)
        hoursLoc = mpl.dates.HourLocator(interval=6)
        time_ax.xaxis.set_major_locator(daysLoc)
        time_ax.xaxis.set_minor_locator(hoursLoc)
   
        fig.autofmt_xdate(bottom=0.18)
        p.grid(True)
        time_ax.set_axis_bgcolor('#999999')
        
    #if we just input our last feed, it's time to save the image.
    if (feednum == feedlen):
        #add our mean line if it's activated
        if(addmean):
            fig = addmeanline(fig,meandict, unit)
        #similarly, add weatherline
        if(weather):
            fig = addweather(fig,tt,vv, weathersource)
            print("Adding weather data...")            
        leg = p.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
        frame = leg.get_frame()
        frame.set_facecolor('#999999')
        for t in leg.get_texts():
            t.set_fontsize('small')    # the legend text fontsize
        #SETTING Y-AXIS LIMITS -- CHANGE THIS TO ADJUST SCALING OF DATA
        if(unit == 'C'):
            p.ylim([0,30])
            feedstr = "temperature" + filename
            time_ax.set_ylabel("Temperature [C]")
        elif(unit == 'W'):
            p.ylim([0,5500])
            feedstr = "ccpower" + filename
            time_ax.set_ylabel("Power Usage [W]")
        else:
            feedstr = "multifeedplot" + filename
            time_ax.set_ylabel("Units")
        p.subplots_adjust(left=0.1,right=.82)
        imagefile = feedstr + date + ".png"
        p.savefig(imagefile,facecolor='#dddddd',edgecolor='#eeeeee')
        #p.savefig(imagefile,dpi=150,facecolor='gray')
        print("SAVED ", imagefile)

        p.close()

    return fig

#this is a separate function to calculate and plot a mean line.    
def addmeanline(fig,mean_dict, unit,color="white",plotnum=1,numplots=1):
    meandates = []
    meanvals = []
    smoothedmeans = []
    
    #unpack our dictionary of date, list-of-value pairs. calculate the mean of each list of values
    for date in sorted(mean_dict.keys()):
        if (len(mean_dict[date]) > 2): #make sure we don't end up with waaay to many date:meanvalue pairs
            meandates.append(dateutil.parser.parse(date, dayfirst=False))
            mean_array = np.array(mean_dict[date])
            meanvals.append(np.mean(mean_array))
   
    #print (len(meandates),len(meanvals))
    #smooth differently for the current cost wattage than for temp
    if(unit == 'C'):
        print("smoothing for temperature")
        smoothedmeans = savitzky_golay(meanvals, window_size=21, order=4)
    elif(unit == 'W'):
        print("smoothing for wattage")
        smoothedmeans = savitzky_golay(meanvals, window_size=7, order=3)
    else:
        print("ACHTUNG - smoothing blindly...")
        smoothedmeans = savitzky_golay(meanvals, window_size=31, order=4)
            
    #this should work the same whether we have one plot or six.        
    print ("Plotting mean on subplot:",plotnum)
    mean_ax = fig.add_subplot(numplots,1,plotnum)
    meanplot = mean_ax.plot_date(mpl.dates.date2num(meandates),smoothedmeans,fmt='-',color=color,lw=1.0,label='smoothed mean',tz=None, xdate=True, ydate=False,alpha=0.8,zorder=1)

    return fig
    
#this is a separate function to plot weather data.    
def addweather(fig,tt,vv,weathersource,color="yellow",plotnum=1,numplots=1):
    #this should work the same whether we have one plot or six.        
    print ("Plotting weather on subplot:",plotnum)
    weather_ax = fig.add_subplot(numplots,1,plotnum)
    
    #smoothing algorithm leaves larger gaps in data -- not using it for now.
    smoothed_vv = savitzky_golay(vv, window_size=51, order=4) 
    
    weatherplot = weather_ax.plot_date(tt,vv,fmt='.-', lw=1.0,color=color,label="outdoor temp: " + "\n" + weathersource, tz=None, xdate=True, ydate=False,zorder=0,alpha=0.8)

    return fig
    
    
