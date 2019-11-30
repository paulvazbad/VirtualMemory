import numpy as np
from LRU import LRU 
from FIFO import FIFO 
from Page import Page 
from Process import Process 

#Global Variables

M = np.zeros(128)
S = np.zeros(256)
lru = LRU()
fifo = FIFO()

# Ask for N-bytes in memory
def P(bytes,process_id):
    print("Asks for memory")



#Returns the number of non-zero elements in memory (# of pages)
def memory_available(memory):
    return len(memory) - np.count_nonzero(memory)



##Read from file 


print(memory_available(M))
print(memory_available(S))