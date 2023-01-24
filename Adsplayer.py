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
    print("Key",key)
    print("value",value) 
    return key, value

'''with open("DurationFile.txt") as fd:    
    d = dict(get_pair(line) for line in fd)
fd.close()

print("Duration file #", d)



f = open(r'AdsFile.txt', 'r' )
# e.g., f = open("data2.txt")
mode = f.read()
f.close()'''

    
# Test Code
count =0 

print("mode from file:", mode)



while True:
    # play media one by one
   
    print("WHILE media diles", media_files)
    f = open('/home/pi/Downloads/Schduletest/AdsFile.txt', 'r' )
# e.g., f = open("data2.txt")
    mode = f.read()
    f.close()
    if mode == 'BS':
        current_mode = mode
        media_prefix = current_mode + '-'
        print("BS prefix",media_prefix)
        prefix = media_prefix
        print(prefix + '------------------------')
    elif mode == 'BSR':
        current_mode = mode
        weather_prefix1 = open('/home/pi/Downloads/Schduletest/weatherFile.txt','r')
        weather_prefix = weather_prefix1.read()
        weather_prefix1.close()
        media_prefix = current_mode + '-'+weather_prefix
        print("BS prefix",media_prefix)
        prefix = media_prefix
        print(prefix + '------------------------')
        
    elif mode == ' ':
        current_mode = mode_default+ '-'
    print("current_mode:", current_mode)
    
    
        # update media prefix
        
    #media_files = [os.path.join('/home/pi/Downloads/Schduletest/media', file) for file in sorted(os.listdir('/home/pi/Downloads/Schduletest/media')) if file.startswith(prefix)]
    #media_index = 0
    #media_size = len(media_files)
        #print("media_files  :", media_files)

        # update earlier response with current response
        

    print('STARTING  playads')
        
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$44
    # update media prefix
    
    media_files = [os.path.join('/home/pi/Downloads/Schduletest/media', file) for file in sorted(os.listdir('/home/pi/Downloads/Schduletest/media')) if file.startswith(prefix)]
    media_index = 0
    media_size = len(media_files)
    print("media_SIZE  :", media_size)

    # update earlier response with current response
    #previous_mode = current_mode
# $$$$$$$$$$$$$$$$$$$$$$$$$$
    
    
    sleep(5)
    if media_files:
        with open("/home/pi/Downloads/Schduletest/DurationFile.txt") as fd:    
            d = dict(get_pair(line) for line in fd)
        fd.close()

        print("Duration file #", d)



        f = open('/home/pi/Downloads/Schduletest/AdsFile.txt', 'r' )
        # e.g., f = open("data2.txt")
        mode = f.read()
        if mode != '':
            current_mode = mode
        f.close()
        print("Current_Mode#", current_mode)




        print("media file to PLAY #",media_files[media_index],datetime.now())
        for i in media_files:
            sleep(5)
            videopath = i
            if videopath.split('.')[-1] != 'tmp':
                for key,value in d.items():
                    print("KEY #", key)
                    print("VALUE #", value)
                    newkey = os.path.join('/home/pi/Downloads/Schduletest/media/' + key)
                    print("newkey", newkey)
                    print("mediafile", i)
                    if (newkey == i):
                        print("matched", key, '#', value)
                        sleepx = int(value) + 1
                        print("sleepx #", sleepx)
                        #sleep(int(value)+1)
                        
                if videopath.split('.')[-1] == 'mp4':
                    player = subprocess.Popen(['omxplayer',videopath],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=False)
                
                    player.stdin.flush()
                    sleep(sleepx)
                #{'BS-11111.jpg': '15', 'BS-01-GossipGirl.mp4': '10', 'BS-11.mp4': '10'}
                elif videopath.split('.')[-1] == 'jpg':
                    play = subprocess.Popen(args=["feh",videopath, "-Y", "-B black", "-F", "-Z", "-x"])
                    sleep(sleepx)
                    play.terminate()
                    
            #sleep(11)
        print("EDN")
        #playProcess.stdin.write('q')
        media_index = (media_index + 1) % media_size
    else :
        print("essssssssssssssss")
        play = subprocess.Popen(args=["feh","black.png", "-Y", "-B black", "-F", "-Z", "-x"])
        sleep(5)
        play.terminate()
    print('While completed')

    
    # Test code START 
    count = count + 1
    if count == 3:
        break
    # Test code END
        
        #subprocess.call(command, shell=False)