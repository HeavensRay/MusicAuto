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
    from launchVid import close_window
    qu.close()
    close_window()
    proc.terminate()
    proc.join()

proc=Process(target=handler,args=(qu,))



