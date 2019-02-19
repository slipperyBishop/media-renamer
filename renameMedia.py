import trie, pickle, os, re, sys, time

movieListName = "movieNames.txt"
movieTrieName = "moviesTrie.pickle"

"""
    
"""
def normalize_movie_name(name):
    
    symbols = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-',
                '=', '+', '[', ']', '{', '}', '\\', '|', ':', ';', '\'', '"', ',', '.',
                '<', '>', '/', '?']
    name = name.lower()
    name2 = ""  
    
    #remove all symbols 
    for char in name:

        if char not in symbols: 
            name2 += char 
        else:    
            name2 += ' ' 

    # replaces multiple contiguous occurences of spaces with one space 
    name2 = re.sub("  +", " ", name2)

    return name2.strip().lower()

def load_dictionary():

    with open(movieTrieName, 'rb') as f:
        return pickle.load(f)

def save_dictionary(moviesTrie):
    
    with open(movieTrieName, 'wb') as f:
        pickle.dump(moviesTrie, f, pickle.HIGHEST_PROTOCOL)


def get_movie_title(name, movieDict):

    bestTitle = ""
    title = search_hash(movieDict, name)

    if title != "" :
        return title

    i = name.find(" ")
    while i != -1:
        
        title = search_hash(movieDict, name[:i])
        
        if title != "":
            bestTitle = title         

        i = name.find(" ", i+1)

    return bestTitle

def get_directory_contents(directory):


    try:
        dirContents = os.listdir(directory) 
    except Exception as e:
        print(e)
        sys.abort()


"""
    checks each file or directory in dirContents for a match
    in the movie names trie

    Returns a list of
"""
def process_directories(directoryPath):

    ### add error checking here
    dirContents = os.listdir(directoryPath)
    moviesDict = load_dictionary()

    numDirs = len(dirContents)
    
    processedMedia = []

    titlesFound = 0
    for name in dirContents:

        response = get_movie_title(normalize_movie_name(name), moviesDict) 

        processedMedia.append([name, response])

    return processedMedia

def search_hash(h, key):
    
    snKey = normalize_movie_name(key).strip()
    if snKey in h:
        return h[snKey]
    
    return ""

def insert_hash(h, key):
   
    snKey = normalize_movie_name(key)
    if snKey not in h:
        h[snKey] = key 
        return True

    return False

def create_movies_dictionary(fileName):
    
    h = {}
    num = 0
    movies = open(fileName)

    for movie in movies:
        if insert_hash(h, movie.strip()):
            num += 1
    
    print("number of movies inserted into dictionary - " + str(num))

    return h

def rename_media(processedMedia, directory):
    
    failed = []

    for i in processedMedia:
        
        newFilePath =  directory + "/" + i[1]
        oldFilePath =  directory + "/" + i[0] 
       
        # if both paths are the same no need to rename anything
        if newFilePath == oldFilePath:
            continue
    
        # make sure the oldPath still exists
        try:
            os.stat(oldFilePath)
        except Exception as exception:
            failed.append([oldFilePath, newFilePath, exception])
            continue 

        appendNumber = 0
        # make sure the file or directory doesn't already exist,
        # otherwise append a number in parenthases and keep incrementing
        # untill the path is unused
        while True or appendNumber == 10:

            try:
                if(appendNumber > 0):
                    os.stat(newFilePath + " ("+str(appendNumber)+")")
                else:
                    os.stat(newFilePath)

            except FileNotFoundError:
                if(appendNumber > 0):
                    newFilePath += " ("+str(appendNumber)+")"
                break
                
            except Exception as e:
                print(e)
                sys.abort()
                
                
            appendNumber += 1

        try:
            os.rename(oldFilePath, newFilePath)
        except Exception as exception:
            failed.append([oldFilePath, newFilePath, exception])

startTime = time.time()

f = open("movieNames.txt")
t = trie.Trie()

for line in f:
    
    l = normalize_movie_name(line)
    t.insert(l, line)


save_dictionary(t)
endTime = time.time()

print("total time taken = " + str(endTime - startTime))

"""

g = load_dictionary()
    
"""

##h = create_movies_dictionary("movieNames.txt")

##save_dictionary(h)

#sys.setrecursionlimit(20000)
#t = update_dictionary()
#t = create_dictionary()
#t = update_dicitonary("movies.txt", t)

#process_directories(dirContents, h)
