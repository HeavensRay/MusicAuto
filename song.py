import json
import const


SONG_LIST="songList.txt"

class Song:
    def __init__(self,name,author,url,desc):
        self.name=name
        self.author=author
        self.url=url
        self.desc=desc
        songMake ={
        "name":str(self.name),
        "author":str(self.author),
        "url":str(self.url),
        "desc":str(self.desc)
        }
        
        try:
            song_json = json.dumps(songMake ,indent=4)
            with open(f'{const.MASTER}{self.name}.json', 'x') as file:  # a for appending creates new if it doesnt exist
                file.write(song_json)
        
        except FileExistsError:
            print(f"Song '{self.name}' already exists.")
        else:
            with open(f'{const.MASTER}songList.txt','a') as file:
                file.write(f"{self.name}:")

def editSong(songName,mode,extra):  #edits description or url etc
    print("Editing song")
    data=openSong(songName)

    # Specify the field key to update
    data[mode]=extra
    
    # Convert the modified data back to JSON
    modified_json = json.dumps(data)   

    with open(f"{const.MASTER}{songName}.json", "w") as file:
        file.write(modified_json)
    
    print("Song edited successfully")
def SearchSong(songName):   
    from pathlib import Path
     
    filePath=Path(const.MASTER) / f"{songName}.json"
    if not filePath.exists():
        raise FileNotFoundError

       

def openSong(songName):
    with open(f"{const.MASTER}{songName}.json", 'r') as file:
        data = json.load(file)
        return data

