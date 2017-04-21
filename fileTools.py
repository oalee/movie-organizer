
import subprocess, os
from pathlib import Path
from shutil import rmtree, move

def du(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')
    
    
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

    
def getMovieList(dirs):
    movies_list = []
    for dir in dirs:
        if Path(dir).is_dir():
            movies_list += [(str(x).split("/")[-1] , str(x) , get_size(str(x) )) for x in Path(dir).iterdir() if x.is_dir() ]
            #Movie  Name , Location and size
    return movies_list
    
def getAllSubdirectories(dirs):
    movies_list = []
    for dir in dirs:
        if Path(dir).is_dir():
            movies_list += [(str(x).split("/")[-1] , str(x) , get_size(str(x))) for x in Path(dir).iterdir() ]
            #Movie  Name , Location and size
    return movies_list
    
def folderMakes(direcotires):
    
    for movie in getAllSubdirectories(direcotires):
        if ".mkv" in movie[0] or ".mp4" in movie[0] or ".avi" in movie[0] or ".rar" in movie[0]:
            print 'making folder for', movie
            movieDir = ' '.join(movie[1].split(".")[:-1])
            os.mkdir(movieDir)
            os.rename(movie[1], movieDir+"/"+movie[0])
            
def renameMovieName( db):
    for item in db.getCollection().find():
        folderName = item['path'].split('/')[-1]
        title = item['Title'].replace("/"," ")
        if folderName != title :
            newPath = '/'.join(item['path'].split('/')[:-1]) +"/" +title
            print 'rename' , item['path'], newPath
            if Path(newPath).exists():
                print "Err, items new path already exists, remove duplicates first"
                continue
            os.rename(item['path'], newPath)
            db.updatePath(item, newPath)

            
def checkFiles(db):
    for movie in db.getCollection().find():
        if not os.path.exists(movie['path']) :
            print 'no', movie['path']
            db.deletePath(movie['path'])
            
def keepBiggest(movies, db):
    sortedMovies = sortMoviesBySize(movies)
    deleteMovies(sortedMovies[1:], db)
    
def keepSmallest(movies, db):
    sortedMovies = sortMoviesBySize(movies)
    deleteMovies(sortedMovies[:-1], db)
    
def keepAndAsk(movies, db):
    sortedMovies = sortMoviesBySize(movies)
    print 'Movie Duplicate', movies[0]['Title']
    for movie in sortedMovies:
        print  sortedMovies.index(movie), movie['path'], movie['size']
    while 1:
        index = input("Enter an index ")
        if index < 0 or index >= len(sortedMovies):
            print 'invalid index'
            continue
        sortedMovies.remove(sortedMovies[index])
        deleteMovies(movies, db)
        break
    
def sortMoviesBySize(movies):
    return sorted(movies, key=getMovieKey, reverse=True)

def getMovieKey(movie):
    return movie['size']
            
def deleteMovies(movies, db):
    for movie in movies:
        print 'deleting', movie['path']
        rmtree(movie['path'])
        db.deletePath(movie["path"])