# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 11:15:27 2020

@author: sleek_eagle
"""

'''
this code compares the files in local with those in the cloud
then it creates a report on what's in cloud and whats not
'''

import dep_data
import set_env
import s3_upload
import os

#report file 
report_file=set_env.get_project_dir(-3)+'generated_data/report.txt'
#get the current deployment id
set_env.read_param()

local_files=s3_upload.get_local_files()
cloud_files=s3_upload.get_s3_files()

report=[]
for file in local_files:
    splt=file.split('/')[-2:]
    local_file=splt[0]+'/'+splt[1]
    in_cloud=local_file in cloud_files
    report.append(local_file+' - ' + str(in_cloud))

#remove the file
if(os.path.exists(report_file)):
    os.remove(report_file)
#write new data to file     
with open(report_file, 'w') as f:
    for item in report:
        f.write("%s\n" % item)
