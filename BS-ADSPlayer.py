import asyncio as aio
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
#mode_default='BS'
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



f = open('AdsFile.txt', 'r' )
# e.g., f = open("data2.txt")
mode = f.read()
f.close()'''

    


print("mode from file:", mode)



while True:
    # play media one by one
   
    print("WHILE media diles", media_files)
    f = open('AdsFile.txt', 'r' )
# e.g., f = open("data2.txt")
    mode = f.read()
    f.close()
    if mode == '':
        current_mode = mode
    else:
        current_mode = mode_default
        print("current_mode:", current_mode)
    
    if previous_mode != current_mode:
        # update media prefix
        media_prefix = current_mode + '-'
        print("not cond prefix",media_prefix)
        prefix = media_prefix
        print(prefix + '------------------------')
        media_files = [os.path.join('/home/pi/Downloads/Schduletest/media', file) for file in sorted(os.listdir('/home/pi/Downloads/Schduletest/media')) if file.startswith(prefix)]
        media_index = 0
        media_size = len(media_files)
        #print("media_files  :", media_files)

        # update earlier response with current response
        previous_mode = current_mode

    print('STARTING  playads')
        
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$44
    # update media prefix
    media_prefix = current_mode + '-'
    print("not cond prefix",media_prefix)
    prefix = media_prefix
    print(prefix + '------------------------')
    media_files = [os.path.join('/home/pi/Downloads/Schduletest/media', file) for file in sorted(os.listdir('/home/pi/Downloads/Schduletest/media')) if file.startswith(prefix)]
    #media_index = 0
    media_size = len(media_files)
    print("media_SIZE  :", media_size)

    # update earlier response with current response
    #previous_mode = current_mode
# $$$$$$$$$$$$$$$$$$$$$$$$$$
    
    
    sleep(5)
    if media_files:
        with open("DurationFile.txt") as fd:    
            d = dict(get_pair(line) for line in fd)
        fd.close()

        print("Duration file #", d)



        f = open('AdsFile.txt', 'r' )
        # e.g., f = open("data2.txt")
        mode = f.read()
        if mode != '':
            current_mode = mode
        f.close()
        print("Current_Mode#", current_mode)





        print("media file to PLAY #",media_files[media_index],datetime.now())
        videopath = media_files[media_index]
        if videopath.split('.')[-1] != 'tmp':
            player = subprocess.Popen(['omxplayer',videopath],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=False)
            
            player.stdin.flush()
            #{'BS-11111.jpg': '15', 'BS-01-GossipGirl.mp4': '10', 'BS-11.mp4': '10'}
            for key,value in d.items():
                print("KEY #", key)
                print("VALUE #", value)
                newkey = os.path.join('/home/pi/Downloads/Schduletest/media/' + key)
                print("newkey", newkey)
                print("mediafile", media_files[media_index])
                if (newkey == media_files[media_index]):
                    print("matched", key, '#', value)
                    sleep(int(value)+1)
            
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

        
        #subprocess.call(command, shell=False)
