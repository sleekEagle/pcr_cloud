# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:11:22 2021

@author: Retriever
"""

import dep_data
import file_system_tasks
import time
import logging
import rds
import Log
import threading
from importlib import reload
reload(logging)

table_name='heart_beat'    
col_names='dep_id,ts'

def insert_heart_beat(rds_connection):        
    try:
        dep_id=dep_data.get_dep_id(file_system_tasks.get_project_dir(-3))
        ts=time.time()
        values=str(dep_id)+','+str(int(ts))
        res=rds_connection.insert_row(table_name,col_names,values)   
    except:
        print('exception when inserting heart beat')
        return -1
    return res

            
#frequency to enter heart beat in seconds            
heart_beat_freq=60*30
def manage_heart_beat():
    while(True):
        print('hb')
        logging.basicConfig(level = logging.INFO, 
                            filename =Log.get_log_path(),
                            format = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s')
        try:
            rds_connection=rds.RDS()
            if(isinstance(rds_connection,rds.RDS)):
                res=insert_heart_beat(rds_connection)
                if(res==-1):
                    logging.error("in manage_heart_beat -1 returned from insert_heart_beat()")
                else:
                    logging.info('Heart beat sent')
                    print("Heart beat sent")
        except Exception as e:
            print('Exception in manage_heart_beat() ')
            logging.error("Exception in manage_heart_beat "+str(e))
        time.sleep(heart_beat_freq)
        
threading.Thread(target=manage_heart_beat).start()

    
