#!/usr/bin/python


############### Imports ############################
#standard module imports
import sys,os
import time,re
import urllib,urllib2,cookielib,base64
import unicodedata
import random
import copy
import threading
import string

##############################################################################################################

import xbmc,xbmcplugin,xbmcgui,xbmcaddon, datetime
import urlresolver

#get path to me
addon_id = 'plugin.video.openviewportal'
selfAddon = xbmcaddon.Addon(id=addon_id)
ovpath = selfAddon.getAddonInfo('path')

''' Use t0mm0's common library for http calls '''
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
net = Net()
addon = Addon(addon_id)
datapath = addon.get_profile()
# /home/pi/.xbmc/userdata/addon_data/plugin.video.openviewportal/
# print datapath


# create userdata paths for addon

#metapath = os.path.join(datapath, 'mirror_page_meta_cache')
cookie_path = os.path.join(datapath, 'cookies')
downinfopath = os.path.join(datapath, 'downloadinfologs')
cookie_jar = os.path.join(cookie_path, "cookiejar.lwp")

# if the datapath is not in place lets create it

if not os.path.exists(datapath): os.makedirs(datapath)
#if not os.path.exists(downinfopath): os.makedirs(downinfopath)
#if not os.path.exists(metapath): os.makedirs(metapath)
#if not os.path.exists(cookie_path): os.makedirs(cookie_path)



#print sys.path

#append lib directory
#sys.path.append( os.path.join( ovpath, 'resources', 'lib' ) )
#insert at location 0 and its libs not lib lol
sys.path.insert( 0,os.path.join( ovpath, 'resources', 'libs' ) )


#print sys.path


#imports of things bundled in the addon
import ovresolvers



#Test Bed Stuff
pluginhandle=int(sys.argv[1])
#addon = xbmcaddon.Addon('plugin.video.openviewportal')
#addon.get_fanart() is using a method in Addon from t0mm0
fanart = addon.get_fanart()

# toplevelmenu() some are playable
def toplevelmenu():

# This is the static Test Video used to ensure the users TV video and sound
# are working.
        
        liz=xbmcgui.ListItem('[COLOR lime]  Test Video[/COLOR]', iconImage='http://openviewrepo.x10.mx/ov_icon_test_video.jpg', thumbnailImage='http://openviewrepo.x10.mx/ov_icon_test_video.jpg')

        liz.setInfo( type="Video", infoLabels={ "Title": 'Test Video' } )
        liz.setProperty('fanart_image', 'http://openviewrepo.x10.mx/ov_test_video.jpg')

# set listitem to playable

        liz.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url='/home/pi/videos/test_video.mp4',listitem=liz,isFolder=False)

# Mode 3 stuff is all about local getting started, the videos that ship with the product
        addDir('[COLOR aqua]  OpenView Getting Started[/COLOR]','http://www.youtube.com/playlist?list=PLF4E7093F628DD57B','getting_started','http://openviewrepo.x10.mx/ov_icon_get_started.jpg',True,'http://openviewrepo.x10.mx/ov_getting_started.jpg')
# mode 1 calls the secondlevelmenu with the appropriate playlist
#        addDir('[COLOR aqua]  Openview Status[/COLOR]','https://gdata.youtube.com/feeds/api/playlists/PLOg_aABUd4EmQ4gTPWyxVrRCjpi8JX1Ej?start-index=1&max-results=50',1,'http://openviewrepo.x10.mx/ov_icon_status.jpg',True,'http://openviewrepo.x10.mx/ov_status.jpg')

        addDir('[COLOR red]  Openview Status[/COLOR]','http://openviewrepo.x10.mx/xml/status.xml',36,'http://openviewrepo.x10.mx/ov_icon_status.jpg',True,'http://openviewrepo.x10.mx/ov_status.jpg')



