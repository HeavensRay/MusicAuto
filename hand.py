from multiprocessing import Process, Queue 

qu=Queue()

def firstLaunch():
    proc.daemon=True
    proc.start()
    return proc

def handler(queue):
    from launchVid import run_video_watcher
    while True:
        url=queue.get()
        run_video_watcher(url)

def endProc():
    print("Quitting ...")
    proc.terminate()
    proc.close()

proc=Process(target=handler,args=(qu,))



