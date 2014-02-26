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

#print sys.path

#append lib directory
#sys.path.append( os.path.join( ovpath, 'resources', 'lib' ) )
#insert at location 0 and its libs not lib lol
sys.path.insert( 0,os.path.join( ovpath, 'resources', 'libs' ) )

# used for hugefiles resolver
import jsunpack

#imports of things bundled in the addon
##import container_urls,clean_dirs,htmlcleaner
#import debridroutines






#Helper function to convert strings to boolean values
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

# resolve_billionuploads(url) sourced from Icefilms
def resolve_billionuploads(url):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving BillionUploads Link...')       
        dialog.update(0)
        
        print 'BillionUploads - Requesting GET URL: %s' % url
        import requests
        response = requests.get(url)
        html =response.text
        html = html.encode("ascii", "ignore")
        dialog.update(50)
              
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            print '***** BillionUploads - Site reported maintenance mode'
            raise Exception('File is currently unavailable on the host')

        # Check for file not found
        if re.search('File Not Found', html):
            print '***** BillionUploads - File Not Found'
            raise Exception('File Not Found - Likely Deleted')  
                    
        #Set POST data values
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
        for name, value in r:
            data[name] = value
        
        #Captcha
        captchaimg = re.search('<img src="(http://BillionUploads.com/captchas/.+?)"', html)

        #Some new data values
        data.update({'submit_btn':'', 'referer': '', 'method_free': '', 'method_premium':''})

        r = re.search('document.createElement\(\'input\'\)\)\.attr\(\'type\',\'hidden\'\)\.attr\(\'name\',\'(.+?)\'\)\.val\(\$\(\'textarea\[source="(.+?)"\]\'\)\.val', html)
        if r:
            ra = re.search('<textarea source="%s" style="display: none;visibility: hidden">(.+?)</textarea>' % r.group(2), html)
            if ra:
                data.update({r.group(1):ra.group(1)})
            
        r = re.search('document\.getElementById\(\'.+\'\)\.innerHTML=decodeURIComponent\(\"(.+?)\"\);', html)
        if r:
            r = re.findall('type="hidden" name="(.+?)" value="(.+?)">', urllib.unquote(r.group(1)).decode('utf8') )
            for name, value in r:
                data.update({name:value})

        #Remove some data items
        r = re.findall('\(\'input\[name=\"(.+?)\"\]\'\)\.remove\(\);', html)
        for keyval in r:
            del data[keyval]
        
        dialog.update(50)
        
        print 'BillionUploads - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content
        dialog.update(100)
        
        def custom_range(start, end, step):
            while start <= end:
                yield start
                start += step

        def checkwmv(e):
            s = ""
            
            # Create an array containing A-Z,a-z,0-9,+,/
            i=[]
            u=[[65,91],[97,123],[48,58],[43,44],[47,48]]
            for z in range(0, len(u)):
                for n in range(u[z][0],u[z][1]):
                    i.append(chr(n))
            #print i

            # Create a dict with A=0, B=1, ...
            t = {}
            for n in range(0, 64):
                t[i[n]]=n
            #print t

            for n in custom_range(0, len(e), 72):

                a=0
                h=e[n:n+72]
                c=0

                #print h
                for l in range(0, len(h)):            
                    f = t.get(h[l], 'undefined')
                    if f == 'undefined':
                        continue
                    a= (a<<6) + f
                    c = c + 6

                    while c >= 8:
                        c = c - 8
                        s = s + chr( (a >> c) % 256 )
            return s

        dll = re.compile('<input type="hidden" id="dl" value="(.+?)">').findall(html)[0]
        dl = dll.split('GvaZu')[1]
        dl = checkwmv(dl)
        dl = checkwmv(dl)
        print 'Link Found: %s' % dl                

        return dl
        
    except Exception, e:
        print '**** BillionUploads Error occured: %s' % e
        raise
    finally:
        dialog.close()

