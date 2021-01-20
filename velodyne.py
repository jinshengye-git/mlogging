#!/usr/bin/env python
# coding: utf-8

# # import modules 
# Necesssry packages:
# - pycurl
# - io / StringIO
# - urllib (python3) / urllib2 (python2)
# - json
# - time(for controling the time delay)

# In[ ]:


import pycurl
try:
	from io import BytesIO
except ImportError:
	from StringIO import StringIO as BytesIO
try:
	from urllib.parse import urlencode
except ImportError:
	from urllib import urlencode

import urllib.request #for python3
# import urllib2 # for python2
import json
import time
from mymath.my_math import severity

# Setup the Base URL of velodyne, we have the velodyne ip address on PC network by default is:
# 
# `192.168.1.201`
# if you want to setup the ip address of velodyne you many use the information on 
# 
# https://greenvalleyintl.com/wp-content/uploads/2019/02/Velodyne-LiDAR-VLP-16-User-Manual.pdf
# 
# the ip address `192.168.1.100` we have on OS named 'Velodnye' or sth. is the ip of PC on Velodyne's network.

# In[ ]:


Base_URL='http://192.168.1.201/cgi'



# To get the status of Laser and rpm number

# In[ ]:


try:
	while True:
		time.sleep(2)
		response = urllib2.urlopen(Base_URL+'status.json')
    	if response:
	    	status = json.loads(response.read())
	    	print ("Sensor laser is " + str(status['laser']['state']) + ", motor rpm is " + str(status['motor']['rpm']))
except KeyboardInterrupt:
	#print("Press Ctrl-C to terminate while statement")
    break
except:
    continue


# if you want to change configure values:

# In[ ]:

"""
def sensor_do(s, url, pf, buf):
	s.setopt(s.URL, url)
	s.setopt(s.POSTFIELDS, pf)
	s.setopt(s.WRITEDATA, buf)
	s.perform()
	rcode = s.getinfo(s.RESPONSE_CODE)
	success = rcode in range(200, 207)
	print('%s %s: %d (%s)' % (url, pf, rcode, 'OK' if success else 'ERROR'))
	return success

sensor = pycurl.Curl()
buffer = BytesIO()
rc = sensor_do(sensor, Base_URL+'reset', urlencode({'data':'reset_system'}), buffer)

if rc:
	time.sleep(10)
	rc = sensor_do(sensor, Base_URL+'setting', urlencode({'rpm':'300'}), buffer)
if rc:
	time.sleep(1)
	rc = sensor_do(sensor, Base_URL+'setting', urlencode({'laser':'on'}), buffer)
if rc:
	time.sleep(10)

"""

