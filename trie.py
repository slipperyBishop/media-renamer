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

        for char in key:
            if(char in n.keys):
                n = n.keys[char]
            else:
                n.keys[char] = Node() 
                n = n.keys[char]
        
        n.values.append(actualName)
        n.is_value = True

    def search(self, key): 
        
        n = self.top

        for char in key:
            if(char in n.keys):
                n = n.keys[char]
            else:
                return '' 
        
        if n.is_value:
            return n.values[0]
        else:
            return ""
