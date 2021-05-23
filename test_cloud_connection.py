#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 07:46:00 2019

@author: sleek_eagle
"""

import s3_functions
import rds

try:
    rds_connection=rds.RDS() 
    local_connection=rds.Local()
    s3_functions.get_bucket()
    
    if(isinstance(rds_connection,rds.RDS) and isinstance(local_connection,rds.Local)):
        print('connection to databases and s3 success')
    else:
        print('connection to databses and s3 unsuccessfull')
except:
    print('exception when connecting to databases and s3')




