#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:44:47 2019

@author: sleek_eagle
"""

from threading import Timer
import set_env
import s3_upload


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False





def s3_upload_task():
  print('uploading missing data...')
  s3_upload.upload_file_not_in_cloud()
 
#read parameters periodically from parameters.json
def read_params():
    print('reading parameters form parameters.json...')
    #read parameters to environment variables from the parameters.json file
    set_env.read_param()
    global s3_upload_time_s
    #the frequency which we upload data to s3
    s3_upload_time_s=int(set_env.get_env('s3_file_upload_time_s'))
    

read_params()
read_param_thread=RepeatedTimer(10,read_params)
upload_thread=RepeatedTimer(s3_upload_time_s,s3_upload_task)
#read_param_thread.stop()
#set_env.get_env('s3_upload_dirs')
