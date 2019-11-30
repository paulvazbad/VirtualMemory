import numpy as np
import math
from LRU import LRU 
from FIFO import FIFO 
from Page import Page 
from Process import Process 

#Global Variables

M = np.zeros(128)
S = np.zeros(256)
lru = LRU()
fifo = FIFO()
global_time = 0
#Instances of process
processes = {}
SIZE_OF_PAGE = 16


# Add the page to memory (swap or insert)
def add_page_to_memory(new_process,page_number):

    # Check frames available
    # Swap or insert
    # Create page object
    frame = 22132321312322312 # Here goes the frame where it is
    new_page = Page(page_number,frame,1)
    # Insert into process tabe
    new_process.insert_page(new_page)



# Ask for N-bytes in memory
def P(number_of_bytes,process_id,time):
    if(number_of_bytes > 2048):
        raise Exception("Memory requested is too big, limit (2048)")
    number_of_pages  = math.ceil(number_of_bytes/SIZE_OF_PAGE) 
    new_process = Process(process_id,number_of_bytes, time)
    #Create each page for the process
    for i in range(0,number_of_pages):
        add_page_to_memory(new_process,i)

    #Add process to list of processes
    processes[process_id] = new_process
    print("Asks for memory")



#Returns the number of non-zero elements in memory (# of pages)
def memory_available(memory):
    return len(memory) - np.count_nonzero(memory)



##Read from file 


print(memory_available(M))
print(memory_available(S))