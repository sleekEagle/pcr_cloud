#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:44:47 2019

@author: sleek_eagle
"""

from threading import Timer
import s3_upload
import m2g
import ema_db
import dep_data
import Log
import logging
import threading
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import rds
import missing_data
import heart_beat
import threading

#connect to local and cloud(RDS) databases
try:
    rds_connection=rds.RDS() 
    local_connection=rds.Local()
    
    if(isinstance(rds_connection,rds.RDS) and isinstance(local_connection,rds.Local)):
        #do these tasks just at the start of the deployment
        ema_db.upload_fixed_tables(local_connection,rds_connection)
        dep_data.upload_dep_data_table(rds_connection)
except:
    print('cannot upload fixed data. Exception occured')

#how frequent we upload data (in seconds)
freq=10*60
def upload_data():
    print('in upload_data()')
    while(True):
        print('uploading data...')
        sleep_time=freq
        try:
            rds_connection=rds.RDS() 
            local_connection=rds.Local()
            if(isinstance(rds_connection,rds.RDS) and isinstance(local_connection,rds.Local)):
                ts_start=time.time()
                #upload files to s3
                s3_upload.upload_file_not_in_cloud()
                #upload M2G entries to RDS
                m2g.upload_missing_entries(rds_connection)
                #upload EMA tables to RDS
                ema_db.upoload_missing_data_ts(rds_connection,local_connection,'ema_data')
                ema_db.upload_unuploaded_rows(rds_connection,local_connection,'reward_data')
                ema_db.upload_unuploaded_rows(rds_connection,local_connection,'ema_storing_data')
            
                #upload stats about data missing from the cloud
                print('uploading missing data...')
                missing_data.insert_missing_files_row(rds_connection)  
                missing_data.insert_missing_M2G(rds_connection)
                missing_data.insert_missing_data(rds_connection,local_connection,'ema_data','missing_ema_data')
                missing_data.insert_missing_data(rds_connection,local_connection,'ema_storing_data','missing_ema_storing_data')
            
                ts_end=time.time()
                #elapsed time in minutes
                elapsed=(ts_end-ts_start)
                sleep_time=freq-elapsed
        except:
            print('Exception in controller')
        if(sleep_time>60):
            time.sleep(int(sleep_time))
            
#frequency to enter heart beat in seconds            
heart_beat_freq=60*1
def manage_heart_beat():
    while(True):
        print('hb')
        try:
            rds_connection=rds.RDS()
            if(isinstance(rds_connection,rds.RDS)):
                res=heart_beat.insert_heart_beat(rds_connection)
        except:
            print('Exception in manage_heart_beat() ')
        time.sleep(heart_beat_freq)


threading.Thread(target=manage_heart_beat).start()
threading.Thread(target=upload_data).start()


    

