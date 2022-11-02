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
import file_system_tasks
import sched

s = sched.scheduler(time.time, time.sleep)



from importlib import reload
reload(logging)

logging.basicConfig(level = logging.INFO, 
                    filename =Log.get_log_path(),
                    format = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s')

#connect to local and cloud(RDS) databases
try:
    rds_connection=rds.RDS() 
    local_connection=rds.Local()
    
    if(isinstance(rds_connection,rds.RDS) and isinstance(local_connection,rds.Local)):
        logging.info('local and remote db connections established')
        #do these tasks just at the start of the deployment
        #ema_db.upload_fixed_tables(local_connection,rds_connection)
        dep_data.upload_dep_data_table(rds_connection)
except:
    print('cannot upload fixed data. Exception occured')
    logging.error('cannot make connections to the databases.')


#how frequent we upload data (in seconds)
file_freq=3.17*60*60
def upload_files(sc):
    try:
        reload(logging)
        logging.basicConfig(level = logging.INFO, 
                        filename =Log.get_log_path(),
                        format = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s')
        
        sleep_time=file_freq
        print('in upload_files()')
        logging.info('starting the upload_files() function')
        try:
            ts_start=time.time()
            
            s3_upload.upload_files()
            
            ts_end=time.time()
            #elapsed time in seconds
            elapsed=(ts_end-ts_start)
            sleep_time=file_freq-elapsed
        except Exception as e:
            print('Exception in controller ' + str(e))
            logging.error('Exception in controller upload_files() function'+str(e))
        sc.enter(file_freq, 1, upload_files, (sc,))
    except Exception as e:
        logging.error("Exception in controller upload_files() function "+str(e))
    finally:
        sc.enter(file_freq, 1, upload_files, (sc,))


upload_freq=2*60*60
def upload_db(sc):
    try:
        reload(logging)

        logging.basicConfig(level = logging.INFO, 
                        filename =Log.get_log_path(),
                        format = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s')
    
        print('in upload_db()')
        logging.info('starting the upload_db() function')
        
        print('uploading data to RDS db...')
        sleep_time=upload_freq
        rds_connection=rds.RDS() 
        local_connection=rds.Local()
        try:
            if(isinstance(rds_connection,rds.RDS) and isinstance(local_connection,rds.Local)):
                logging.info('local and remote db connections established')
                ts_start=time.time()
                
                #upload M2G entries to RDS
                '''
                print('uploading m2g data...')
                try:
                    rds_connection=rds.RDS() 
                    local_connection=rds.Local()
                    #m2g.upload_missing_entries(rds_connection)
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    logging.error("in controller uploading m2g entries to rds" + str(e))
                '''
                    
                #upload EMA tables to RDS
                #ema_db.upoload_missing_data_ts(rds_connection,local_connection,'ema_data')
                print('uploading reward_data table...')
                logging.info('uploading reward_data table...')
                try:
                    rds_connection=rds.RDS() 
                    local_connection=rds.Local()
                    ema_db.upload_unuploaded_rows(rds_connection,local_connection,'reward_data')
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    logging.error("in controller uploading data to reward_data in RDS "+str(e))
                    
                print('uploading ema_storing_data table...')
                logging.info('uploading ema_storing_data table...')
                try:
                    rds_connection=rds.RDS() 
                    local_connection=rds.Local()
                    ema_db.upload_unuploaded_rows(rds_connection,local_connection,'ema_storing_data')
                except Exception as e:
                    print('Exception in controller ' + str(e))
                    logging.error("in controller uploading data to ema_storing_data in RDS "+str(e))

                '''
                print('uploading m2g missing data...')    
                try:
                    missing_data.insert_missing_M2G(rds_connection) 
                except Exception as e:
                    print('Exception in controller ' + str(e))
                '''   
                
                
            
                ts_end=time.time()
                #elapsed time in seconds
                elapsed=(ts_end-ts_start)
                sleep_time=upload_freq-elapsed
        except Exception as e:
            print('Exception in controller ' + str(e))
            logging.error("in controller uploading data to RDS "+str(e))
    except Exception as e:
        logging.error("in controller uploading data to RDS "+str(e))
    finally:
        sc.enter(upload_freq, 1, upload_db, (sc,))
           
#frequency to create missing data reports in seconds
missing_data_freq=3*60*60
def log_missing_data(sc):
    
    try:
        reload(logging)
        logging.basicConfig(level = logging.INFO, 
                    filename =Log.get_log_path(),
                    format = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s')
    
        ts_start=time.time()
        dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
        print(dep_id)
        print('creating ema_storing_data and reward_data missing logs...')
        logging.info('creating ema_storing_data and reward_data missing logs...')
        missing_data.insert_missing_data(rds_connection,local_connection,'reward_data','missing_reward_data','TimeSent')
        missing_data.insert_missing_data(rds_connection,local_connection,'ema_storing_data','missing_ema_storing_data','time')
        print('done uploading missing data rows')
       
        ts_end=time.time()
        #elapsed time in seconds
        elapsed=(ts_end-ts_start)
        sleep_time=missing_data_freq-elapsed  
    except Exception as e:
        logging.error("Exception in log_missing_data "+str(e))
    finally:
        sc.enter(missing_data_freq, 1, log_missing_data, (sc,))
    
#start tasks  
s.enter(file_freq, 1, upload_files, (s,))
s.enter(missing_data_freq, 1,log_missing_data, (s,))
s.enter(upload_freq, 1, upload_db, (s,))
s.run()


