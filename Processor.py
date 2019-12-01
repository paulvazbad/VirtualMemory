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
logs = []
debug = False

#Instances of process
processes = {}
algorithm = [lru, fifo]
SIZE_OF_PAGE = 16
PAGE_REPLACEMENT_ALGORITHM = 0


# Add the page to memory (swap or insert)
def add_page_to_memory(new_process, page_number):
    # Check available frames
    if memory_available(M) <= 0:
        # Swap
        swap(new_process, page_number)
    else:
        # Insert
        new_frame = -1
        for memory in M:
            if memory == 0:
                memory = [new_process, page_number]
                new_frame = memory.index
                break
        # Create page object
        new_page = Page(page_number, new_frame, 1)
        # Insert into process tabe
        processes[new_process].insert_page(new_page)
        algorithm[PAGE_REPLACEMENT_ALGORITHM].insert(new_process, page_number)

def swap(process_to_insert_ID, process_to_insert_page_number):
    process_to_switch_ID, process_to_switch_page_number =  algorithm[PAGE_REPLACEMENT_ALGORITHM].pop()
    #inserts process into main memory
    algorithm[PAGE_REPLACEMENT_ALGORITHM].insert(process_to_insert_ID, process_to_insert_page_number)
    #updates process table of inserted page
    processes[process_to_insert_ID].table[process_to_insert_page_number].bit_memory = 1
    S_frame = processes[process_to_insert_ID].table[process_to_insert_page_number].frame
    processes[process_to_insert_ID].table[process_to_insert_page_number].frame = processes[process_to_switch_ID].table[process_to_switch_page_number].frame
    #updates process table of switched page
    processes[process_to_switch_ID].table[process_to_switch_page_number].frame = S_frame
    processes[process_to_switch_ID].table[process_to_switch_page_number].bit_memory = 0

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

def A(virtual_address, process_ID, modify):
    #Validates if virtual address exists
    if (virtual_address > processes[process_ID].size or virtual_address < 0):
        raise Exception("The virual address is not valid.")

    print("A", virtual_address, process_ID, modify)
    #Gets page to modify
    page = processes[process_ID].table[virtual_address % SIZE_OF_PAGE]

    if page.bit_memory:
        return page.frame + virtual_address % SIZE_OF_PAGE
    else:
        processes[process_ID].page_faults += 1
        print("Memoria en S:", page.frame)
        #Swaps if there are no spaces available in M
        if memory_available(M) == 0:
            swap(process_ID, page)
        # Inserts into M
        else:
            new_frame = -1
            for memory in M:
                if memory == 0:
                    memory = [process_ID, page.ID]
                    new_frame = memory.index
                    break
            #Changes page characteristics in processes
            processes[process_ID].tabe[page.ID].frame = new_frame
            processes[process_ID].tabe[page.ID].bit_memory = 1
            algorithm[PAGE_REPLACEMENT_ALGORITHM].insert(process_ID, page.ID)

        print("Memoria actual en M:", (processes[process_ID].table[page.ID].frame + virtual_address % SIZE_OF_PAGE))
    return 0

#Frees all the pages of a process
def L(process_id):
    # Iterate in the process.table
    process = processes[process_id]
    if (process == None):
        raise Exception("Process id not found")
    reales_liberados = []
    swapping_liberados = []
    for page in process:
        #Deletes the page
        frame = page.frame
        bit_memory = page.bit_memory
        if(bit_memory==1):
            #Delete from M
            M[frame] = 0
            reales_liberados.append(frame)
        else:
            #Delete from S
            S[frame] = 0 
            swapping_liberados.append(frame)
        global_time += 0.1
    if(len(reales_liberados)>0):
        print("Se liberan los marcos de memoria real:", reales_liberados)
    if(len(swapping_liberados)>0):
        print("Se liberan los marcos de swapping", swapping_liberados)
    
    turnaround = global_time - process.timestamp
    #Add to logs the information regarding the process
    log_string = "Process: " + str(process_id) +  "Turnaround: " + str(turnaround) + "Page faults: "+str(process.page_faults)
    logs.append(log_string)
    # Delete process from list of processes
    del processes[process_id]

#Returns the number of non-zero elements in memory (# of pages)
def memory_available(memory):
    return len(memory) - np.count_nonzero(memory)

#Prints OUTPUT and resets everything
def F():
    global logs
    global M
    global S
    global lru
    global fifo
    global global_time
    global logs
    global processes
    global  SIZE_OF_PAGE
    #Instances of process
    processes = {}
    SIZE_OF_PAGE = 16
    for log in logs:
        print(log)

    #resets everything
    M = np.zeros(128)
    S = np.zeros(256)
    lru = LRU()
    fifo = FIFO()
    global_time = 0
    logs = []


##Read from file 

def debug_status(process_id):
    print("Memoria M:", memory_available(M))
    print("Memoria S:", memory_available(S))
    
    if memory_available(processes) > 0:
        print("Process memory:")
        for page in processes[process_id].table:
            if page:
                print (page.ID, page.frame, page.bit_memory)

