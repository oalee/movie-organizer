#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 17:54:27 2017

@author: al
"""

import dbWrapper as db
import omdbWrapper as omdb

import argparse
import sys
from fileTools import folderMakes, checkFiles
from pathlib import Path



def currectName(name):
    name = name.lower()
    cn = ""
    qualities = [ "criterion", "director's cut"
    , "blu-ray" , "directors cut" ,"director's cut" , "remastered"
    "bdrip" , "x264" , "hdtv" , "xvid" , "ntsc",
    "720" , "1080" , "brip" , "bluray" , "dvd" ,
    "m-hd", "hd" , "web" , "brrip", 'extended']
    for q in qualities:
        if name.count(q) > 0:
            cn = q
            break
    if len(cn)> 0:
        name = name.split(cn)[0]
    forbidden_list = [ ")" , "(" , "]" , "[", "{" , "}"]
    name = name.replace("." , " ").replace('_' , " ")
    doReplace = False
    temp = ""
    for j in name:
        if j == '[':
            doReplace = True

        if not doReplace and j not in forbidden_list:
            temp += j

        if j == ']':
            doReplace = False
            
        if j == '-':
            if temp[-2] == ' ':
                temp = temp[:-2]

    name = temp.split(" ")
    index = len(name)
    while index > 0:
        index = index - 1
        try:
            year = int(name[index])
            if year > 1900 :
                break
        except:
            pass
    if index > 0 :
        temp = ""
        for k in range(0,index):
            temp += name[k]
            temp += " "
    return temp
    
    
def init_parser():
    parser = argparse.ArgumentParser(description="Remove Duplicate movies where they have same imdb id")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument("--dirs", nargs='+', dest="dirs",
                        help="parent folder where movies are")
    parser.add_argument('-r',  default=False, action="store_true")
    return parser.parse_args(sys.argv[1:])



def findMovies(directories):
    
    for movie in getMovieList(directories):
        if db.movieExist(movie[1]) :
            continue
        omovie = omdb.findMovieByName(currectName(movie[0]))
        if omovie == None:
            print 'Err, Didnt find' , movie[1], "," ,currectName(movie[0])
        else :
            omovie['path'] = movie[1]
            omovie['size'] = movie[2]
            db.insert(omovie)
            
            
def printAllMovies():
    for movie in db.getCollection().find():
        print movie['Title'], movie['Year'], movie['path'], movie['size']



pars = init_parser()

dirs = pars.dirs

if pars.r:
    newDir = []
    for dir in dirs:
        newDir += [x for x in Path(dir).iterdir()]
    dirs = newDir
    print dirs


#db.deleteAll()
    
folderMakes(dirs)
checkFiles(db)
 
findMovies(dirs)
printAllMovies()
   