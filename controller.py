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
        #ema_db.upload_fixed_tables(local_connection,rds_connection)
        dep_data.upload_dep_data_table(rds_connection)
except:
    print('cannot upload fixed data. Exception occured')

#how frequent we upload data (in seconds)
freq=2*60*60
def upload_data():
    print('in upload_data()')
    while(True):
        print('uploading data...')
        sleep_time=freq
        rds_connection=rds.RDS() 
        local_connection=rds.Local()
        try:
            if(isinstance(rds_connection,rds.RDS) and isinstance(local_connection,rds.Local)):
                ts_start=time.time()
                #upload files to s3
                print('uploading s3 files...')
                try:
<<<<<<< HEAD
                    not_uploaded=s3_upload.upload_files()
=======
                    local_files,cloud_files,not_uploaded=s3_upload.upload_file_not_in_cloud()
>>>>>>> 4de561680309c6b7e15cc1d2562b101573ffe78a
                except Exception as e:
                    print('Exception in controller ' + str(e))

                #upload M2G entries to RDS
                print('uploading m2g data...')
                try:
                    rds_connection=rds.RDS() 
                    local_connection=rds.Local()
                    m2g.upload_missing_entries(rds_connection)
                except Exception as e:
                    print('Exception in controller ' + str(e))
                #upload EMA tables to RDS
                #ema_db.upoload_missing_data_ts(rds_connection,local_connection,'ema_data')
                print('uploading reward_data table...')
                try:
                    rds_connection=rds.RDS() 
                    local_connection=rds.Local()
                    ema_db.upload_unuploaded_rows(rds_connection,local_connection,'reward_data')
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    
                print('uploading ema_storing_data table...')
                try:
                    rds_connection=rds.RDS() 
                    local_connection=rds.Local()
                    ema_db.upload_unuploaded_rows(rds_connection,local_connection,'ema_storing_data')
                except Exception as e:
                    print('Exception in controller ' + str(e))
                
            
                #upload stats about data missing from the cloud
                print('uploading s3 files missing data...')
                try:
                    missing_data.insert_missing_files_row(rds_connection,local_files,cloud_files,not_uploaded)
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    
                #print('uploading m2g missing data...')    
                #try:
                #    missing_data.insert_missing_M2G(rds_connection) 
                #except Exception as e:
                #    print('Exception in controller ' + str(e))
                    
                print('uploading ema_storing_data missing data...')
                try:
                    missing_data.insert_missing_data(rds_connection,local_connection,
                                                     'ema_storing_data',
                                                     'missing_ema_storing_data',
                                                     'time')
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    
                print('uploading reward_data missing data...')
                try:
                    missing_data.insert_missing_data(rds_connection,
                                                     local_connection,
                                                     'reward_data',
                                                     'missing_reward_data',
                                                     'TimeSent')
                except Exception as e:
                    print('Exception in controller ' + str(e))
                
            
                ts_end=time.time()
                #elapsed time in minutes
                elapsed=(ts_end-ts_start)
                print("elapsed time = " +str(elapsed))
                sleep_time=freq-elapsed
        except Exception as e:
            print('Exception in controller ' + str(e))
        if(sleep_time>60):
            time.sleep(int(sleep_time))
            
#frequency to enter heart beat in seconds            
heart_beat_freq=60*30
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


    

