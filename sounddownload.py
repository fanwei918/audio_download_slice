#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 15:55:41 2017

@author: weif
"""
import pafy
import pandas as pd
import numpy as np
from pydub import AudioSegment
import soundfile as sf

#%%
#csv_header = ['YTID', 'start_sec', 'end_sec','l1','l2','l3','l4','l5','l6','l7','l8','l9','l10','l11']
#csv_header = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]

#videolist =  pd.read_csv('../balanced_train_segments.csv',skiprows=2, header=None,names = ['id',"start", "end", "0", "1","2","3","4","5","6","7","8","9","10","11","12","13" ])   #skip_blank_lines=5
videolist =  pd.read_csv('../eval_segments.csv',skiprows=2, header=None,names = ['id',"start", "end", "0", "1","2","3","4","5","6","7","8","9","10","11","12","13" ])   #skip_blank_lines=5

(row,col)=videolist.shape

Is_wanted= np.zeros((row,1),dtype=np.bool)

num=0

for i in range(0,row):
    for j in range (3,col):
        if type(videolist.iat[i,j])== str:
            if '/m/07pbtc8' in videolist.iat[i,j]:                
                Is_wanted[i]=True
                         
label='Footsteps'
                    
print(np.sum(Is_wanted))     
                   




data_df=pd.DataFrame([], columns=['name','format','start_sec','end_sec','length','bitrate','address','label'])
num=0

#%%
for i in np.arange(0,row):
    print(i)
    print(Is_wanted[i])
    if Is_wanted[i]==True:
        url = "https://www.youtube.com/watch?v="+videolist.iat[i,0]
        try:
            video=pafy.new(url)
            streams=video.audiostreams        
            k=streams[0]
        except (IOError,OSError,ValueError):
            continue    
        try:
            k.download(filepath= ( str(num) )  )  
        except (IOError,OSError,ValueError):
            continue
        df1=pd.DataFrame([[str(num), k.extension, videolist.iat[i,1], videolist.iat[i,2], video.length, k.bitrate, videolist.iat[i,0],label]], columns=['name','format','start_sec','end_sec','length','bitrate','address','label'])
        data_df=data_df.append(df1)
        num=num+1

#        i_now=i+1 # for restarting from error
        
#data_df.to_csv(label+'_balanced_train.csv')   
data_df.to_csv(label+'_eval.csv')  

#%%
AudioSegment.ffmpeg="/Users/weif/Documents/ffmpeg"
AudioSegment.converter = r"/Users/weif/Documents/ffmpeg"

(row,col)=data_df.shape

for i in range(0,row):

#    filename=data_df.iat[i,0]+'.'+data_df.iat[i,1]
    filename=str(data_df.iat[i,0])
    start_sec = float(data_df.iat[i,2])
    stop_sec =float(data_df.iat[i,3])
    duration = int(stop_sec-start_sec)
    filename1=label+'_2_'+str(duration)+'s_'+str(data_df.iat[i,0])+'.ogg'
    AudioSegment.from_file(filename)[int(1000* start_sec):int(1000*stop_sec)].export(filename1, format ='ogg' )
