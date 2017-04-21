#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 16:23:25 2017

@author: al
"""

"""
sample movie in db
{ "_id" : ObjectId("58f9e9fbb6a49a42d4d69271"),
 "Plot" : "Nineteen-year-old Alice returns to the magical world from her childhood adventure, where she reunites with her old friends and learns of her true destiny: to end the Red Queen's reign of terror."
 , "Rated" : "PG",
 "Ratings" : [ { "Source" : "Internet Movie Database",
 "Value" : "6.5/10" }, { "Source" : "Rotten Tomatoes", "Value" : "52%" }, { "Source" : "Metacritic", "Value" : "53/100" } ],
 "DVD" : "01 Jun 2010", 
 "Writer" : "Linda Woolverton (screenplay), Lewis Carroll (books)", 
 "Production" : "Walt Disney Pictures", 
 "Actors" : "Johnny Depp, Mia Wasikowska, Helena Bonham Carter, Anne Hathaway", 
 "Type" : "movie", "imdbVotes" : "321,381", 
 "size" : NumberLong("8531184192"),
 "Website" : "http://disney.go.com/disneypictures/aliceinwonderland/",
 "Poster" : "https://images-na.ssl-images-amazon.com/images/M/MV5BMTMwNjAxMTc0Nl5BMl5BanBnXkFtZTcwODc3ODk5Mg@@._V1_SX300.jpg", 
 "Title" : "Alice in Wonderland",
 "Director" : "Tim Burton",
 "Released" : "05 Mar 2010",
 "Awards" : "Won 2 Oscars. Another 32 wins & 61 nominations.", 
 "Genre" : "Adventure, Family, Fantasy", 
 "imdbRating" : "6.5", "Language" : "English",
 "Country" : "USA", "BoxOffice" : "$319,323,000.00",
 "path" : "/media/al/My Passport/Movies/2010/Alice in Wonderland",
 "Runtime" : "108 min", "imdbID" : "tt1014759",
 "Metascore" : "53", "Response" : "True", "Year" : "2010" }


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
    
def updatePath(item, newPath):
    item["path"] = newPath
    getCollection().find_and_modify( { "_id" : item["_id"] }, item )

def printAllMovies():
    print 'printing movies in db'
    for movie in getCollection().find():
        print movie['Title'], movie['Year'], movie['path'], movie['size']
    print 'end movies'

def getDuplicates():
    movies = {}
    for movie in getCollection().find():
        if not movie["imdbID"] in movies:
            movies[movie["imdbID"]] = [ x for x in findMoviesById(movie["imdbID"]) ]
    return {k: v for k,v in movies.iteritems() if len(v) > 1}
    
def getDirectorsMap(limit):
    movies = {}
    for movie in getCollection().find():
        directors = movie["Director"].split(", ")
        for director in directors:
            if not director in movies:
                movies[director] = [movie]
            else:
                movies[director] += [movie]

    return {k: v for k,v in movies.iteritems() if len(v) >= limit}

    