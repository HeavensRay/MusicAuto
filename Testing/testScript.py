from multiprocessing import Process
import hand

def testProc():   # creates the test multithread
    
    
    testpr=Process(target=hand.handler,args=(hand.qu,))
    testpr.daemon=True
    testpr.start()



    