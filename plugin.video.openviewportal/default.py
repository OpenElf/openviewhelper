#!/usr/bin/python

############### Imports ################################################

import sys,os
import re
import urllib,urllib2
import xbmc,xbmcplugin,xbmcgui,xbmcaddon

########################################################################

# get path to me

addon_id = 'plugin.video.openviewportal'
selfAddon = xbmcaddon.Addon(id=addon_id)

# ovpath will point to
# /home/pi/.xbmc/addons/plugin.video.openviewportal

ovpath = selfAddon.getAddonInfo('path')

''' Use t0mm0's common library for http calls '''
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
net = Net()
addon = Addon(addon_id)

# datapath will point to
# /home/pi/.xbmc/userdata/addon_data/plugin.video.openviewportal/

datapath = addon.get_profile()

# create paths to files

cookie_path = os.path.join(datapath, 'cookies')
downinfopath = os.path.join(datapath, 'downloadinfologs')
cookie_jar = os.path.join(cookie_path, "cookiejar.lwp")
receivedseqnumpath = os.path.join(datapath, 'receivedseqnum')

# if the directories are not in place then make them
 
if not os.path.exists(datapath): os.makedirs(datapath)

# insert at location 0 and its libs not lib lol! This is to ensure
# we search these paths for our bespoke python modules. Remember that
# you need dummy __init__.py files in the directories for module
# imports to work. We do not import modules yet but this is here
# for future developments.

sys.path.insert( 0,os.path.join( ovpath, 'resources', 'libs' ) )

# import of OV modules
import updatefromremote
import ua

# update
#updatefromremote.begin()

# global variables used within many functions

pluginhandle=int(sys.argv[1])
fanart = addon.get_fanart()

def getserial():

        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"

        return cpuserial

# toplevelmenu() is invoked when main() is initially called.
# The params will initially be none.  Some of the directories are
# playable, for example 'Test Video'.

def toplevelmenu():

# This is the playable Test Video used to ensure usersTV video and sound
# are working. This plays a local SD file and does not require internet
# connection.
        
        liz=xbmcgui.ListItem('[COLOR lime]  Test Video[/COLOR]', iconImage='https://raw.github.com/OpenElf/openviewimages/master/ov_icon_test_video.jpg', thumbnailImage='https://raw.github.com/OpenElf/openviewimages/master/ov_icon_test_video.jpg')

        liz.setInfo( type="Video", infoLabels={ "Title": 'Test Video' } )
        liz.setProperty('fanart_image', 'https://raw.github.com/OpenElf/openviewimages/master/ov_test_video.jpg')

# set listitem to playable

        liz.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url='/home/pi/videos/test_video.mp4',listitem=liz,isFolder=False)

# OpenView Getting Started directory is not playable.  The purpose is to
# invoke mode '3' upon user selection.  The url parsed
# points to a YT playlist but this is meaningless because the only
# used will be SD based.

        addDir('[COLOR yellow]  OpenView Getting Started[/COLOR]','http://www.youtube.com/playlist?list=PLF4E7093F628DD57B',3,'https://raw.github.com/OpenElf/openviewimages/master/ov_icon_get_started.jpg',True,'https://raw.github.com/OpenElf/openviewimages/master/ov_getting_started.jpg')

# OpenView Status directory is not playable.  The purpose is to invoke
# mode 4 that will call the addDirxml(url) function.  The url parsed
# points to a status.xml file that is located on a public internet
# server.  The content of this file concerns OpenView status updates.


        addDir('[COLOR yellow]  OpenView Status[/COLOR]','https://raw.github.com/OpenElf/openviewmessages/master/status.xml',4,'https://raw.github.com/OpenElf/openviewimages/master/ov_icon_status.jpg',True,'https://raw.github.com/OpenElf/openviewimages/master/ov_status.jpg')


