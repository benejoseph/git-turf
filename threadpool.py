#!/usr/bin/python
from threading import Thread
from multiprocessing import Pool
from Queue import Queue
import time

class ThreadPool(Thread):
    def __init__(self,workerfunc,numthreads):
        Thread.__init__(self)
        self.running = True
        self.workerfunc = workerfunc
        self.queue = Queue(numthreads*10)
        self.pool = Pool(numthreads)
        
    def run(self):
        while (self.running == True):
            data = self.queue.get(True) #blocks

            if data is not None:
                self.pool.map_async(self.workerfunc,[data])
                

    def stop(self):
        self.running = False
        self.queue.put(None)
        self.join()

    def put(self,data):
        self.queue.put(data)
        

def testworker(data):
    time.sleep(3)
    print data

if __name__ == '__main__':
    #do a test
    t = ThreadPool(testworker,2)

    t.start()
    names = ["foo","bar","ice cream"]

    for name in names:
        print ("putting %s" % name)
        t.put(name)
        
    time.sleep(10)

    t.stop()
