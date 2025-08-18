import const
from pathlib import Path


class Playlist:
    def __init__(self,name):
        self.name=name.strip()
        createTxt(self)
    
def createTxt(self):
    # Create the directory
        try:
            with open(f'{const.PLAY_PATH}{self.name}.txt', 'x') as file: # makes empty file once
                pass 
        except FileExistsError:
            print(f"Playlist {self.name} already exists.")
        else:
            print(f"Playlist {self.name} created successfully")
            with open(f'{const.PLAY_PATH}allLists.txt','a') as file: # saves to allLists 
                file.write(f"{self.name}:")

def addToList(path,songName,listName):
    with open(f'{path}{listName}.txt', 'a') as file:
        file.write(f"{songName}:")
    
def checkForDuplicates(song,listData):
    if(listData==[]):
        return False
    for x in listData:
        if song==x:
            print(f"{x} was already in playlist") 
            return True
    return False

def listExists(path,listName): #returns T/F
    filepath = Path(path) / f"{listName}.txt"   
    if not filepath.exists():
        raise FileNotFoundError
     
def openList(path,listName):  #returns list
     with open(f'{path}{listName}.txt', 'r') as file:
            data=file.read().split(":")
            data = data[:-1]
            return data
