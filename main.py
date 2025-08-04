from song import *
from playList import *
from hand import qu
import validators  
import const
SONG="song"
LIST="list"

def menu(command):
    match(command):
        case -1:
            from hand import endProc
            endProc()
            print("Quitting ...")
            return
        case 0: print_commands()
        case 1: make_song()
        case 2: make_playlist()
        case 3: SongToPlaylist()
        case 4: printSongInfo()
        case 5: songEditing()
        case 6: DeleteFile()
        case 7: printList()
        case 8: printSongInfo(randSong())
        case 9: AutoPlay()
        case 101:Testing()
        case _: print("Invalid command")

def make_song(name=None): #makes song w user
        print("making song ")
        if(name==None): #so we can pass it in create
            name = input(str("give name ")).strip()
            if(name==""):
                print("Song name can't be empty")
                main()
        author = input(str("give auth "))
        url = input(str("url? _ "))
        desc = input(str("description (optional) "))
        Song(name.lower(),author,url,desc)

def make_playlist(name=None): #makes playlist
    if(name==None):
        listName = input("Give playlist name ").lower()
    Playlist(listName)
    

def fileNotExist(songName,mode):
    data=input(f"'{songName}' not found. Would you like to create it? y/n ").lower()
    if(data=="yes" or data=="y"):
        if(mode==SONG):
            make_song(songName)
        elif(mode==LIST):
            make_playlist(songName)
        print(f"{songName} made successfully")
        return songName
    else:
        print(f"The {mode} {songName} doesnt exist still ...")
        print("Returning to the menu")
        main()

def songEditing():
    songName=input("Which song do you wish to edit? ")
    choice=input("what to edit 1-author , 2-url, 3-desc ")
    match(int(choice)):
        case 1: mode="author"
        case 2: mode="url"
        case 3: mode="desc"
        case _:
            print("invalid mode. \n returning to the program ") 
            return    
    edited=input("Add content you're replacing with ")
    try:
        editSong(songName,mode,edited)
    except FileNotFoundError:
        print("Song not found")
        return

def SongToPlaylist():
    # say this is frm user
    #1st see if a song even exists
    print("Adding song to a playlist")
    listName=input("Which list? ")
    try:
        listData=openList(const.PLAY_PATH,listName)
    except FileNotFoundError:
         fileNotExist(listName,LIST)
         return
    songCount =input(f"How many songs do you wish to add to {listName} ")
    for x in range(int(songCount)):
        songName=input("Song for playlist? ")
        try:
            SearchSong(songName)
        except FileNotFoundError:
            fileNotExist(songName,SONG)
        #now find the playlist
        #see if list exists
        
        #now that we have a list let's check for duplicates
        if(checkForDuplicates(songName,listData)):
            return
        addToList(const.PLAY_PATH,songName,listName)
        print(f"{songName} added to {listName} successfully")
         
def print_commands():
    print("0 help" \
    "\n 1 create song" \
    "\n 2 create playlist" \
    "\n 3 add existing song in a playlist" \
    "\n 4 get song  " \
    "\n 5 edit song  " \
    "\n 6 delete  " \
    "\n 7 print a given list " \
    "\n 8 choose a song at random "\
    "\n 9 AutoPlay songs or PlayList")

def printList():
    listName=input("give a playlist name A for songList B for allList ").lower()
    path=const.PLAY_PATH
    try:
        match(str(listName)):
            case "a": 
                listName="songList" 
                path=const.MASTER
            case "b": 
                listName="allLists"
        listData=openList(path,listName)
    except FileNotFoundError:
        print("List doesn't exist")
        return
    else:
        print()
        print(f"Playlist {listName}:")
        if(listData==None):
            print("the list is empty")
            return
        for x in list(listData):
            print(F"{x}: ",end=" ")
        print()

def printSongInfo(songName=None):

    if(songName==None):
        songName=input("Which song do you wish to see? ")
    try:
        songData=openSong(songName)
    except FileNotFoundError:
        print("Song not found")
        return
    print(f"{songData['name']} by {songData['author']} {songData['desc']}")
    run=input("do you wish to run it? y/n ")
    if(run=="y" or run=="yes"):
        urlManip(songName)
        # from launchVid import close_window
        # close_window()
    


def urlManip(songName):
    url=openSong(songName)["url"]
    if(validators.url(url)):
        qu.put(url)
        return
    else:
        ans=input(f"url for {songName} not provided. Would you like to give url y/n ")
        if(ans=="y" or ans=="yes"):
            url=input("Input valid url and try again ")
            editSong(songName,'url',url)
            urlManip(songName)
        else:
            print("Returning...")
            return

