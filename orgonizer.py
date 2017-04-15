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
import fileTools as ft
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
        if j == '[' or j =='(' :
            doReplace = True

        if not doReplace and j not in forbidden_list:
            temp += j

        if j == ']' or j == ')':
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
    parser.add_argument("--dirs", nargs='*', dest="dirs",
                        help="movie folders are in this directories")
    parser.add_argument('--parent',  default=False, action="store_true",
                        help="dirs object are treated as parent folder,\
                        meaning sub directories have actual movie folder in them")
    parser.add_argument('-c', default=False, action="store_true",
                        help="clear database")
    parser.add_argument('-p', default=False, action="store_true",
                        help="print all movies in database")
    parser.add_argument('-m', default=False, action="store_true",
                        help="make folder for raw movie files\
                        only folders are considered as movie file")
    parser.add_argument('--checkfiles', default=False, action="store_true"
                        , dest="checkfiles"
                        , help="recheck database and files (deleted movies)")
    parser.add_argument('-d', default=False, action="store_true",
                        help="check duplicate movies")
    parser.add_argument('--ask', default=False, action="store_true",
                        help="ask every duplicate movie to save which one\
                         . must use -d arg")
    parser.add_argument('--bigest', default=False, action="store_true",
                        help="save the bigest movie in case of duplicates. must use -d arg")
    parser.add_argument('--smallest', default=False, action="store_true",
                        help="save the smallest movie in case of duplicates. must use -d arg")
    
    parser.add_argument('--name', default=False, action="store_true",
                        help="corrects the name of folder to actual title")
    
        
    
    return parser.parse_args(sys.argv[1:])



def findMovies(directories):
    
    for movie in ft.getMovieList(directories):
        if db.movieExist(movie[1]) :
            continue
        omovie = omdb.findMovieByName(currectName(movie[0]))
        if omovie == None:
            print 'Err, Didnt find' , movie[1], "," ,currectName(movie[0])
        else :
            omovie['path'] = movie[1]
            omovie['size'] = movie[2]
            db.insert(omovie)
            



pars = init_parser()

dirs = pars.dirs


if pars.c:
    db.deleteAll()
    exit()

if pars.parent:
    newDir = []
    for dir in dirs:
        newDir += [x for x in Path(dir).iterdir()]
    dirs = newDir
    print dirs

if len(dirs) < 1 :
    print 'atleast 1 directory must be selected';
    exit()

if pars.m:
    ft.folderMakes(dirs)
if pars.checkfiles:
    ft.checkFiles(db)
 
findMovies(dirs)
if pars.p:
    db.printAllMovies()

if pars.d:
    for item, o in db.getDuplicates().iteritems():
        for j in o:
            print j['path'], j['size']/(1024*1024*1024.0) , "GB"

if pars.name:
    ft.renameMovieName(db)            
   