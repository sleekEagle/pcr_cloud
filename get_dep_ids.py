# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:17:34 2020

@author: M2FED_LAPTOP
"""
import s3_functions
import set_env

ids=s3_functions.get_depids()    
set_env.set_var('dep_ids',ids)
print(set_env.get_env('dep_ids'))