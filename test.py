# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 18:42:25 2021

@author: Meerkat
"""

import logging
from importlib import reload
reload(logging)

def gooo():
    logging.basicConfig(level = logging.ERROR, 
                        filename = "C:/Users/Meerkat/Desktop/Patient-Caregiver-Relationship/Patient-Caregiver-Relationship/cloud_upload/pcr_cloud/my.log",
                        format = '%(asctime)s,%(msecs)d %(levelname)-8s [[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s')
    
    logging.error('And this, too')   
    
gooo()
