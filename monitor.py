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
import numpy as np
import pandas as pd
import schedule
import datetime
import time
import sched
import json

parameter_path='/home/ubuntu/dep_ids.json'

def add_value_dep_ids(key,value):
    with open(parameter_path, 'r') as f:
        param = json.load(f)[0]

    param[key]+=','+value
    # Serializing json
    json_object = json.dumps([param], indent=4)
    # Writing to sample.json
    with open(parameter_path, "w") as outfile:
        outfile.write(json_object)

#read the monitored and ignored deployment IDs from jason file
def get_dep_ids():
    try:
        ids=file_system_tasks.get_parameters("dep_ids.json")
        monitored_dep_ids=ids['monitored'].split(',')
        ignored_dep_ids=ids['ignored'].split(',')
    except:
        print('Exception in reading monitored dep IDs')
        
    return monitored_dep_ids,ignored_dep_ids

#time threshold in seconds if exceeded should be notified via slack
threshold=2*60*60
#frequency where the tasks are executed
heart_freq=60*30
def monitor_hb(sc):
    print('in monitoring heart beat')
    try:
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
            print("current ts = " + str(current_ts))
            print("last ts = " + str(last_updated_ts))
            print(str(dep_id)+" " + str(time_diff)) 
            print("_______")
            if(time_diff>threshold):
                message="No heartbeat detected for deployment "+str(dep_id)+". It may be offline"
                slack.post_slack(message,'dep-monitor')
    except Exception as e:
        print('Exception in monitor_hb() '+str(e))
    finally:
        sc.enter(heart_freq,1,monitor_hb,(sc,))       

newdp_freq=3*60*60
def detect_new_deps(sc):
    print('detecting new deployments')
    try:
        monitored_dep_ids,ignored_dep_ids=get_dep_ids()
        rds_connection=rds.RDS()
        dep_ids=rds_connection.get_unique_values('heart_beat','dep_id')
        new_dep_ids=[d[0] for d in dep_ids if ((str(d[0]) not in monitored_dep_ids) and (str(d[0]) not in ignored_dep_ids))]
        new_dep_ids_str=" , ".join([str(id) for id in new_dep_ids])
        if(len(new_dep_ids)>0):
            message="New deployment/s detected. There id/s : " + new_dep_ids_str
            slack.post_slack(message,'dep-monitor')
            message="Adding this dep number to the monitored list..."
            slack.post_slack(message,'dep-monitor')
            add_value_dep_ids('monitored',new_dep_ids_str)
    except Exception as e:
        print('Exception in detect_new_deps() '+str(e))

    finally:
        sc.enter(newdp_freq,1,detect_new_deps,(sc,))      

def slack_dep_RDS_stats(dep_num):
    print(dep_num)
    rds_connection=rds.RDS() 
    reward_ncloud,reward_nlocal,reward_ts,ema_ncloud,ema_nloca,ema_tsl=-1,-1,-1,-1,-1,-1
    last_entry=rds_connection.get_last_entry('missing_reward_data',dep_num)
    reward_ncloud,reward_nlocal,reward_ts=-1,-1,-1,
    if(len(last_entry)>0):
        reward_ncloud=last_entry[0][3]
        reward_nlocal=last_entry[0][2]
        reward_ts=last_entry[0][1]
    last_entry=rds_connection.get_last_entry('missing_ema_storing_data',dep_num)
    ema_ncloud,ema_nlocal,ema_ts=-1,-1,-1
    if(len(last_entry)>0):
        ema_ncloud=last_entry[0][3]
        ema_nlocal=last_entry[0][2]
        ema_ts=last_entry[0][1]
    msg='***deployment '+str(dep_num)+'***\n'
    msg+='*table name,ts,#local rows,#cloud rows*\n' 
    if(not(reward_ts==-1)):
        msg+="reward_data \n" + reward_ts[:10]+" \n" + str(reward_nlocal)+" , " + str(reward_ncloud)+"\n"
    else:
        msg+="No data received from reward_data table yet"
    if(not(ema_ts==-1)):
        msg+="ema_storing_data\n" + ema_ts[:10]+"\n" + str(ema_nlocal)+" , " + str(ema_ncloud)+"\n"
    else:
        msg+="No data received from ema_storing_data table yet"
    print(msg)  
    slack.post_slack(msg,'dep-stats')

