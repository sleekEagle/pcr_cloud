#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 07:46:00 2019

@author: sleek_eagle
"""

import boto3
import set_env
import s3_functions


set_env.read_param()
s3_functions.get_bucket()
s3_functions.get_item_num()


