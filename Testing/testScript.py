from multiprocessing import Process
import hand

testpr=Process(target=hand.handler,args=(hand.qu,))

def testProc():   # creates the test multithread
    testpr.daemon=True
    testpr.start()

def endProc():
    from launchVid import close_window
    close_window()
    testpr.terminate()
    testpr.join()
    



    