'''
def slack_dep_RDS_stats(dep_num):
    path=dep_num+"/cloud_logs/missing_data/"
    files=s3_functions.get_sorted_files(path,1000)
    print(dep_num)
    dates=[]
    fmts=[]
    for f in files:
        s=f.split('/')[-1].split('.')[0]
        #print(s)
        valid_date_fmt=0
        for fmt in ("%Y-%m-%d","%d-%m-%Y"):
            #print(fmt)
            try:
                d=datetime.datetime.strptime(s,fmt).date()
                dates.append(d)
                valid_date_fmt=1
                fmts.append(fmt)
                break
            except ValueError:
                pass
        if(valid_date_fmt==0):
            raise ValueError('no valid date format found')

    #dates=[datetime.datetime.strptime(f.split('/')[-1].split('.')[0], "%d-%m-%Y").date() for f in files]
    max_idx=np.argmax(dates)
    last_file=path+str(dates[max_idx].strftime(fmts[max_idx]))+'.log'
    #print("last file = " +str(last_file))
    #files=[item.split('/')[-1].split('.')[0] for item in r]
    dep=path.split('/')[0]  
    msg='***************** deployment '+str(dep) +' *****************\n'
    if(len(files)>0):
        #files.sort(key=lambda data:datetime.datetime.strptime(data,"%d-%m-%Y"))
        #last_file=path+last_date+'.log'
        
        lines=s3_functions.read_lines_from_txt_file(last_file)
        #print(lines) 
        if(lines!=-1):
            #find the last occurance of the logs on ema and reward data tables
            last_ema_line_n=-1
            for i,line in enumerate(lines):
                if("ema_storing_data table" in line):
                    last_ema_line_n=i
                    continue
            
            msg+='*table name,last_update_date,#local rows,#cloud rows*\n'    
            n_days=2
            for i in range(n_days):
                last_reward_data=lines[last_ema_line_n-1*(i+1)].replace('\r','').replace("'",'')
                last_ema_line=lines[-1*(i+1)].replace('\r','').replace("'",'')
                msg+='reward_data table, '+last_reward_data+'\n'
                msg+='ema_storing_data table, '+last_ema_line+'\n' 
        
    else:
        msg+='no log files uploaded'
    print(msg)
    slack.post_slack(msg,'dep-stats')
'''

def slack_emotion_counts(dep_num):
    path=dep_num+"/generated_mood_classification/"
    msg='*emotion counts*\n'
    files=s3_functions.get_sorted_files(path,10000)
    if(len(files)>0):
        last_date=''
        dates=[]
        emotions=[]
        for f in files:
            emo,date=f.split('/')[-1].split(' ')
            date=date[:-13]
            dates.append(date)
            emotions.append(emo)
        df=pd.DataFrame()
        df['date']=dates
        df['emo']=emotions  
        df.sort_values(by=['date'])
        counts=df.groupby(['date','emo']).size()
        last_date=max(dates)
        msg+='date='+last_date+'\n'
        emonames=counts[last_date].index
        for e in emonames:
            msg+=e+'-'+str(counts[last_date][e])+'\n'
    else:
        msg+='Cannot find any emotion files'
    print(msg)
    slack.post_slack(msg,'dep-stats')


stat_freq=1*60#1*60*60
#scheduled time in hours in 24hr format
ran=False
schedule_time=14
def RDS_stats(sc):
    global ran
    print("in RDS_stats")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    hr=int(current_time[:2])
    print("current time hr = "+str(hr))
    if((hr==schedule_time or hr==schedule_time+1) and (not ran)):
        #run the payload
        print("running dep stats...")
        monitored_dep_ids,ignored_demonitored_dep_idsp_ids=get_dep_ids()
        for dep_num in monitored_dep_ids:
            try:
                slack_dep_RDS_stats(dep_num)
                slack_emotion_counts(dep_num)
            except Exception as e:
                print(e)
        ran=True
    else:
        ran=False
    sc.enter(stat_freq,1,RDS_stats,(sc,))      

s = sched.scheduler(time.time, time.sleep)
print('starting testing')
s.enter(heart_freq,1,monitor_hb, (s,))
s.enter(newdp_freq,1,detect_new_deps, (s,))
s.enter(stat_freq,1,RDS_stats, (s,))
s.run()

#threading.Thread(target=monitor_hb).start()
#threading.Thread(target=detect_new_deps).start()
#threading.Thread(target=RDS_stats).start()
#now = datetime.datetime.now()
#slack_dep_RDS_stats('8122022')



    
    
    
    
