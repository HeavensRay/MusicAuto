from multiprocessing import Process, Queue
from song import openSong, editSong
import validators  

qu=Queue()

def firstLaunch():
    proc.daemon=True
    proc.start()
    return proc

def handler(queue):
    while True:
        song=queue.get()
        urlManip(song)

def endProc():
    import time
    print("Quitting ...")
    proc.terminate()
    proc.close()
    time.sleep(2)

proc=Process(target=handler,args=(qu,))

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
        

