import threading
import pdb
import numpy as np
import pandas as pb
import multiprocessing

def worker1():
    
    print ('Worker1')
    return
    
def worker2():
    
    print ('Worker2')
    return

if __name__ == '__main__':
    jobs = []
    

    for i in range(50):
        p1 = multiprocessing.Process(target=worker1)
        p2 = multiprocessing.Process(target=worker2)
        
        p1.start()
        p2.start()

    print("Joined")
    p1.join()
    p2.join()