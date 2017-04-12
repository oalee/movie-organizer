#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 12:45:23 2017

@author: al
"""
import requests
import json

def findMovieByName(name):
    url = 'http://www.omdbapi.com/'
    data = {"t" : name}
    response = requests.get(url, data)
    print response.json()
    if response.status_code != 200:
        return
        
    if response.json()['Response'] == 'False':
        return
        
    return response.json()
    
