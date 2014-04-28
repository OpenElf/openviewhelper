# -*- coding: utf-8 -*-
# This code is to develop my understanding of universal analytics.
# send data to Google Analytics using the Measurement Protocol: 2 parts
# 1) The transport – to where and how you send data, the end point
# 2) The payload – the data you send

import urllib
import urllib2
import random


################################  constants ####################################
VERSION = '1'
UATRACKER = 'UA-49026691-1'
APPNAME = 'OpenView'
APPVERSION = '1.0.11'
ENDPOINT = 'http://www.google-analytics.com/collect'

################################################################################

def client_id():

        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR1234789abcd"

        clientid = cpuserial[-8:] + "-1a05-49e7-b576-2b884d0f825b"

        return clientid


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

def update(category, action, value = "0"):

#        print "OV - this is ua.py"

        payload = ENDPOINT + "?" + \
            "v=" + VERSION + \
            "&tid=" + UATRACKER + \
            "&cid=" + client_id() + \
            "&t=" + "event" + \
            "&ec=" + category + \
            "&ea=" + action + \
            "&el=" + getserial() + \
            "&ev=" + value + \
            "&an=" + APPNAME + \
            "&av=" + APPVERSION + \
            "&z=" + str(random.randint(0, 0x7fffffff))

        try:

                req = urllib2.Request(payload)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                responseUA = urllib2.urlopen(req)
#                w = responseUA.geturl()
#                x = responseUA.getcode()
#                y = responseUA.info()
#                print w
#                print x
#                print y
                
        except:

                print ("OV: UA fail: %s" % payload)

        return



