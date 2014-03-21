#!/usr/bin/python

############### Imports ################################################

import sys,os,ftplib
import re
#import urllib,urllib2
import xbmc
#xbmcplugin,xbmcgui,xbmcaddon

########################################################################


# set up UA

ovpath = '/home/pi/.xbmc/addons/plugin.video.openviewportal/'
sys.path.insert( 0,os.path.join( ovpath, 'resources', 'libs' ) )
import ua



# Connection information

server = 'ftp.openviewrepo.x10.mx'
username = 'openelf@openviewrepo.x10.mx'
password = 'secret7'

 
# Server XML directory and XML updater file name

xmldirectoryonserver = '/xml'
xmlupdaterfile = 'updater.xml'

# OpenView directory

ovxmlupdaterpath = '/home/pi/'


# wildcard match for all files with extensions
filematch = '*.*'


#ftpdownload() get a file called updater.xml from the server and writes it to
#the pi home directory.  The contents of this file are the parameters used in
#the update.

def getupdaterxmlfile():

    if not os.path.exists(ovxmlupdaterpath):
        os.makedirs(ovxmlupdaterpath)

# Change destination directory
    os.chdir(ovxmlupdaterpath)
 
# Establish the connection

    ftp = ftplib.FTP()
    
    try:
        ftp.connect(server)
    except:
        print 'OV - cannot connect to FTP server'
        ua.update("exception","ftpconnect")        
        return False

    if not ftp.login(username, password):
        print 'OV - login failed to FTP server'
        ua.update("exception","ftplogin")
        return False
        
 
# Change to the proper directory
    ftp.cwd(xmldirectoryonserver)

# Check to make sure file is on server

    if not ftp.nlst(xmlupdaterfile):
        print 'OV - updatefromremote.py - Missing file called ' +xmlupdaterfile
        ua.update("exception","xmlupdatefile")
        return False
 
# Loop through matching files and download each one individually
# you could use wildcards like *.* to match all files and therefore download
# all files
    for filename in ftp.nlst(xmlupdaterfile):
        fhandle = open(filename, 'wb')
        print 'OV - updatefromremote.py - Getting ' + xmldirectoryonserver + filename
        ftp.retrbinary('RETR ' + filename, fhandle.write)
        fhandle.close()
    return True



# if the update flag is set then start to update OV. The update flag is set in
# updater.xml that should now be located at /home/pi after the call to
# getupdaterxmlfile()

def starttoupdate():

# open the updater.xml file that in the the OV /home/pi directory

    f = open(ovxmlupdaterpath+xmlupdaterfile,'r+')

# make a string of the filecontents

    xmlfilecontent = f.read()
    f.close()

# get rid of stuff in the string

    xmlfilecontent = xmlfilecontent.replace('\r','').replace('\n','').replace('\t','')
    
# get the update flag value

    match=re.compile('<update>(.+?)</update>').findall(xmlfilecontent)

# if the update flag is true then we return true

    if match[0] == 'TRUE':
        return True

# if the update flag is false then we return false

    if match[0] == 'FALSE':
        return False
    return


def checkupdatelevel():

    currentupdatelevel = '/home/pi/.xbmc/userdata/addon_data/plugin.video.openviewportal/currentupdatelevel'

# open the updater.xml file that in the the OV /home/pi directory

    f = open(ovxmlupdaterpath+xmlupdaterfile,'r+')

# make a string of the filecontents

    xmlfilecontent = f.read()
    f.close()

# get rid of stuff in the string

    xmlfilecontent = xmlfilecontent.replace('\r','').replace('\n','').replace('\t','')
  
# make dictionary

    match=re.compile('<number>(.+?)</number><server_directory>(.+?)</server_directory><server_file>(.+?)</server_file><ov_directory>(.+?)</ov_directory>').findall(xmlfilecontent)


    if len(match)>0:

        if os.path.isfile(currentupdatelevel):
            f = open(currentupdatelevel,'r+')
        else:              
            f = open(currentupdatelevel, 'w+')
            f.write("0")
            f.close
            f = open(currentupdatelevel,'r+')

        currentlevel = f.read()
        f.close()

        for number,server_dir,server_file,ov_dir in match:
            if int(number) >= int(currentlevel):
                # update is needed
                return True                                
    
    else:
        print 'OV - http://openviewrepo.x10.mx/ Down'
        ua.update("exception","x10down")

    # False because no update is needed
    return False

def update():

    currentupdatelevel = '/home/pi/.xbmc/userdata/addon_data/plugin.video.openviewportal/currentupdatelevel'

# open the updater.xml file that in the the OV /home/pi directory

    f = open(ovxmlupdaterpath+xmlupdaterfile,'r+')

# make a string of the filecontents

    xmlfilecontent = f.read()
    f.close()

# get rid of stuff in the string

    xmlfilecontent = xmlfilecontent.replace('\r','').replace('\n','').replace('\t','')
  
# make dictionary

    match=re.compile('<number>(.+?)</number><server_directory>(.+?)</server_directory><server_file>(.+?)</server_file><ov_directory>(.+?)</ov_directory>').findall(xmlfilecontent)

# update

    for number,server_dir,server_file,ov_dir in match:

        # Change to OV local directory
        if not os.path.exists(ov_dir):
            os.makedirs(ov_dir)

        os.chdir(ov_dir)

        # Establish connection to server
        ftp = ftplib.FTP(server)
        if not ftp.login(username, password):
            ua.update("exception","ftplogin")
            return False
        
        # Change to the proper directory on server
        ftp.cwd(server_dir)

        # Check to make sure file is on server
        if not ftp.nlst(server_file):
            print 'OV - updatefromremote.py - Missing file called ' +server_file
            ua.update("exception","ftpfilemissing")
            return False

        # copy files from server to OV
        for filename in ftp.nlst(server_file):
            fhandle = open(filename, 'wb')
            print 'OV - updatefromremote.py - Getting ' + server_dir + "/" + filename
            ua.update("openview","ftpupdate")
            ftp.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()

    nextexpectedupdatenumber = int(number) + 1
            
    f = open(currentupdatelevel, 'w+')
    f.write(str(nextexpectedupdatenumber))
    f.close  

    return


def begin():
    print "OV - begin update"

    # is there a local updater.xml file?

    xmlupdatefile = getupdaterxmlfile()
    if xmlupdatefile == True:
        # is there an update flag set in the updater.xml file?
        updateflag = starttoupdate()
    
        if updateflag == True:
            # is there a new update?
            newupdate = checkupdatelevel()
            if newupdate == True:
                ua.update("openview","newupdate")
                # update
                xbmc.executebuiltin("XBMC.Notification(OpenView Update,New Update detected,3000,"")")
                xbmc.executebuiltin("XBMC.Notification(OpenView Update,Updating...,3000,"")")
                print "OV - new update detected"
                update()
            if newupdate == False:
                print "OV - no new update detected"
        if updateflag == False:
            print "OV - no update flag set"

    return



