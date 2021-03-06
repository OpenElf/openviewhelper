import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon
import os


#EWTN Player. Just learning!


ovpath = '/home/pi/.xbmc/addons/plugin.video.openviewportal/'
# update sys.path
sys.path.insert( 0,os.path.join( ovpath, 'resources', 'libs' ) )

# import ov lib

import ua

pluginhandle=int(sys.argv[1])
addon = xbmcaddon.Addon('plugin.video.ewtnplayer')

# v1.1.0 changed to YT gdata api links

def CATEGORIES():

        ua.update("ewtn","started")

        addDir('Mother Angelica Live Classics','https://gdata.youtube.com/feeds/api/playlists/PLF4E7093F628DD57B?start-index=1&max-results=50',1,'http://www.ewtn.com/Mother_041902.jpg',True)
        addDir( 'Life On The Rock','https://gdata.youtube.com/feeds/api/playlists/PL5ACC9477FE945B19?start-index=1&max-results=50',1,'http://www.passionistnuns.org/blog/wp-content/themes/fallseason/images/LifeontheRocklogoblog.jpg',True)
        addDir( 'News Nightly','https://gdata.youtube.com/feeds/api/playlists/PL9CQlldupc5_STtOyJ3gnmbEWyFDpRzw-?start-index=1&max-results=50',1,'http://laycatholics.files.wordpress.com/2013/09/ewtn-news-nightly-set.jpg',True)
        addDir( 'The Journey Home','https://gdata.youtube.com/feeds/api/playlists/PL97DC29A06F85B07E?start-index=1&max-results=50',1,'http://brightcove.vo.llnwd.net/e1/pd/1675170007001/1675170007001_2785771911001_vs-527178aee4b078301ebe35c3-1083021587001.jpg?pubId=1675170007001',True) 
        addDir( 'The World Over','https://gdata.youtube.com/feeds/api/playlists/PL0B89A05F9F6D3E47?start-index=1&max-results=50',1,'https://5e21104210-custmedia.vresp.com/8d19f99916/World%20Over.jpg',True) 
        addDir( 'Live','https://gdata.youtube.com/feeds/api/playlists/PLA02A15AE776B6200?start-index=1&max-results=50',1,'http://images.zap2it.com/tvbanners/h3/AllPhotos/229688/p229688_b_h3_aa/ewtn-live.jpg',True) 
        addDir( 'Bookmark','https://gdata.youtube.com/feeds/api/playlists/PL66752F72224387D4?start-index=1&max-results=50',1,'http://tmsimg.com/showcards/h3/AllPhotos/229685/p229685_b_h3_aa.jpg',True) 
        addDir( 'Threshold of Hope','https://gdata.youtube.com/feeds/api/playlists/PLBC7E2C12010A545B?start-index=1&max-results=50',1,'http://i1.ytimg.com/vi/LyLh3zB8-64/hqdefault.jpg',True)
        addDir( 'Vaticano','https://gdata.youtube.com/feeds/api/playlists/PL0296666211FB63DA?start-index=1&max-results=50',1,'http://b.vimeocdn.com/ts/443/509/443509831_640.jpg',True)
#added 1.0.2 note mode 3
        addDir( 'The Chaplet of Divine Mercy in Song','p5TGfisOKMM',3,'http://divinemercychant.excerptsofinri.com/images/divine-mercy-chaplet-front-cover.png',False)

                           
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

#v1.1.0 scraper changed from
#        match=re.compile('<meta itemprop="name" content=".+?">\n  <link itemprop="thumbnailUrl" href="(.+?)">\n\n      <div class="thumb-container">\n    <a href="(.+?)" title="(.+?)"').findall(link)

# to

        match=re.compile("href='https://m.youtube.com/details.?v=(.+?)'/.+?<media\:descriptio[^>]+>([^<]+)</media\:description>.+?<media\:thumbnail url='([^']+)'.+?<media:title type='plain'>(.+?)/media:title>",re.DOTALL).findall(link)

#v1.1.0 changed from

#        for thumbnail,url,name in match:
#                splitname=name.partition('-')
#                name=splitname[2]
#                name=name.strip()
#                addDir(name,url,2,thumbnail,False)

# to

        for url,desc,thumbnail,name in (match):

                name=name.replace('<','')
                addDir(name,url,2,thumbnail,False)


def VIDEOLINKS(url,name):
        id=url.lstrip("/watch?v=")
        id=id.partition("&") 
        id=str(id[0])
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + id
        print "VIDEOLINKS " +url
        playvideo(url)
                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def playstream(videoid):
        ok=True
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + videoid
        print "EWTNplayer playstream url is "+url
# hard coded for the chaplet song, should be url passed or is parsed? ha ha
# of course i assume this hard code would play but ...
        liz = xbmcgui.ListItem(path=url)

        xbmcplugin.setResolvedUrl(pluginhandle, True, liz)


        return ok


def playvideo(url):
        ok=True

        print "EWTNplayer playvideo url is "+url

        liz = xbmcgui.ListItem(path=url)

        xbmcplugin.setResolvedUrl(pluginhandle, True, liz)
        return ok

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
        
              
params=get_params()
url=None
name=None
mode=None



try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        ua.update("ewtn","index")
        print "EWTNplayer mode 1"+url
        INDEX(url)
        
elif mode==2:
        ua.update("ewtn",url)
        print "EWTNplayer mode 2"+url
        VIDEOLINKS(url,name)

elif mode==3:
        ua.update("ewtn","chaplet")
        print "EWTNplayer mode 3 "+url
# you need a function that just plays the URL and not send it to youtube
# plugin like v1.0.0 stuff
        playstream(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
