#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 10:10:49 2021

@author: sleekeagle
"""

import rds
import os
import datetime
import slack
import time
import threading
import s3_functions


monitored_dep_ids=[3162022]
non_monitored_dep_ids=[21,6092021,7132021,8022021,10282021,10,11111,11112,54321,5062022,5122022,1172022,2182022]
#time threshold in seconds if exceeded should be notified via slack
threshold=2*60*60
#frequency where the tasks are executed
freq=2*60*60


def monitor_hb():
    try:
        rds_connection=rds.RDS() 
        dep_ids=rds_connection.get_unique_values('heart_beat','dep_id')
        valid_dep_ids=[d[0] for d in dep_ids if ((d[0] in monitored_dep_ids) and (d[0] not in non_monitored_dep_ids))]
        
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
    except:
        print('Exception in monitor_hb() ')
            


def detect_new_deps():
    try:
        rds_connection=rds.RDS()
        dep_ids=rds_connection.get_unique_values('heart_beat','dep_id')
        new_dep_ids=[d[0] for d in dep_ids if ((d[0] not in monitored_dep_ids) and (d[0] not in non_monitored_dep_ids))]
        new_dep_ids_str=" , ".join([str(id) for id in new_dep_ids])
        if(len(new_dep_ids)>0):
            message="New deployment/s detected. There id/s : " + new_dep_ids_str
            slack.post_slack(message,'dep-monitor')
            
    except:
        print('Exception in detect_new_deps() ')
        

def start_monitor():
    while(True):
        monitor_hb()
        detect_new_deps()
        time.sleep(int(freq))
        

#threading.Thread(target=start_monitor).start()

#connect to S3


def slack_dep_RDS_stats(dep_num):
    path=dep_num+"/cloud_logs/missing_data/"
    r=s3_functions.get_files_in_dir(path,1000)
    files=[item['Key'].split('/')[-1].split('.')[0] for item in r['Contents']]
    
    files.sort(key=lambda data:datetime.datetime.strptime(data,"%d-%m-%Y"))
    last_date=files[-1]
    last_file=path+last_date+'.log'
    
    lines=s3_functions.read_lines_from_txt_file(last_file)
    
    #find the last occurance of the logs on ema and reward data tables
    last_ema_line,last_reward_line=-1,-1
    for i,line in enumerate(lines):
        if("ema_storing_data table" in line):
            last_ema_line=i
            continue
        if("reward_data table" in line):
            last_reward_line=i
            continue
        
    dep=path.split('/')[0]
    last_reward_data=lines[last_ema_line-1].replace('\r','').replace("'",'')
    last_ema_line=lines[-1].replace('\r','').replace("'",'')
    msg='*** deployment '+str(dep) +' ***\n'
    msg+='*table name,last_update_date,#local rows,#cloud rows*\n'
    msg+='reward_data table, '+last_reward_data+'\n'
    msg+='ema_storing_data table, '+last_ema_line+'\n'
    slack.post_slack(msg,'dep-stats')
        
    
    
    
        
    
    
    
    
    
    
    
    
