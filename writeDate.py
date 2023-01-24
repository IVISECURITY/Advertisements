#import datetime
#with open('dateInfo.txt','a') as outFile:
#    outFile.write('\n' + str(datetime.datetime.now()))
    

import requests as req
import os
import shutil
import subprocess
import wget
import geocoder
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Process some values.')
parser.add_argument('deviceId', 
                    help='an integer for the accumulator')
parser.add_argument('deviceMode', 
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
deviceId = args.deviceId
deviceMode = args.deviceMode
    # global previous_response, media_files, media_index, media_size, media_prefix
media_prefix = str(deviceMode)+'-'
mode = str(deviceMode)
print("media_prefix start:", media_prefix)
getApi = 'http://usmgmt.iviscloud.net:777/ProximityAdvertisement/getAdsUpdateInfo/?deviceId='+ str(deviceId)
current_response = req.get(getApi).json()
print(current_response)

if current_response['f_deviceMode']:
    # update media prefix
    media_prefix = current_response['f_deviceMode'] + '-'
    mode = current_response['f_deviceMode']

# # update invocation interval
# invocation_interval = current_response['f_deviceCallFreq']

# extract the root path of the media files
root_path = current_response['f_path']

# download media files and store it in temporary directory
for lst in current_response["ads_list"]:
    video_path = os.path.join(root_path, lst['f_ads'])
    print("video_path:", video_path)
    if lst['f_statusList'][0] == 'A':
        
        
        wget.download(video_path, out='/home/pi/Downloads/Schduletest/media/' + lst['f_ads'])
        with open('/home/pi/Downloads/Schduletest/DurationFile.txt','a') as outFile0:
            duration = lst['f_ads'] + '#' + lst['fdurationList']
            print("duration:", duration)
            outFile0.write(duration)
            outFile0.write('\n')
            outFile0.close()    
            print("Wrote to file-0")
        
        #wget.download('http://usmgmt.iviscloud.net:444/ivis-us-allsiteimages/QRCode/1001/BS-11111.jpg', out='/home/pi/Downloads/Schduletest/media/' + lst['f_ads'])
    elif lst['f_statusList'][0] == 'R':
        if os.path.exists('/home/pi/Downloads/Schduletest/media/' + lst['f_ads']):
            os.remove('/home/pi/Downloads/Schduletest/media/' + lst['f_ads'])

                                # update media list with existing folder
print("TEST STARTS")
# prefix = media_prefix + ('' if media_prefix == 'BS-' else weather_prefix)
prefix = media_prefix
print(prefix)
media_files = [os.path.join('/home/pi/Downloads/Schduletest/media', file) for file in sorted(os.listdir('/home/pi/Downloads/Schduletest/media')) if
               file.startswith(prefix)]

media_index = 0
media_size = len(media_files)

# update sunc status to server
req.post('http://usmgmt.iviscloud.net:777/ProximityAdvertisement/setAdsUpdateInfo/?deviceId=120', 'Synced')

# update earlier response with current response
previous_response = current_response

#open global file in writing mode

print("Writing to file")
#AdsModeFile = open('AdsFile.txt','w')
#AdsModeFile.write(mode)
#AdsModeFile.close()

with open('/home/pi/Downloads/Schduletest/AdsFile.txt','w') as outFile1:
    outFile1.write(mode)
    outFile1.close()    
print("Wrote to file-1")

import datetime
with open('/home/pi/Downloads/Schduletest/dateInfo.txt','a') as outFile2:
    outFile2.write('\n' + str(datetime.datetime.now()))
print("Wrote to file-2")