# OpenView Howto directory is not playable.  The purpose is to invoke
# mode 1 that will call secondlevelmenu(url) function.  The url parsed
# points to playlist on YT.

        addDir('[COLOR yellow]  OpenView Howto[/COLOR]','https://gdata.youtube.com/feeds/api/playlists/PLOg_aABUd4ElXhIaP9KzblWCb6Jwhdeh-?start-index=1&max-results=50',1,'https://raw.github.com/OpenElf/openviewimages/master/ov_icon_howto.jpg',True,'https://raw.github.com/OpenElf/openviewimages/master/ov_howtos.jpg')

# This is the playable Keyboard Video to the keyboard controls
# This plays a remote youtube video.
        
        liz=xbmcgui.ListItem('[COLOR yellow]  OpenView Keyboard[/COLOR]', iconImage='https://raw.github.com/OpenElf/openviewimages/master/ov_icon_keyboard.jpg', thumbnailImage='https://raw.github.com/OpenElf/openviewimages/master/ov_icon_keyboard.jpg')

        liz.setInfo( type="Video", infoLabels={ "Title": 'OpenView Keyboard' } )
        liz.setProperty('fanart_image', 'https://raw.github.com/OpenElf/openviewimages/master/ov_keyboard.jpg')

# set listitem to playable

        liz.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=_ichUqpoo28',listitem=liz,isFolder=False)

        return True

# showMessage() displays dialog boxes to the user based on the contents
# of an xml file located on a server.  Each server based message has a
# unique send sequence number. The function checks the send sequence
# number against what it is expecting next to determine whether the user
# has already seen the message.  This is to prevent the user being hit
# the same message over and over again.

def showMessage():
    

        url = 'https://raw.github.com/OpenElf/openviewmessages/master/message.xml'

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        
        try:
            response = urllib2.urlopen(req)
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("OpenView Warning", "You are not connected to the internet so you will not see", "anything here yet.[COLOR aqua]  Look in [/COLOR][COLOR yellow]OpenView Getting Started[/COLOR]")
            return False

        link=response.read()
        response.close()

        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

        match=re.compile('<message><sendseqnum>(.+?)</sendseqnum><line1>(.+?)</line1><line2>(.+?)</line2><line3>(.+?)</line3></message>').findall(link)


        if len(match)>0:

            if os.path.isfile(receivedseqnumpath):
                f = open(receivedseqnumpath,'r+')
            else:              
                f = open(receivedseqnumpath, 'w+')
                f.write("0")
                f.close
                f = open(receivedseqnumpath,'r+')

            receivedseqnum = f.read()
            f.close()


            for sendseqnum,line1,line2,line3 in match:
                if int(sendseqnum) > int(receivedseqnum):

                    dialog = xbmcgui.Dialog()
                    ok=dialog.ok('[B]Important OpenView Announcement![/B]', str(line1) ,str(line2),str(line3))

            nextexpectedseqnum = int(sendseqnum) + 1
            
            f = open(receivedseqnumpath, 'w+')
            f.write(str(nextexpectedseqnum))
            f.close                                    
    
        else: 
            print 'http://github.com/ Down'
            ua.update("exception","github")

        return True


# from server
#showMessage()


# gettingstarted(url) lists all the SD content that is shipped
# with the product. The content is NOT within the OV addon.  The content
# is located at /home/pi/videos and is pre-installed on the SD card.
# To play a local video you have to give the full path like this:
# /home/pi/video_calibration.mp4


