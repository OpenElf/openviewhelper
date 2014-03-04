#!/usr/bin/python

############### Imports ################################################

import sys,os
import xbmc,xbmcplugin,xbmcgui,xbmcaddon

########################################################################



# define some paths

datapath = '/home/pi/.xbmc/userdata/addon_data/plugin.video.openviewportal/'
softwarekeypath = os.path.join(datapath, 'softwarekey')

# if the directories are not in place then make them
 
if not os.path.exists(datapath): os.makedirs(datapath)

# Extract serial from cpuinfo file

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

# create softwarekey

def getsoftwarekey():

        hardwarekey = getserial()
                
# if the software key is not present then create it in SD file

        if os.path.isfile(softwarekeypath):
            f = open(softwarekeypath,'r+')
        else:              
            f = open(softwarekeypath, 'w+')
            f.write(hardwarekey)
            f.close
            f = open(softwarekeypath,'r+')

        softwarekey = f.read()
        f.close()

        return softwarekey

def powerdown():

        command = "/usr/bin/sudo /sbin/poweroff"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

        return

# verify hardware to sofware

hardwarekey = getserial()
softwarekey = getsoftwarekey()

if hardwarekey != softwarekey:
#           incrementwipeout() 
        dialog = xbmcgui.Dialog()
        ok=dialog.ok('[B]THIS SD CARD IS INVALID IN THIS UNIT[/B]', 'Did you put the wrong SD card into the wrong OpenView' ,'unit? OpenView SD cards only work in their original','OpenView unit. Click OK to safely power down.')
       
        powerdown()

           