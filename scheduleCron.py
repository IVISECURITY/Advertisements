from crontab import CronTab
import requests as req 
from datetime import datetime

import socket
deviceName = socket.gethostname()

# Importing OS module
import os
# Python get home directory using os module
dir = '/home/pi/Downloads/Advertisements'
print("CWD:", dir)
userName = str(os.path.expanduser("~")).split('/')[-1]
print("userName:", userName)
from datetime import datetime
dtime = str(datetime.now())
#userName = 'root'
#Remove exisitng Advertisements CronTabs
my_cron = CronTab(user=userName)
for job in my_cron:  
    print(job, '  ###  ')
#if comment == 'AdsReaderJob':
    my_cron.remove(job)
    my_cron.write()
    

# For the first time  get the device Advertisement Details to set the CroTab(s) 
api = 'http://usmgmt.iviscloud.net:777/ProximityAdvertisement/getDeviceAdsInfo_1_0/?deviceName='+deviceName
current_response = req.get(api).json()

print("current_response", current_response)

siteId = current_response['Device_details']['siteId']
deviceId = current_response['Device_details']['deviceId']
deviceMode = current_response['Device_details']['deviceMode']
cameraId = current_response['Device_details']['cameraId']

#Set Device Call Frequency 
    # Device Ads Manager API call Interval(in minutes)
if current_response['Device_details']['deviceCallFreq'] == None or current_response['Device_details']['deviceCallFreq'] == '' :
    deviceCallFreq = 1
else:
    deviceCallFreq = current_response['Device_details']['deviceCallFreq']
    
#Set Ads Hour window     
adsHours = current_response['Device_details']['adsHours']

startTime,sep,endTime = adsHours.strip().partition("-")

#Set Advertisements Working Days
if current_response['Device_details']['workingDays'] == None or current_response['Device_details']['workingDays'] == '':
    workingDays = str('1,2,3,4,5')   # Mon - 1; Tue - 2 , ...Fri - 5
else:
    workingDays = current_response['Device_details']['workingDays']
    
#Weather Details
    # Weather API call Interval(in minutes)
if current_response['Device_details']['weather_interval'] == None or current_response['Device_details']['weather_interval'] == '' :
    weatherCallFreq = 30
else:
    weatherCallFreq = current_response['Device_details']['weather_interval']
    # Weather API Key 
weatherAPIKey =current_response['Device_details']['weatherApiKey']


# Schedule Jobs using CRONTAB


#Ads Job

AdsCommand =  '/usr/bin/python3 '+dir+'/AdsReader.py'+' '+str(deviceId)+' '+deviceMode
#logfile
dtime = dtime[:10] + '_' +  dtime[20:]
logFile = ' >>'+dir+'/logs/AdsGet'+dtime+'.txt'

AdsJob = AdsCommand+ logFile 
print("AdsJob:", AdsJob)

my_cron = CronTab(user=userName)
job = my_cron.new(command = AdsJob, comment='AdsReaderJob')
job.minute.every(deviceCallFreq)
'''job.hour.every(startTime)
for i in range (int(startTime)+1,int(endTime)+1):
    job.hour.also.on(i)

for j in range(1, 8):
    b,sep1,a = workingDays.strip().partition(",")
    if j==1:
        job.day.on(b)
    else:
        job.day.also.on(b)
    if a=='':
        break
    else:
        j=j+1
        workingDays = a '''
        
my_cron.write()


#Preparing Weather Job

WeatherCommand =  '/usr/bin/python3 '+dir+'/weather.py' #+' '+str(weatherApiKey)
#logfile
logFile = ' >>'+dir+'/logs/Wther'+dtime+'.txt'

WeatherJob = WeatherCommand+ logFile 
print("Weather:", WeatherJob)

my_cron = CronTab(user=userName)
job = my_cron.new(command=WeatherJob, comment='WeatherJob')
job.minute.every(weatherCallFreq)
my_cron.write()



#@reboot sleep 60 && /usr/bin/python3 /home/pi/Downloads/Advertisements/objdet.py >> /home/pi/Downloads/Advertisements/ObjDetectReader2023-02-03_.txt  # ObjDetectJob
# Object Detection Job (which runs only once)

#my_cron = CronTab(user=userName)
#job = my_cron.new(command = AdsplayerJob, comment='AdsplayerJob')
#job.every_reboot()
#my_cron.write()

#ObjDetJob = ObjDetectCommand+ logFile 
#print("ObjDetJob:", ObjDetectCommand)
#@reboot sleep 60 && /usr/bin/python3 /home/pi/Downloads/Advertisements/objdet.py >> /home/pi/Downloads/Advertisements/ObjDetectReader2023-02-03_.txt  # ObjDetectJob
# Object Detection Job (which runs only once)

#my_cron = CronTab(user=userName)
#job = my_cron.new(command = ObjDetectCommand, comment='ObjDetectJob')
#job.minute.every(0)
#job.every_reboot()
#my_cron.write()
 