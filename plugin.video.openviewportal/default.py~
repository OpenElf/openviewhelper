import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

#Test Bed Stuff
pluginhandle=int(sys.argv[1])
addon = xbmcaddon.Addon('plugin.video.openviewportal')

# toplevelmenu() some are playable
def toplevelmenu():

# This is the static Test Video used to ensure the users TV video and sound
# are working.
        
        liz=xbmcgui.ListItem('Test Video', iconImage='http://1.bp.blogspot.com/-btG9xVfC8Sk/UgyD4HHFs6I/AAAAAAAAAlA/u84z3lDMPhI/s1600/family-watching-tv.jpg', thumbnailImage='http://1.bp.blogspot.com/-btG9xVfC8Sk/UgyD4HHFs6I/AAAAAAAAAlA/u84z3lDMPhI/s1600/family-watching-tv.jpg')

        liz.setInfo( type="Video", infoLabels={ "Title": 'Test Video' } )
        liz.setProperty('fanart_image', 'http://4.bp.blogspot.com/-e7CnG6kPs-A/UcGHfG_ZQQI/AAAAAAAAAGs/1dFiD9d7Bds/s1600/P1050212.JPG')

# set listitem to playable

        liz.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url='/home/pi/videos/test_video.mp4',listitem=liz,isFolder=False)


        addDir('Getting Started','http://www.youtube.com/playlist?list=PLF4E7093F628DD57B',3,'http://2.bp.blogspot.com/-UsCN852hjUg/Ucm0KsEeXFI/AAAAAAAAAIQ/LGSIWTbydqA/s1600/getting_started.jpg',True)

        addDir('Status','http://www.youtube.com/playlist?list=PLOg_aABUd4EmQ4gTPWyxVrRCjpi8JX1Ej',1,'http://4.bp.blogspot.com/-kkq3lL3ZHow/UfPyjJQ85YI/AAAAAAAAAcA/NFuMmYpRjvg/s1600/status.jpeg',True)

        addDir('Recommended','http://www.youtube.com/playlist?list=PLF4E7093F628DD57B',3,'http://3.bp.blogspot.com/-9hMdKmDQRD4/UfF_mECzJrI/AAAAAAAAAak/3NdATzTI3tg/s250/openview_recommended.png',True)

        addDir('HOWTOs','http://www.youtube.com/playlist?list=PLOg_aABUd4ElXhIaP9KzblWCb6Jwhdeh-',1,'http://2.bp.blogspot.com/-C8NREK6a9XE/Ufa6qS1jSXI/AAAAAAAAAdI/K5lYsD_OH4A/s1600/listening.jpg',True)

        addDir('Jack\'s Stash','http://www.youtube.com/playlist?list=PLOg_aABUd4ElXhIaP9KzblWCb6Jwhdeh-',4,'http://3.bp.blogspot.com/-b3R5TnvHon8/UuI-JAEyIpI/AAAAAAAAA0Y/BEwt8c0qeFQ/s1600/jackstash.jpg',True)


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


# secondlevelmenu(url) is playable
def secondlevelmenu(url):

        print "secondlevelmenu() the URL is " +url

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<meta itemprop="name" content=".+?">\n  <link itemprop="thumbnailUrl" href="(.+?)">\n\n      <div class="thumb-container">\n    <a href="(.+?)" title="(.+?)"').findall(link)
        for thumbnail,url,name in match:
 #               splitname=name.partition('-')
#                name=splitname[2]
 #               name=name.strip()
                addDir(name,url,2,thumbnail,False)


def addDir(name,url,mode,iconimage,isfolder):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        myicon=addon.getAddonInfo('fanart')
        liz=xbmcgui.ListItem(name, iconImage=myicon, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty('fanart_image', myicon)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isfolder)
        return ok



# playvideo plays a Youtube video
def playvideo(url):
        
        print "playvideo() the URL is " +url

        id=url.lstrip("/watch?v=")

        print "playvideo() id after url.lstrip is " +str(id[0])

        id=id.partition("&") 

        print "playvideo() id after id.partition() is " +str(id[0])

        id=str(id[0])

        print "playvideo() id after str(id[0]) is " +id

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

# put this in your default.py
class main (object):
    """Call a function based on XBMC callback string sys.argv[2]"""
    def __init__(self):
        global action
        params = {}
# sys.argv[2] from XBMC originated from within your addon.
# originate may look like this where the & delimits some
# key/value pairs and = delimits value from key and ? delimits start.
# u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+
# "&name="+urllib.quote_plus(name)
# XBMC callback string may look like this

        print "main() sys.argv[2] is " +sys.argv[2]

# This is the callback string from toplevelmenu()
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

# replace XXXX, YYYY and ZZZZ with dictionary key names; mode url name
# the key names were provided by your addon to XBMC probably within the
# url=<value> parameter in xbmcplugin.addDirectoryItem.  XBMC callsback
# your addon with the url string you provided

        try:        mode = urllib.unquote_plus(params["mode"])
        except:     mode = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None

# map function to XXXX, replace function name
# note that the values in params dictionary are strings not numeric

        if mode   == None :      toplevelmenu()
        elif mode == "1"  :      secondlevelmenu(url)
        elif mode == "2"  :      playvideo(url)
        elif mode == "3"  :      gettingstarted(url)
        elif mode == "4"  :      jackstash()

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return
# call main() from default.py

main()


