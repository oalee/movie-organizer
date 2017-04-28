#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 12:45:23 2017

@author: al
"""
import requests

def findMovieByName(name, year):
    movie = searchMovie(name, "t", year)
    if  movie == None:
        print searchMovie(name, "s", year)
        
        return 
    else:
        return movie
    
def searchMovie(name, typeSearch, year):
    url = 'http://www.omdbapi.com/'
    data = {typeSearch : name}
    if year != None:
        data['y'] = year
    response = requests.get(url, data)
    res = response.json()
    
    if response.status_code != 200:
        return 
        
    if res['Response'] == 'False':
        return 
        
    return res
    
