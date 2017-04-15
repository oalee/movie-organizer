#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 16:23:25 2017

@author: al
"""

import pymongo

db = None

def getCollection():
    
    global db
    if db != None:
        return db['movies']
        
    client = pymongo.MongoClient()
    db = client['movies_db']
    return db['movies']

def findMoviesById(id):
    collection = getCollection()
    return collection.find( { "imdbID" : id })
    

def movieExist(path):
    collection = getCollection()
    movie = collection.find_one( {"path" : path } )
    if movie == None:
        return False
    return True;
    
def insert(movie):
    getCollection().insert_one(movie)
    
def deleteAll():
    getCollection().remove()
    
def deletePath(path):
    getCollection().remove( {'path' : path} )
    

def printAllMovies():
    for movie in getCollection().find():
        print movie['Title'], movie['Year'], movie['path'], movie['size']

def getDuplicates():
    movies = {}
    for movie in getCollection().find():
        if not movie["imdbID"] in movies:
            movies[movie["imdbID"]] = [ x for x in findMoviesById(movie["imdbID"]) ]
    return {k: v for k,v in movies.iteritems() if len(v) > 1}
    
    