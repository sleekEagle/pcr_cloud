# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from getmac import get_mac_address
from requests import get

def get_mac():
    wls_mac = get_mac_address(interface="wls2")
    return wls_mac

def get_ip():
    ip = get('https://api.ipify.org').text
    return ip