def gettingstarted(url):

        ua.update("openview","gettingstarted")

        lia=xbmcgui.ListItem('Play, Pause & Stop', iconImage="/home/pi/.xbmc/addons/plugin.video.openviewportal/images/play_pause_stop.jpg", thumbnailImage="/home/pi/.xbmc/addons/plugin.video.openviewportal/images/play_pause_stop.jpg")

        lib=xbmcgui.ListItem('Connect using a wired ethernet cable', iconImage="/home/pi/.xbmc/addons/plugin.video.openviewportal/images/wired_connection.jpg", thumbnailImage="/home/pi/.xbmc/addons/plugin.video.openviewportal/images/wired_connection.jpg")

        lic=xbmcgui.ListItem('Connect using a wireless network', iconImage="/home/pi/.xbmc/addons/plugin.video.openviewportal/images/wireless_connection.jpg", thumbnailImage="/home/pi/.xbmc/addons/plugin.video.openviewportal/images/wireless_connection.jpg")

        liz=xbmcgui.ListItem('TV Screen Calibration', iconImage="/home/pi/.xbmc/addons/plugin.video.openviewportal/images/tv_screen_calibration.jpg", thumbnailImage="/home/pi/.xbmc/addons/plugin.video.openviewportal/images/tv_screen_calibration.jpg")

        lia.setInfo( type="Video", infoLabels={ "Title": 'Play, Pause & Stop' } )
        lib.setInfo( type="Video", infoLabels={ "Title": 'Connect using a wired ethernet cable' } )
        lic.setInfo( type="Video", infoLabels={ "Title": 'Connect using a wireless network' } )
        liz.setInfo( type="Video", infoLabels={ "Title": 'TV Screen Calibration' } )

# set fanart

        lia.setProperty('fanart_image', '/home/pi/.xbmc/addons/plugin.video.openviewportal/images/play_pause_stop.jpg')
        lib.setProperty('fanart_image', '/home/pi/.xbmc/addons/plugin.video.openviewportal/images/wired_connection.jpg')
        lic.setProperty('fanart_image', '/home/pi/.xbmc/addons/plugin.video.openviewportal/images/wireless_connection.jpg')
        liz.setProperty('fanart_image', '/home/pi/.xbmc/addons/plugin.video.openviewportal/images/tv_screen_calibration.jpg')

        
# set listitem to playable

        lia.setProperty('IsPlayable', 'true')
        lib.setProperty('IsPlayable', 'true')
        lic.setProperty('IsPlayable', 'true')
        liz.setProperty('IsPlayable', 'true')

# isFolder=False because this is a playable resource

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url="/home/pi/videos/play_pause_stop.mp4",listitem=lia,isFolder=False)

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url="/home/pi/videos/wired_connection.mp4",listitem=lib,isFolder=False)

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url="/home/pi/videos/wireless_connection.mp4",listitem=lic,isFolder=False)

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url="/home/pi/videos/video_calibration.mp4",listitem=liz,isFolder=False)


        return True


# addDirxml(url) builds directories based on the content of an xml file
# located on a server. One of these files is 'status.xml'. This function 
# is called through mode 4 from the OpenView Status toplevelmenu().
# It is not called by anything else.

def addDirxml(url):

        ua.update("openview","status")

        # update
#        updatefromremote.begin()

        xmlurl = url

# Display Important OpenView Annoucements to the user using dialog boxes

#        showMessage()

# Display OpenView Licence

        licence = getserial()
        name = "Your OpenView Licence is " +licence
        addDir(name,xmlurl,4,'nill',True,fanart)

# url parsed points to xml file that is located on a server.


        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        try:
            response = urllib2.urlopen(req)
        except:
            print 'OV - cannot build XML directory listing, x10 down'
            return False

        link=response.read()
        response.close()

# clean

        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)

        for name,url,thumbnail in match:
# the status.xml has link set to 'nill'
            if url == 'nill':
                # information only displayed to user in OV status
                # xmlurl is url of xml file just in case user clicks on
                # this directory we send them back to the same view!
                addDir(name,xmlurl,4,thumbnail,True,fanart)
                
            else:
                # playable url for youtube
                # this is not used, we do not build YT directories based
                # on xml file.
                addDir(name,url,2,thumbnail,False,fanart)


        return True


