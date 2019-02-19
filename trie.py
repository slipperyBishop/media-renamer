from enum import Enum
class SearchResult(Enum):
    
    NO_MATCH = 0
    PARTIAL_MATCH = 1
    FULL_MATCH = 2 

class Node:
    
    def __init__(self):
        
        self.is_value = False
        self.keys = {} 
        self.values = []


class Trie:
    
    def __init__(self):
        
        self.top = Node() 
        self.size = 0;

    def insert(self, key, actualName):
        
        n = self.top
        key = key.split(" ")
        isNewValue = False 

        for word in key:
            if(word in n.keys):
                n = n.keys[word]
            else:
                n.keys[word] = Node() 
                n = n.keys[word]
        
        n.values.append(actualName)
        n.is_value = True

    
    def search(self, key): 

        if(key == ""):
            return (SearchResult.NO_MATCH, '') 
        
        n = self.top

        key = key.split(" ")
        partialKey = ""

        for word in key:

            if(word in n.keys):
                partialKey += word + " "
                n = n.keys[word]
            else:
                break

        if partialKey == "":
            return (SearchResult.NO_MATCH, '') 

        partialKey = partialKey.strip()
        
        if n.is_value:
            return (SearchResult.FULL_MATCH, n.values[0])
        else:
            return (SearchResult.PARTIAL_MATCH, partialKey)  