def DeleteFile():
    answer=int(input("what would you like to delete? 1, playlist 2 song from playlist "))
    match(answer):
        case 1: delPlaylist()
        case 2: DelSongFromPlaylist()
        case _: print("invalid comand, returning to the menu...")

def DelSongFromPlaylist():
    print("Removing song from playlist")
    list=input("Enter playlist you wish to delete from ").strip()
    song=input("Enter song you choose to delete ").strip()
    
    
    try:
        SearchSong(song)
        data=openList(const.PLAY_PATH,list)
        ans=input(f"Are you sure you wish to remove {song} from {list} y/n? ").lower().strip()
        if not(ans=="y" or ans=="yes"):
            print("Deletion canceled... \n returning to menu")
            main()
            return
        print(f"Deleting file {song} from {list} ... ")
        
        newData=data

        for x in data:
            if x==list or x=='':
                data.remove(x)

        with open(f'{const.PLAY_PATH}{list}.txt', 'w') as file:
            for x in newData:
                file.write(f"{x}:")
    except FileNotFoundError:
        print("Something wasn't found \n returning to menu")
    
def delPlaylist():
    from const import ALL_LISTS
    print("Removing playlist")
    list=input("Enter playlist you wish to delete ").strip()
    
    try:
        listExists(const.PLAY_PATH,list)
        allLists=openList(const.PLAY_PATH,ALL_LISTS)
        ans=input(f"Are you sure you wish to remove playlist {list} y/n? ").lower().strip()
        if not(ans=="y" or ans=="yes"):
            print("Deletion canceled... \n returning to menu")
            main()
            return
        print(f"Deleting {list} ... ")
        from pathlib import Path
     
        listPath=Path(const.PLAY_PATH) / f"{list}.txt"
        newAll=allLists

        for x in allLists:
            if x==list or x=='':
                newAll.remove(x)

        with open(f'{const.PLAY_PATH}{ALL_LISTS}.txt', 'w') as file:
            for x in newAll:
                file.write(f"{x}:")
        listPath.unlink()
        print(f"{list} deleted")
    except FileNotFoundError:
        print("Something wasn't found \n returning to menu")

def randSong(listName=None,path=None):
    print("choosing a song at random")
    if(listName==None):  
        yN=input("From list? y/n  ")
        listName="songList"
        path=const.MASTER
        if(yN=="y" or yN=="yes"):
            listName=input("Give valid list name ")
            path=const.PLAY_PATH
            
    try:
            listData=openList(path,listName)
    except FileNotFoundError:
        print("List doesn't exist")
        return
    import random
    
    chosen= random.randint(0,len(listData)-1)
    print("Random song chosen ")
    return listData[chosen]

def AutoPlay():
    print("🔁 Autoplaying ... ")
    yN=input("From list? y/n ")
    listName="songList"
    path=const.MASTER
    if(yN=="y" or yN=="yes"):
        listName=input("Give valid list name ")
        path=const.PLAY_PATH
        
    try:
        listData=openList(path,listName)
    except FileNotFoundError:
        print("List doesn't exist")
        return
    ans=input("Would you like to randomize it? y/n ")
    if not (ans=="y" or ans=="yes"):
        for x in list(listData):
                urlManip(x)
    
    else:
        import random
        random.shuffle(listData)
        for x in list(listData):
            urlManip(x)
    # from launchVid import close_window
    # close_window()

def Testing():
    from Testing import testScript
    
    from hand import endProc
    # endProc()
    const.PLAY_PATH = ".\\Testing\\"
    const.MASTER=f"{const.PLAY_PATH}Master\\"
    # testScript.testProc()
    print("Launching testing please wait ...")
    
    import time
    time.sleep(5)
    print("Testing begins")
    print("If you wish to quit testing simply exit the program: -1 ")
    main()
    print("Would you like to delete testing mode? y/n ")
    const.PLAY_PATH = ".\\Playlists\\"
    print("Switched out of testing")
    # firstLaunch()

def main():
    command = None
    while(command!=-1):
        try:
            command=int(input("Choose command 0 help -1 quit "))
            menu(command)
        except ValueError:
            print("Command must be a number")
    
if __name__ == "__main__":
    from hand import firstLaunch
    firstLaunch()
    main()