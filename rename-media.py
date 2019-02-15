#!/bin/python
import trie, pickle, os, re, sys

def split_name(name):
    
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
               'n','o','p','q','r','s','t','u','v','w','x','y','z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    name = name.lower()
    name2 = ""  

    for char in name:

        if((char not in letters) and (char not in numbers)): 
            name2 += ' '
        else:    
            name2 += char


    name2 = re.sub("  +", " ", name2)
    return name2.strip().lower()

def load_trie():

    #taken from python.org article on pickle
    with open('moviesTrie.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        return pickle.load(f)

def save_trie(moviesTrie):
    
    #taken from python.org article on pickle
    with open('moviesTrie.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(moviesTrie, f, pickle.HIGHEST_PROTOCOL)

def create_trie():

    movieTrie = trie.Trie()

    movies = open("movieNames.txt")

    for movie in movies:
        
        movieTrie.insert(split_name(movie), movie.strip())

    return movieTrie

def get_movie_title(name, movieTrie):

    bestTitle = ""
    title = movieTrie.search(name)

    if title != "" :
        return title

    i = name.find(" ")
    while i != -1:
        
        title = movieTrie.search(name[:i])
        
        if title != "":
            bestTitle = title         

        i = name.find(" ", i+1)

    return bestTitle
"""

t = create_trie()
save_trie(t)

"""
directory = sys.argv[1]

moviesTrie = load_trie()
dirContents = os.listdir(directory) 

l = 0 

for name in dirContents:
    l += 1
    print(name)

response = input("\nproceed with overwriting directory and file names? ")

count = 0

if(response == "Y" or response == "y"):
    
    for n in dirContents:
        

        response = get_movie_title(split_name(n), moviesTrie) 
        if response == "":
            count += 1
        print( response + " - " + n)

print(((l - count) / l))