#        addDir('[COLOR aqua]  OpenView Recommended[/COLOR]','https://gdata.youtube.com/feeds/api/playlists/PLF4E7093F628DD57B?start-index=1&max-results=50',3,'http://openviewrepo.x10.mx/ov_icon_recommended.jpg',True,'http://openviewrepo.x10.mx/ov_recommended.jpg')


        addDir('[COLOR yellow]  OpenView Howto[/COLOR]','https://gdata.youtube.com/feeds/api/playlists/PLOg_aABUd4ElXhIaP9KzblWCb6Jwhdeh-?start-index=1&max-results=50',1,'http://openviewrepo.x10.mx/ov_icon_howto.jpg',True,'http://openviewrepo.x10.mx/ov_howtos.jpg')


#        addDir('[COLOR yellow]  OpenView Latest[/COLOR]','https://raw.github.com/HackerMil/HackerMilsMovieStash/master/Freshout/Directories/This%20Week%27s%20Movies.xml',777,'http://openviewrepo.x10.mx/ov_icon_wotz_new.jpg',True,'http://openviewrepo.x10.mx/ov_new.jpg')


#        addDir('Jack\'s Stash','http://www.youtube.com/playlist?list=PLOg_aABUd4ElXhIaP9KzblWCb6Jwhdeh-',4,'http://3.bp.blogspot.com/-b3R5TnvHon8/UuI-JAEyIpI/AAAAAAAAA0Y/BEwt8c0qeFQ/s1600/jackstash.jpg',True)


        return True

# gettingstarted(url) lists all the static content that is shipped
# with the product. 
# To play a local video you have to give the full path like this:
# /home/pi/video_calibration.mp4


def gettingstarted(url):

        print "entering gettingstarted() .........."

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


# addDirYTxml(url) receives one argument that is an XML file located on
# a server.  From this single file xbmc directories are built.

def addDirYTxml(url):

        print "addDirYTxml() the URL is " +url

        xmlurl = url

# url parsed points to xml file that is located on a server.


        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

# clean

        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

        print "addDirYTxml() the link is " +link

        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)

        print match


        for name,url,thumbnail in match:

            if url == 'nill':
                # information only displayed to user
                # xmlurl is url of xml file just in case user clicks on this directory
                addDir(name,xmlurl,36,thumbnail,True,fanart)
                
            else:
                # playable url for youtube
                addDir(name,url,2,thumbnail,False,fanart)


        return True


# secondlevelmenu(url) receives one argument in the following form
# https://gdata.youtube.com/feeds/api/playlists/PLOg_aABUd4EmQ4gTPWyxVrRCjpi8JX1Ej?start-index=1&max-results=50
# This url houses the YT playlist to be scraped for a name, url and thumbnail.
# The url is the videoid only. The listitems are then displayed in
# the XBM gui

def secondlevelmenu(url):

        print "secondlevelmenu() the URL is " +url

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close() 
        
        match=re.compile("href='https://m.youtube.com/details.?v=(.+?)'/.+?<media\:descriptio[^>]+>([^<]+)</media\:description>.+?<media\:thumbnail url='([^']+)'.+?<media:title type='plain'>(.+?)/media:title>",re.DOTALL).findall(link)
        for url,desc,thumbnail,name in reversed(match):

                name=name.replace('<','')
                addDir(name,url,2,thumbnail,False,'http://openviewrepo.x10.mx/ov_theatre.jpg')

# freshout() receives one argument in the following form
# https://raw.github.com/HackerMil/HackerMilsMovieStash/master/Freshout/Directories/This%20Week%27s%20Movies.xml
# This url points to an XML file that contains links to content.

def freshout(url):

        print "freshout() the URL is " +url

# url parsed points to xml file
# Open xml file, exclude certain hosts that are in these xml files
# because the resolvers do not work.

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

# clean

        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

# add hosts to exclude

        link = re.sub(r'<sublink>http://180upload.+?</sublink>',"", link)

 #       print link

        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)

# Add the directories to display to the user
# the url parsed will a string of sublinks for each named content

        for name,url,thumbnail in match:
            addDir(name,url,888,thumbnail,True,fanart)

        return True





