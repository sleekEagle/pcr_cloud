#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:44:47 2019

@author: sleek_eagle
"""

from threading import Timer
import set_env
import s3_upload
import m2g
import ema_db
import dep_data


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
  print('uploading missing data to S3...')
  s3_upload.upload_file_not_in_cloud()
  print('done uploading missing data to S3')
 
#read parameters periodically from parameters.json
def read_params():
    print('reading parameters form parameters.json...')
    #read parameters to environment variables from the parameters.json file
    set_env.read_param()
    global s3_upload_time_s,m2g_upload_time_s
    #the frequency which we upload data to s3
    s3_upload_time_s=int(set_env.get_env('s3_file_upload_time_s'))
    m2g_upload_time_s=int(set_env.get_env('m2g_upload_time_s'))
    print('parameters read from parameters.json.')
    
#upload missing data to m2g database
def m2g_upload_task():
    print("uploading m2g data...")
    m2g.upload_missing_entries()
    print("done uploading m2g data.")
    
#uupload missing data to ema tables
def ema_upload_task():
    print("updating ema data table...")
    ema_db.upoload_missing_data_ts('ema_data')
    print("done updating ema data table.")
    print("updating reward data...")
    ema_db.upload_unuploaded_raws('reward_data')
    print("done updating reward data table.")
    print("updating storing data...")
    ema_db.upload_unuploaded_raws('ema_storing_data')
    print("done updating storing data table.")
 

#read parameter from file
read_params()
read_param_thread=RepeatedTimer(60,read_params)

#schedule recurring tasks
s3_upload_thread=RepeatedTimer(s3_upload_time_s,s3_upload_task)
m2g_upload_thread=RepeatedTimer(m2g_upload_time_s,m2g_upload_task)
ema_upload_thread=RepeatedTimer(600,ema_upload_task)

#upload just once tasks
#upload ema_phones table ones   
ema_db.upload_fixed_tables()
dep_data.upload_dep_data_table()

#read_param_thread.stop()
#set_env.get_env('s3_upload_dirs')


import dep_data
dep_data.upload_zip_file()