# secondlevelmenu(url) receives one argument in the following form
# https://gdata.youtube.com/feeds/api/playlists/
#    PLOg_aABUd4EmQ4gTPWyxVrRCjpi8JX1Ej?start-index=1&max-results=50
# url points to YT playlist to be scraped for a name, url and thumbnail.
# Currently two YT playlists are being used 'status' and 'howto'

def secondlevelmenu(url):

        ua.update("openview","howto")

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        
        try:
            response = urllib2.urlopen(req)
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok("OpenView Warning", "You are not connected to the internet so you will not see", "anything here yet.[COLOR aqua]  Look in [/COLOR][COLOR yellow]OpenView Getting Started[/COLOR]")
            return False

        link=response.read()
        response.close() 
        
        match=re.compile("href='https://m.youtube.com/details.?v=(.+?)'/.+?<media\:descriptio[^>]+>([^<]+)</media\:description>.+?<media\:thumbnail url='([^']+)'.+?<media:title type='plain'>(.+?)/media:title>",re.DOTALL).findall(link)
        for url,desc,thumbnail,name in reversed(match):

                name=name.replace('<','')
                addDir(name,url,2,thumbnail,False,'https://raw.github.com/OpenElf/openviewimages/master/ov_theatre.jpg')


# build directories

def addDir(name,url,mode,iconimage,isfolder,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        myicon=addon.get_fanart()
        liz=xbmcgui.ListItem(name, iconImage=myicon, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isfolder)
        return ok



# playvideo plays a Youtube video.  The function takes one argument 
# this is the videoid, for example CPCQsOAjEys
# The url is parsed to the youtube plugin and have this form:
# playvideo() url for  xbmcgui.ListItem(path=url) is 
# plugin://plugin.video.youtube/
#        ?path=/root/video&action=play_video&videoid=CPCQsOAjEys

def playvideo(url):

        ua.update("exception",url)

        id = url

        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + id

        liz = xbmcgui.ListItem(path=url)

        xbmcplugin.setResolvedUrl(pluginhandle, True, liz)
  
        return True




# main

class main (object):
    """Call a function based on XBMC callback string sys.argv[2]"""
    def __init__(self):
        global action

# the x10 ftp is down and this causes the whole portal to error
# need to fix this 28 april
#        updatefromremote.begin()
        # from server
        showMessage()
        
        params = {}

#        print "main() sys.argv[2] is " +sys.argv[2]

# This is a callback string example
# ?mode=1&name=Mother%20Angelica%20Live%20Classics&url=http%3a%2f%2f
# www.youtube.com%2fplaylist%3flist%3dPLF4E7093F628DD57B

        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')

#        print "main() splitparams list are "
#        print ", ".join(splitparams)

# spltparams is a list, the contents are
# mode=1, name=Mother%20Angelica%20Live%20Classics, url=http%3a%2f%2f
# www.youtube.com%2fplaylist%3flist%3dPLF4E7093F628DD57B

        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

#        print "main() params dictionary are "
#        for key in params:
#	        print key, params[key]

# params key/value pairs are
# : main() params dictionary are
# : url
# : http%3a%2f%2fwww.youtube.com%2fplaylist%3flist%3dPLF4E7093F628DD57B
# : mode
# : 1
# : name
# : Mother%20Angelica%20Live%20Classics

# mode url name
# the key names were provided by your addon, probably within the
# url=<value> parameter in xbmcplugin.addDirectoryItem.  XBMC callsback
# your addon with the url string you provided

        try:        mode = urllib.unquote_plus(params["mode"])
        except:     mode = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None

# map a mode to a function
# note that the values in params dictionary are strings not numeric

        if mode   == None :      toplevelmenu()
        elif mode == "1"  :      secondlevelmenu(url)
        elif mode == "2"  :      playvideo(url)
        elif mode == "3"  :      gettingstarted(url)
        elif mode == "4"  :      addDirxml(url)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return
# call main() from default.py

main()