def resolve_yify(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Yify Link...')       
        dialog.update(0)
        print 'Yify - Requesting GET URL: %s' % url
        html = net.http_GET(url).content
        url = re.compile('showPkPlayer[(]"(.+?)"[)]').findall(html)[0]
        url = 'http://yify.tv/reproductor2/pk/pk/plugins/player_picasa.php?url=https%3A//picasaweb.google.com/' + url
        html = net.http_GET(url).content
        html = re.compile('{(.+?)}').findall(html)[-1]
        stream_url = re.compile('"url":"(.+?)"').findall(html)[0]
        return stream_url
    except Exception, e:
        print '**** Yify Error occured: %s' % e
        raise
    finally:
        dialog.close()

def resolve_movreel(url):

    try:

        if str2bool(selfAddon.getSetting('movreel-account')):
            print 'MovReel - Setting Cookie file'
            cookiejar = os.path.join(cookie_path,'movreel.lwp')
            net.set_cookies(cookiejar)

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Movreel Link...')       
        dialog.update(0)
        
        print 'Movreel - Requesting GET URL: %s' % url
        html = net.http_GET(url).content
        
        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            print '***** Movreel - Site reported maintenance mode'
            raise Exception('File is currently unavailable on the host')

        #Set POST data values
        op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        method_free = re.search('<input type="(submit|hidden)" name="method_free" (style=".*?" )*value="(.*?)">', html).group(3)
        method_premium = re.search('<input type="(hidden|submit)" name="method_premium" (style=".*?" )*value="(.*?)">', html).group(3)
        
        if method_free:
            usr_login = ''
            fname = re.search('<input type="hidden" name="fname" value="(.+?)">', html).group(1)
            data = {'op': op, 'usr_login': usr_login, 'id': postid, 'referer': url, 'fname': fname, 'method_free': method_free}
        else:
            rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
            data = {'op': op, 'id': postid, 'referer': url, 'rand': rand, 'method_premium': method_premium}
        
        print 'Movreel - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content

        #Only do next post if Free account, skip to last page for download link if Premium
        if method_free:
            #Check for download limit error msg
            if re.search('<p class="err">.+?</p>', html):
                print '***** Download limit reached'
                errortxt = re.search('<p class="err">(.+?)</p>', html).group(1)
                raise Exception(errortxt)
    
            dialog.update(66)
            
            #Set POST data values
            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
    
            if r:
                for name, value in r:
                    data[name] = value
            else:
                print '***** Movreel - Cannot find data values'
                raise Exception('Unable to resolve Movreel Link')

            print 'Movreel - Requesting POST URL: %s DATA: %s' % (url, data)
            html = net.http_POST(url, data).content

        #Get download link
        dialog.update(100)
        link = re.search('<a href="(.+)">Download Link</a>', html)
        if link:
            return link.group(1)
        else:
        	  raise Exception("Unable to find final link")

    except Exception, e:
        print '**** Movreel Error occured: %s' % e
        raise
    finally:
        dialog.close()

def resolve_hugefiles(url):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving HugeFiles Link...')       
        dialog.update(0)
        
        print 'HugeFiles - Requesting GET URL: %s' % url
        html = net.http_GET(url).content
        print 'HugeFiles - Got the webpage'        
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            print '***** HugeFiles - File Not Found'
            raise Exception('File Not Found')
        print 'HugeFiles - Checked page for error messages'
        #Set POST data values
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
        
        if r:
            for name, value in r:
                data[name] = value
        else:
            print '***** HugeFiles - Cannot find data values'
            raise Exception('Unable to resolve HugeFiles Link')
        
        data['method_free'] = 'Free Download'
        file_name = data['fname']

        print 'HugeFiles - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content
        
        #Set POST data values
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
        
        if r:
            for name, value in r:
                data[name] = value
        else:
            print '***** HugeFiles - Cannot find data values'
            raise Exception('Unable to resolve HugeFiles Link')

        embed = re.search('<h2>Embed code</h2>.+?<IFRAME SRC="(.+?)"', html, re.DOTALL + re.IGNORECASE)
        html = net.http_GET(embed.group(1)).content
        
        #Get download link
        dialog.update(100)

        sPattern = '''<div id="player_code">.*?<script type='text/javascript'>(eval.+?)</script>'''
        r = re.findall(sPattern, html, re.DOTALL|re.I)
        if r:
            sUnpacked = jsunpack.unpack(r[0])
            sUnpacked = sUnpacked.replace("\\'","")
            r = re.findall('file,(.+?)\)\;s1',sUnpacked)
            if not r:
               r = re.findall('name="src"[0-9]*="(.+?)"/><embed',sUnpacked)
            return r[0]
        else:
            print '***** HugeFiles - Cannot find final link'
            raise Exception('Unable to resolve HugeFiles Link')
        
    except Exception, e:
        print '**** HugeFiles Error occured: %s' % e
        raise
    finally:
        dialog.close()

# needs a directory at
#home/pi/.xbmc/userdata/addon_data/plugin.video.openviewportal
#created withi default.py using os.makedir
def resolve_180upload(url):

    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving 180Upload Link...')
        dialog.update(0)
        
        puzzle_img = os.path.join(datapath, "180_puzzle.png")
        
        print '180Upload - Requesting GET URL: %s' % url
        html = net.http_GET(url).content
        print 'got the 180 html'
        dialog.update(50)
                
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            raise Exception('Unable to resolve 180Upload Link')
        print 'just about to check for captcha'
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)
        print 'assigned solvemedia variable'
        if solvemedia:
           dialog.close()
           html = net.http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           print 'just about to assign alt_puzzle'
           #Check for alternate puzzle type - stored in a div
           alt_puzzle = re.search('<div><iframe src="(/papi/media.+?)"', html)
           if alt_puzzle:
               open(puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % alt_puzzle.group(1)).content)
           else:
               open(puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % re.search('<img src="(/papi/media.+?)"', html).group(1)).content)
           print 'just about to assign img variable with puzzle_img'
           print 'the puzzle_img path is ' +puzzle_img
#create a control element for your window
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           print 'img variable assigned'
#create your dialog window
           wdlg = xbmcgui.WindowDialog()
           print 'wdlg variable assigned'

#put your control element in your dialog window, this is where it bombs out
#the puzzle_img file size is 300x150 pixels
#need to find out what the cordinate units are in xbmcgui.ControlImage, if they
#pixels then I cannot see how the png image file will fit
#There is a difference between Icefilms and ov that can be seen in debug
#in Icefilms ImageLib-arm.so  is unloaded first but what causes this?
           wdlg.addControl(img)
           print 'added the img to wdlg'
#display your window
           wdlg.show()
           print 'did you see the image?'
           xbmc.sleep(3000)
           print 'wakeup'
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





