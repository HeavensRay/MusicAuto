from multiprocessing import Process, Queue 
from multiprocessing import Event

qu=Queue()

def firstLaunch():
    proc.daemon=True
    proc.start()

def handler(queue):
    event=Event()
    from launchVid import run_video_watcher
    while True:
        url=queue.get()
        if queue.empty():
            event.set()
        run_video_watcher(url,event)
        event.clear()
        

def endProc():
    from launchVid import close_window
    qu.close()
    close_window()
    proc.terminate()
    proc.join()

proc=Process(target=handler,args=(qu,))

