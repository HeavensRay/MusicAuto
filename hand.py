from multiprocessing import Process, Queue
from song import openSong, editSong
import validators  

qu=Queue()
def first_launch():
    proc=Process(target=handler,args=(qu,))
    proc.daemon=True
    proc.start()



def handler(qu):
    while True:
        song=qu.get()
        urlManip(song)

def urlManip(songName):
    
    url=openSong(songName)["url"]
    if(validators.url(url)):
        from launchVid import run_video_watcher
        run_video_watcher(url)
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