# sublink receives url from freshout.  This url is a list of all the hosts that have the content and orginates from xml file.
def sublink(url):
        print "sublink() the URL is " +url
# the url is a string of sublinks with the various host names
# these are not playable urls yet
# Example
# <sublink>http://billionuploads.com/ajxe5r788ere</sublink><sublink>http://hugefiles.net/rahj3evn4br3</#sublink>
# first we get the host name to display to the user
# the host name by itself can be confussing for the user so we will
# need to also display the name of the content

        match=re.compile('<sublink>(.+?)</sublink>').findall(url)

        print "sublink() match looks like this"
        print match

        for url in match:

# get the host name of the server from the url

            match6=re.compile('http://(.+?)/.+?').findall(url)

            print "sublink() and match6 looks like this"
            print match6

# clean up the host name ready for display

            for url2 in match6:
                host = url2.replace('www.','').replace('.in','').replace('.tv','').replace('.net','').replace('.com','').replace('.to','').replace('.org','').replace('.ch','')

# sometimes a static IP address is given for the content

            if re.findall('\d+.\d+.\d+.\d+',host):
                host='Static'
# capitalize
            host = ' [COLOR blue]'+host.upper()+'[/COLOR]'
            print "sublink() the host to addDir is " +host
            print "sublink() the URL to addDir is " +url
#            addDir(host,url,777,'http://1.bp.blogspot.com/-btG9xVfC8Sk/UgyD4HHFs6I/AAAAAAAAAlA/u84z3lDMPhI/s1600/family-watching-tv.jpg',False)
# now add a directory item for each host.
            myicon=addon.get_fanart()
            iconimage='http://1.bp.blogspot.com/-btG9xVfC8Sk/UgyD4HHFs6I/AAAAAAAAAlA/u84z3lDMPhI/s1600/family-watching-tv.jpg'
            liz=xbmcgui.ListItem(host, iconImage=myicon, thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": host } )
            liz.setProperty('IsPlayable', 'true')
            liz.setProperty('fanart_image', myicon)

#            stream_url = urlresolver.resolve(url)
#perhaps we should set isFolder to true and send the url to addDir then mode it to urlresolver to play see 1 channel        
 #           xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=stream_url,listitem=liz,isFolder=False)
# True is set because the url will not be played directly but will be passed into urlresolver
# Try seeting to False
            addDir(host,url,250,myicon,False,fanart)
        return True

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
# plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=CPCQsOAjEys

def playvideo(url):

#        if 'https' in url:
 #               id=url
 #       else:
        
 #           print "playvideo() the URL is " +url

 #           id=url.lstrip("/watch?v=")

 #           print "playvideo() id after url.lstrip is " +str(id[0])

 #           id=id.partition("&") 

 #           print "playvideo() id after id.partition() is " +str(id[0])

 #           id=str(id[0])

 #           print "playvideo() id after str(id[0]) is " +id

        id = url

        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + id

        print "playvideo() url for  xbmcgui.ListItem(path=url) is " +url

        liz = xbmcgui.ListItem(path=url)

        xbmcplugin.setResolvedUrl(pluginhandle, True, liz)  
        return True

# stub
def jackstash():

        lia=xbmcgui.ListItem('PewDiePie', iconImage="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRx2Z-Xoi8tdEW859CnB9KN0N6kn3rLH6KjhDuJIqF8S3F26PbGEw", thumbnailImage="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRx2Z-Xoi8tdEW859CnB9KN0N6kn3rLH6KjhDuJIqF8S3F26PbGEw")

        lia.setInfo( type="Video", infoLabels={ "Title": 'PewDiePie' } )

        lia.setProperty('fanart_image', 'http://images6.fanpop.com/image/photos/32800000/A-PewDiePie-wallpaper-I-made-for-you-brofist-ladyemzy16-32863202-1366-768.jpg')

        lia.setProperty('IsPlayable', 'true')

# the PewDiePie url is not playable, we need to send it for processing to youtube channel

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url="PewDiePie",listitem=lia,isFolder=True)

