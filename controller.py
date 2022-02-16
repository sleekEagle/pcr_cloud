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
import file_system_tasks
from inspect import currentframe, getframeinfo

#connect to local and cloud(RDS) databases
def connect_dbs():
    rds_connection,local_connection=-1,-1
    try:
        #setting logger
        log_path=Log.get_log_path()
        Log.reset_logger()
        Log.set_logger(log_path)
        
        Log.write_info("trying to connect to RDS")
        rds_connection=rds.RDS() 
        Log.write_info("connected to RDS successfully")
        Log.write_info("trying to connect to local DB")
        local_connection=rds.Local()
        Log.write_info("Local DB connection successful")
        
        if(isinstance(rds_connection,rds.RDS) and isinstance(local_connection,rds.Local)):
            #do these tasks just at the start of the deployment
            #ema_db.upload_fixed_tables(local_connection,rds_connection)
            dep_data.upload_dep_data_table(rds_connection)
    except:
        print('cannot upload fixed data. Exception occured')
        Log.write_error("Error connecting to local/cloud DB")
    return rds_connection,local_connection

#how frequent we upload data (in seconds)
freq=2*60*60
def upload_data():
    print('in upload_data()')
    Log.write_info("upload_data() of controller.py starting uploading data")
    while(True):
        #setting logger
        log_path=Log.get_log_path()
        Log.reset_logger()
        Log.set_logger(log_path)
        
        print('uploading data...')
        sleep_time=freq
        try:
            if(isinstance(rds_connection,rds.RDS) and isinstance(local_connection,rds.Local)):
                ts_start=time.time()
                #upload files to s3
                print('uploading s3 files...')
                Log.write_info("getting ready to upload files to S3")
                rds_connection,local_connection = connect_dbs()
                try:
                    not_uploaded=s3_upload.upload_file_not_in_cloud()
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    Log.write_error("Error in uploading files to S3")

                #upload M2G entries to RDS
                print('uploading m2g data...')
                Log.write_info("getting ready to upload M2G data")
                rds_connection,local_connection = connect_dbs()
                try:
                    rds_connection=rds.RDS() 
                    local_connection=rds.Local()
                    m2g.upload_missing_entries(rds_connection)
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    Log.write_error("Error in uploading M2G data")
                #upload EMA tables to RDS
                #ema_db.upoload_missing_data_ts(rds_connection,local_connection,'ema_data')
                print('uploading reward_data table...')
                Log.write_info("getting ready to upload reward_data table ")
                rds_connection,local_connection = connect_dbs()
                try:
                    rds_connection=rds.RDS() 
                    local_connection=rds.Local()
                    ema_db.upload_unuploaded_rows(rds_connection,local_connection,'reward_data')
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    Log.write_error("Error in uploading reward_data table")
                    
                print('uploading ema_storing_data table...')
                Log.write_info("getting ready to upload ema_storing_data table")
                rds_connection,local_connection = connect_dbs()
                try:
                    rds_connection=rds.RDS() 
                    local_connection=rds.Local()
                    ema_db.upload_unuploaded_rows(rds_connection,local_connection,'ema_storing_data')
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    Log.write_error("Error in uploading ema_storing_data table")
                
            
                #upload stats about data missing from the cloud
                print('uploading s3 files missing data...')
                try:
                    missing_data.insert_missing_files_row(rds_connection,not_uploaded)
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    
                print('uploading m2g missing data...')    
                try:
                    missing_data.insert_missing_M2G(rds_connection) 
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    
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


    

