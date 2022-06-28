#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 13:38:42 2021

@author: sleekeagle
"""

import requests
import file_system_tasks

def post_slack(text,channel):
    #get secret url
    param_dict=file_system_tasks.get_parameters('slack_secret.txt')
    x = requests.post(param_dict[channel], json = {'text':text})
    return x


        


