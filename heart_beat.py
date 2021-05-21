# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:11:22 2021

@author: Retriever
"""

import dep_data
import file_system_tasks
import time

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
    
