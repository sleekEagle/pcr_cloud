#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 10:10:49 2021

@author: sleekeagle
"""

import rds
import datetime
import slack
import time
import threading
import s3_functions
import file_system_tasks
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from threading import Timer

#read the monitored and ignored deployment IDs from jason file
def get_dep_ids():
    ids=file_system_tasks.get_parameters("dep_ids.json")
    monitored_dep_ids=ids['monitored'].split(',')
    ignored_dep_ids=ids['ignored'].split(',')
    return monitored_dep_ids,ignored_dep_ids

#time threshold in seconds if exceeded should be notified via slack
threshold=2*60*60

#frequency where the tasks are executed
hb_freq=2*60*60
def monitor_hb():
    while(True):
        try:
            sleep_time=hb_freq
            ts_start=time.time()
            monitored_dep_ids,ignored_dep_ids=get_dep_ids()
            rds_connection=rds.RDS() 
            dep_ids=rds_connection.get_unique_values('heart_beat','dep_id')
            valid_dep_ids=[d[0] for d in dep_ids if ((str(d[0]) in monitored_dep_ids) and (str(d[0]) not in ignored_dep_ids))]
            
            for dep_id in valid_dep_ids:
                last_entry=rds_connection.get_last_entry('heart_beat',dep_id)
                last_updated_ts=last_entry[0][-1]
                current_ts=rds_connection.get_ts()[0][0]
                #get the time since last heart beat in seconds
                time_diff=(current_ts-last_updated_ts).total_seconds()
                #print("current ts = " + str(current_ts))
                #print("last ts = " + str(last_updated_ts))
                #print(str(dep_id)+" " + str(time_diff)) 
                #print("_______")
                if(time_diff>threshold):
                    message="No heartbeat detected for deployment "+str(dep_id)+". It may be offline"
                    slack.post_slack(message,'dep-monitor')
                ts_end=time.time()
                elapsed=(ts_end-ts_start)
                sleep_time=hb_freq-elapsed
        except:
            print('Exception in monitor_hb() ')
        if(sleep_time>60):
            time.sleep(int(sleep_time))
            

newdp_freq=3*60*60
def detect_new_deps():
    while(True):
        try:
            sleep_time=newdp_freq
            ts_start=time.time()
            monitored_dep_ids,ignored_dep_ids=get_dep_ids()
            rds_connection=rds.RDS()
            dep_ids=rds_connection.get_unique_values('heart_beat','dep_id')
            new_dep_ids=[d[0] for d in dep_ids if ((str(d[0]) not in monitored_dep_ids) and (str(d[0]) not in ignored_dep_ids))]
            new_dep_ids_str=" , ".join([str(id) for id in new_dep_ids])
            if(len(new_dep_ids)>0):
                message="New deployment/s detected. There id/s : " + new_dep_ids_str
                slack.post_slack(message,'dep-monitor')
            ts_end=time.time()
            elapsed=(ts_end-ts_start)
            sleep_time=newdp_freq-elapsed   
        except:
            print('Exception in detect_new_deps() ')
        if(sleep_time>60):
            time.sleep(int(sleep_time))   

def slack_dep_RDS_stats(dep_num):
    path=dep_num+"/cloud_logs/missing_data/"
    r=s3_functions.get_files_in_dir(path,1000)
    files=[item.split('/')[-1].split('.')[0] for item in r]
    dep=path.split('/')[0]  
    msg='*** deployment '+str(dep) +' ***\n'
    if(len(files)>0):
        files.sort(key=lambda data:datetime.datetime.strptime(data,"%d-%m-%Y"))
        last_date=files[-1]
        last_file=path+last_date+'.log'
        
        lines=s3_functions.read_lines_from_txt_file(last_file)
        
        #find the last occurance of the logs on ema and reward data tables
        last_ema_line=-1
        for i,line in enumerate(lines):
            if("ema_storing_data table" in line):
                last_ema_line=i
                continue
            
        last_reward_data=lines[last_ema_line-1].replace('\r','').replace("'",'')
        last_ema_line=lines[-1].replace('\r','').replace("'",'')
        
        msg+='*table name,last_update_date,#local rows,#cloud rows*\n'
        msg+='reward_data table, '+last_reward_data+'\n'
        msg+='ema_storing_data table, '+last_ema_line+'\n'
    else:
        msg+='no log files uploaded'
    slack.post_slack(msg,'dep-stats')

def RDS_stats():
    monitored_dep_ids,ignored_dep_ids=get_dep_ids()
    for dep_id in monitored_dep_ids:
        slack_dep_RDS_stats(dep_id)
    
        x=datetime.datetime.today()
        #y=x.replace(day=x.day+1, hour=11, minute=13, second=0, microsecond=0)
        y=x.replace(day=x.day, hour=x.hour, minute=x.minute+1, second=x.second, microsecond=0)
        delta_t=y-x
        secs=(delta_t.total_seconds()+1)
        t=Timer(secs,RDS_stats)
        t.start()
        
threading.Thread(target=monitor_hb).start()
threading.Thread(target=detect_new_deps).start()
#threading.Thread(target=RDS_stats).start()
RDS_stats()        
    
    
    
    
    
    
    
    
