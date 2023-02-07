#import asyncio as aio
import requests as req
import os
import shutil
import subprocess
import wget
import geocoder
from datetime import datetime
#from omxplayer.player importqq OMXPlayer
from pathlib import Path
from time import sleep


media_files = [],
media_index = 0,
media_size = 0
media_prefix = ''
weather_prefix = ''

previous_mode=''
mode_default='BS'
mode=''


#open global file in reading mode


d={}
def get_pair(line):
    key, sep, value = line.strip().partition("#")
    return key, value

# Test Code
cnt =0
count=''

while True:
    # play media one by one
   
    f = open('/home/pi/Downloads/Advertisements/AdsFile.txt', 'r' )
    mode = f.read()
    f.close()
    print("Mode from AdsFile:", mode)
    if mode == 'BS':
        current_mode = mode
        media_prefix = current_mode + '-'
        print("prefix",media_prefix)
        prefix = media_prefix
    if mode == 'BSR':
        current_mode = mode
        weather_prefix1 = open('/home/pi/Downloads/Advertisements/weatherFile.txt','r')
        weather_prefix = weather_prefix1.read()
        weather_prefix1.close()
        media_prefix = current_mode + '-'+weather_prefix
        print("prefix",media_prefix)
        prefix = media_prefix
    if mode == 'ODR':
        print("Check for ODR")
        current_mode = mode
        weather_prefix1 = open('/home/pi/Downloads/Advertisements/weatherFile.txt','r')
        weather_prefix = weather_prefix1.read()
        weather_prefix1.close()
        media_prefix = current_mode + '-'+weather_prefix
       
        file = open('/home/pi/Downloads/Advertisements/person.txt', 'r' )
        count = file.read()
        file.close()
        count = count.split('#')[-1]
        
        prefix = media_prefix+'P'+count
        print("*** ODR prefix",prefix)
        
    if mode == ' ':
        current_mode = mode_default+ '-'
  #  print("current_mode:", current_mode)
    
  
 #   print('STARTING  playads')

    # update media prefix
    
    media_files = [os.path.join('/home/pi/Downloads/Advertisements/media', file) for file in sorted(os.listdir('/home/pi/Downloads/Advertisements/media')) if file.startswith(prefix)]
    media_index = 0
    media_size = len(media_files)
#    print("media_SIZE  :", media_size)
    
    sleep(1)
    if media_files:
        with open("/home/pi/Downloads/Advertisements/DurationFile.txt") as fd:    
            d = dict(get_pair(line) for line in fd)
        fd.close()

        #print("Duration file #", d)



        f = open('/home/pi/Downloads/Advertisements/AdsFile.txt', 'r' )
        # e.g., f = open("data2.txt")
        mode = f.read()
        if mode != '':
            current_mode = mode
        f.close()
        
        #print("media file to PLAY #",media_files[media_index],datetime.now())
        for i in media_files:
            sleep(2)
            videopath = i
            if videopath.split('.')[-1] != 'tmp':
                for key,value in d.items():
                   # print("KEY #", key)
                   # print("VALUE #", value)
                    newkey = os.path.join('/home/pi/Downloads/Advertisements/media/' + key)
                   # print("newkey", newkey)
                   # print("mediafile", i)
                    if (newkey == i):
                        print("Ads_played_data =", key ,' : ' ,datetime.now())
                        sleepx = int(value) + 1
                    #    print("sleepx #", sleepx)
                        #sleep(int(value)+1)
                dtime = str(datetime.now())
                        
                if videopath.split('.')[-1] == 'mp4':
                    player = subprocess.Popen(['omxplayer',videopath],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=False)
                    print("playing...!",current_mode)
                    player.stdin.flush()
                    sleep(sleepx)
                #{'BS-11111.jpg': '15', 'BS-01-GossipGirl.mp4': '10', 'BS-11.mp4': '10'}
                elif videopath.split('.')[-1] == 'jpg':
                    play = subprocess.Popen(args=["feh",videopath, "-Y", "-B black", "-F", "-Z", "-x"])
                    sleep(sleepx)
                    play.terminate()
                    
                #Ads_played_data = key , datetime.now()
  
        media_index = (media_index + 1) % media_size
    else :
        print("essssssssssssssss")
        play = subprocess.Popen(args=["feh","/home/pi/Downloads/Advertisements/black.png", "-Y", "-B black", "-F", "-Z", "-x"])
        sleep(5)
        play.terminate()
    print('*****************While completed*************')

    
    # Test code START 
    cnt = cnt + 1
    if cnt == 3:
        break
    # Test code END
        
        #subprocess.call(command, shell=False)