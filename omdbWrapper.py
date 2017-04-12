#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 12:45:23 2017

@author: al
"""
import requests

def findMovieByName(name):
    movie = searchMovie(name, "t")
    if  movie == None:
        print searchMovie(name, "s")
    
def searchMovie(name, typeSearch):
    
    url = 'http://www.omdbapi.com/'
    data = {typeSearch : name}
    response = requests.get(url, data)
    if response.status_code != 200:
        return
        
    if response.json()['Response'] == 'False':
        return
        
    return response.json()
    
