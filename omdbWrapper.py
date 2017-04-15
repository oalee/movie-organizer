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
        return 
    else:
        return movie
    
def searchMovie(name, typeSearch):
    url = 'http://www.omdbapi.com/'
    data = {typeSearch : name}
    response = requests.get(url, data)
    res = response.json()
    
    if response.status_code != 200:
        return 
        
    if res['Response'] == 'False':
        return 
        
    return res
    

def checkFiles(db):
    for movie in db.getCollection().find():
        if not os.path.exists(movie['path']) :
            print 'no', movie['path']
            db.deletePath(movie['path'])