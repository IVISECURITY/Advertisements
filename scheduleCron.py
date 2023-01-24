from crontab import CronTab

import requests as req
#import os
#import shutil
#import subprocess
import wget
#import geocoder
from datetime import datetime

import socket
deviceName = socket.gethostname()
deviceIPAddr = socket.gethostbyname(deviceName)
exIP = socket.gethostbyname_ex(deviceName)
a = socket.gethostbyaddr(deviceName)
# Importing OS module
import os
# printing
print("The HOME directory is :")
# Python get home directory using os module
userName = str(os.path.expanduser("~")).split('/')[-1]
print(userName)
print("name:",deviceName)
print("IPAddr:",deviceIPAddr)
#print("Ex IPAddr:",exIP)
#print(a)



# For the first time  get the frequency and set the CroTab timeInterval 
#current_response = req.get('http://usmgmt.iviscloud.net:777/ProximityAdvertisement/getDeviceAdsInfo/?deviceName=+'deviceName').json()
#print("current_response", current_response)

deviceId =120
deviceCallFreq = 1
deviceMode = 'BS'
AdsHours = '8-19'
nonWorkingDays = '1,2,3,4,5,6'
cameraId='IVISUSA1001C2'
weatherAPIKey ='fhsfhueihrewurfeiuwhsjfndsfn'
weatherCallFreq = 30


# update invocation interval
#invocation_interval = current_response['f_deviceCallFreq']
#invocation_interval = deviceCallFreq



my_cron = CronTab(user=userName)
frstcommand = 'python3 /home/pi/Downloads/Schduletest/writeDate.py'+' '+str(deviceId)+' '+deviceMode
command =frstcommand+ ' >> /home/pi/Downloads/Schduletest/log24Jan.txt'
print(command)
job = my_cron.new(command = command)
job.minute.every(deviceCallFreq)
#job.hour(8-9)
#job.day.on(1-6)
my_cron.write()

#weather_interval = 30
my_cron = CronTab(user='pi')
job = my_cron.new(command='python3 /home/pi/Downloads/Schduletest/weather.py >> /home/pi/Downloads/Schduletest/weatherlog.txt')
job.minute.every(weatherCallFreq)
my_cron.write()