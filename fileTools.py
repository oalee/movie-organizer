
import subprocess, os
from pathlib import Path


def du(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')

    
def getMovieList(dirs):
    movies_list = []
    for dir in dirs:
        if Path(dir).is_dir():
            movies_list += [(str(x).split("/")[-1] , str(x) , du(str(x))) for x in Path(dir).iterdir() if x.is_dir() ]
            #Movie  Name , Location and size
    return movies_list
    
def getAllSubdirectories(dirs):
    movies_list = []
    for dir in dirs:
        if Path(dir).is_dir():
            movies_list += [(str(x).split("/")[-1] , str(x) , du(str(x))) for x in Path(dir).iterdir() ]
            #Movie  Name , Location and size
    return movies_list
    
def folderMakes(direcotires):
    
    for movie in getAllSubdirectories(direcotires):
        if ".mkv" in movie[0] or ".mp4" in movie[0] or ".avi" in movie[0]:
            print movie
            movieDir = ' '.join(movie[1].split(".")[:-1])
            os.mkdir(movieDir)
            os.rename(movie[1], movieDir+"/"+movie[0])
            
            
def checkFiles(db):
    for movie in db.getCollection().find():
        if not os.path.exists(movie['path']) :
            print 'no', movie['path']
            db.deletePath(movie['path'])