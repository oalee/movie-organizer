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



def correctName(name):
    name = name.lower()
    while 1:
        cn = ""
        qualities = [ "criterion", "director's cut"
        , "blu-ray" , "directors cut" ,"director's cut" , "remastered"
        "bdrip" , "x264" , "hdtv" , "xvid" , "ntsc",
        "720" , "1080" , "brip" , "bluray" , "dvd" ,
        "m-hd", "hd" , "web" , "brrip", 'extended', 'unrated','final cut',
        "bdrip"]
        for q in qualities:
            if name.count(q) > 0:
                cn = q
                break
        if len(cn)> 0:
            name = name.split(cn)[0]
        else:
            break
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
    parser = argparse.ArgumentParser(description="a movie organizer")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument("--dirs", nargs='*', dest="dirs",
                        help="movies are in this directories")
    parser.add_argument('--parents',nargs='*',
                        help="parent folder where movie dirs are")
    
    parser.add_argument('-c', default=False, action="store_true",
                        help="clear database (for debugging) ")
    parser.add_argument('-p', default=False, action="store_true",
                        help="print all movies in database")
    parser.add_argument('-m', default=False, action="store_true",
                        help="make folders for movies if movie files (i.e, .mp4) is in directory")
    parser.add_argument('--checkfiles', default=False, action="store_true"
                        , dest="checkfiles"
                        , help="recheck database and files (deleted movies)")
    parser.add_argument('-d', default=False, action="store_true",
                        help="check duplicate movies")
    parser.add_argument('--ask', default=False, action="store_true",
                        help="ask every duplicate movie to save which one\
                         . must use -d arg")
    parser.add_argument('--biggest', default=False, action="store_true",
                        help="keeps the biggest movie in case of duplicates. must use -d arg")
    parser.add_argument('--smallest', default=False, action="store_true",
                        help="keeps the smallest movie in case of duplicates. must use -d arg")
    
    parser.add_argument('--name', default=False, action="store_true",
                        help="corrects the name of folder to actual title")
    parser.add_argument('--year', default=False, action="store_true",
                        help="Makes Yearly Folder")
    
    
        
    
    return parser.parse_args(sys.argv[1:])



def findMovies(directories):
    
    for movie in ft.getMovieList(directories):
        if db.movieExist(movie[1]) :
            continue
        name = correctName(movie[0])
        omovie = omdb.findMovieByName(name)
        
        if "and" in name and omovie == None:
                omovie = omdb.findMovieByName(name.replace("and","&"))
        if omovie == None:
            print 'Err, Didnt find' , movie[1], "," ,correctName(movie[0])
            print "Enter Correct Name or press Enter for passing"

        while omovie == None:
            inputs = raw_input()
            if inputs =="":
                print 'skiping...'
                break
            omovie= omdb.findMovieByName(inputs)
            if omovie != None:
                print 'found the movie'
        if omovie != None :
            omovie['path'] = movie[1]
            omovie['size'] = movie[2]
            db.insert(omovie)
            



pars = init_parser()

dirs = pars.dirs
if dirs == None:
    dirs = []


if pars.c:
    db.deleteAll()
    exit()

if pars.parents:
    newDir = []
    for dir in pars.parents:
        newDir += [x for x in Path(dir).iterdir()]
    dirs = newDir + dirs
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
    duplicates = db.getDuplicates()
    if len(duplicates) == 0:
        print 'No Duplicates found'

    else:
        print len(duplicates),'Duplicates found'
    for item, movies in duplicates.iteritems():
#        for j in o:
#            print j['path'], j['size']/(1024*1024*1024.0) , "GB"
#        print 'end dup movie'
        if pars.ask:
            ft.keepAndAsk(movies, db)
        if pars.biggest:
            ft.keepBiggest(movies, db)
        if pars.smallest:
            ft.keepSmallest(movies, db)

if pars.name:
    ft.renameMovieName(db)        

if pars.year:
    ft.makeYearlyFolders(db)    
    
ft.clearEmptyFolders(dirs)
   