# move the mode on to process this url




        return True


def getstreamurl(url):
# This function receives a host url, transforms it to a stream url and plays it.
        print "getstreamurl() the URL is " +url
# extract the host name from inside the url
#        match6=re.compile('http://(.+?)/.+?').findall(url)
 #       for url2 in match6:
  #          host = url2.replace('www.','').replace('.in','').replace('.tv','').replace('.net','').replace('.com','').replace('.to','').replace('.org','').replace('.ch','')

 #       print "getstreamurl(url) the host is " +host
# match the host name to the correct resolver, the resolver will return the playable url
# the resolvers are located in ovresolvers.py or urlresolver.py
#        if host == 'billionuploads':
 #         stream_url = urlresolver.resolve(url)
  #      elif host == 'movreel':
  #        stream_url = ovresolvers.resolve_movreel(url)
   #     elif host == 'hugefiles':
    #      stream_url = ovresolvers.resolve_hugefiles(url)
     #   elif host == 'hugefiles':
        #  stream_url = urlresolver.resolve(url)

        stream_url = urlresolver.resolve(url)

#        elif host == '180upload':
  #        stream_url = urlresolver.resolve(url)
 #         stream_url = getattr(sys.modules[__name__], "resolve_180upload")(url)

# getattr(sys.modules[__name__], "%s" % hoster[3])(url)
#          stream_url = urlresolver.resolve(url)
#       elif host == 'yify':
#        stream_url = urlresolver.resolve(url)

        if stream_url == False:
          print "getstreamurl() says urlresolver returned false"
          return
#        print "getstreamurl() the resolved stream is " +stream_url
# play the url
        playable = xbmcgui.ListItem(path=stream_url)
        xbmcplugin.setResolvedUrl(pluginhandle, True, playable)

        return True

def resolve_180upload(url):

    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving 180Upload Link...')
        dialog.update(0)
        
        puzzle_img = os.path.join(datapath, "180_puzzle.png")
        
        print '180Upload - Requesting GET URL: %s' % url
        html = net.http_GET(url).content

        dialog.update(50)
                
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            raise Exception('Unable to resolve 180Upload Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net.http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           
           #Check for alternate puzzle type - stored in a div
           alt_puzzle = re.search('<div><iframe src="(/papi/media.+?)"', html)
           if alt_puzzle:
               open(puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % alt_puzzle.group(1)).content)
           else:
               open(puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % re.search('<img src="(/papi/media.+?)"', html).group(1)).content)
           
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           xbmc.sleep(3000)

           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()
   
           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving 180Upload Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print '180Upload - Requesting POST URL: %s' % url
        html = net.http_POST(url, data).content
        dialog.update(100)
        
        link = re.search('id="lnk_download" href="([^"]+)', html)
        if link:
            print '180Upload Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            raise Exception('Unable to resolve 180Upload Link')

    except Exception, e:
        print '**** 180Upload Error occured: %s' % e
        raise
    finally:
        dialog.close()





# put this in your default.py
class main (object):
    """Call a function based on XBMC callback string sys.argv[2]"""
    def __init__(self):
        global action
        params = {}

        print "main() sys.argv[2] is " +sys.argv[2]

# This is a callback string example
# ?mode=1&name=Mother%20Angelica%20Live%20Classics&url=http%3a%2f%2f
# www.youtube.com%2fplaylist%3flist%3dPLF4E7093F628DD57B

        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')

        print "main() splitparams list are "
        print ", ".join(splitparams)

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

        print "main() params dictionary are "
        for key in params:
	        print key, params[key]

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
        elif mode == "getting_started"  :      gettingstarted(url)
        elif mode == "4"  :      jackstash()
        elif mode == "250" :    getstreamurl(url)
        elif mode == "777" :    freshout(url)
        elif mode == "888" :    sublink(url)
        elif mode == "36" :    addDirYTxml(url)


        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return
# call main() from default.py

main()


