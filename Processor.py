import collections
import numpy as np
import math
from LRU import LRU 
from FIFO import FIFO 
from Page import Page 
from Process import Process 

#Global Variables

M = [[-1,-1]]*128
S = [[-1,-1]]*256
lru = LRU()
fifo = FIFO()
global_time = 0
logs = []

#Instances of process
processes = {}
algorithm = [fifo, lru]
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
        for index, memory in enumerate(M):
            if memory == [-1,-1]:
                M[index] = [new_process, page_number]
                new_frame = index
                break
        if page_number not in processes[new_process].table:
            # Create page object
            new_page_obj = Page(page_number, new_frame, 1)
            # Insert into process table
            processes[new_process].insert_page(new_page_obj)
        else:
            #Change S memory
            S[processes[new_process].table[page_number].frame] = [-1, -1]
            #Changes page characteristics in processes
            processes[new_process].table[page_number].frame = new_frame
            processes[new_process].table[page_number].bit_memory = 1
        algorithm[PAGE_REPLACEMENT_ALGORITHM].insert(new_process, page_number)

def swap(process_to_insert_ID, process_to_insert_page_number):
    #gets process to switch with
    process_to_switch_ID, process_to_switch_page_number =  algorithm[PAGE_REPLACEMENT_ALGORITHM].pop()
    S_frame = -1
    #If process needs to switch from S to M
    if process_to_insert_page_number in processes[process_to_insert_ID].table:
        S_frame = processes[process_to_insert_ID].table[process_to_insert_page_number].frame
    #If it is a new page/process
    else:
        S_frame = -1
        for index, memory in enumerate(S):
            if memory == [-1,-1]:
                S_frame = index
                break
        # Create default page object
        new_page_obj = Page(process_to_insert_page_number, -1, -1)
        # Insert into process table
        processes[process_to_insert_ID].insert_page(new_page_obj)
    page_to_S = processes[process_to_switch_ID].table[process_to_switch_page_number]
    ##inserts new/needed process into main memory and algorithm
    processes[process_to_insert_ID].table[process_to_insert_page_number].frame = page_to_S.frame
    processes[process_to_insert_ID].table[process_to_insert_page_number].bit_memory = 1
    algorithm[PAGE_REPLACEMENT_ALGORITHM].insert(process_to_insert_ID, process_to_insert_page_number)
    #updates process table of switched page
    processes[process_to_switch_ID].table[process_to_switch_page_number].frame = S_frame
    processes[process_to_switch_ID].table[process_to_switch_page_number].bit_memory = 0
    #updates S memory
    S[S_frame] = [process_to_switch_ID, page_to_S.ID]
    #updates M memory
    M[processes[process_to_insert_ID].table[process_to_insert_page_number].frame] = [process_to_insert_ID,process_to_insert_page_number]
    print("Página", process_to_insert_page_number, "del proceso", process_to_insert_ID, "swappeada al marco", processes[process_to_insert_ID].table[process_to_insert_page_number].frame, "del área real")
    print("Página", process_to_switch_page_number, "del proceso", process_to_switch_ID, "swappeada al marco", S_frame, "del área de swapping")
    

# Ask for N-bytes in memory
def P(number_of_bytes,process_id,time):
    print("P", number_of_bytes, process_id)
    if(number_of_bytes > 2048):
        raise Exception("Memory requested is too big, limit (2048)")
    number_of_pages  = math.ceil(number_of_bytes/SIZE_OF_PAGE) 
    new_process = Process(process_id,number_of_bytes, time)
    processes[process_id] = new_process
    #Create each page for the process
    for i in range(0,number_of_pages):
        add_page_to_memory(process_id,i)
    #Add process to list of processes
    processes[process_id] = new_process
    print("Asks for memory")

#Gets the real address of a page
def A(virtual_address, process_ID, modify):
    #Validates if virtual address exists
    if (virtual_address > processes[process_ID].size or virtual_address < 0):
        raise Exception("The virual address is not valid.")
    print("A", virtual_address, process_ID, modify)
    #Gets page to execute
    page = processes[process_ID].table[int(virtual_address / SIZE_OF_PAGE)]
    if modify == 1:
        algorithm[PAGE_REPLACEMENT_ALGORITHM].touch(process_ID,page.ID)
        print("Página", int(virtual_address / SIZE_OF_PAGE), "del proceso", process_ID, "modificada.")
    print("Dirección virtual:", virtual_address)
    #If page is already in M it only calculates the real address
    if page.bit_memory:
        print("Dirección real (M):", (page.frame * SIZE_OF_PAGE + virtual_address % SIZE_OF_PAGE))
    #Page is on S, it has to be moved to M by swapping or directly putting it
    else:
        processes[process_ID].page_faults += 1
        print("Memoria en S:", page.frame)
        #Swaps if there are no spaces available in M
        if memory_available(M) == 0:
            swap(process_ID, page.ID)
        # Inserts directly into M
        else:
            add_page_to_memory(process_ID, page.ID)
        print("Dirección real (M):", (processes[process_ID].table[page.ID].frame * SIZE_OF_PAGE + virtual_address % SIZE_OF_PAGE))
    return 0

#Frees all the pages of a process
def L(process_id):
    if not (process_id in processes):
        raise Exception("Process id not found")
    # Iterate in the process.table
    global global_time
    reales_liberados = []
    swapping_liberados = []
    for page in processes[process_id].table.items():
        #Deletes the page
        frame = page[1].frame
        bit_memory = page[1].bit_memory
        if(bit_memory==1):
            #Delete from M
            M[frame] = [-1, -1]
            reales_liberados.append(frame)
        else:
            #Delete from S
            S[frame] = [-1, -1] 
            swapping_liberados.append(frame)
        global_time += 0.1
    if(len(reales_liberados)>0):
        print("Se liberan los marcos de memoria real:", reales_liberados)
    if(len(swapping_liberados)>0):
        print("Se liberan los marcos de swapping", swapping_liberados)
    turnaround = global_time - processes[process_id].timestamp
    #Add to logs the information regarding the process
    log_string = "Process: " + str(process_id) +  "Turnaround: " + str(turnaround) + "Page faults: "+str(processes[process_id].page_faults)
    logs.append(log_string)
    # Delete process from list of processes
    del processes[process_id]

#Returns the number of non-zero elements in memory (# of pages)
def memory_available(memory):
    return sum(-1 in item for item in memory) 

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
    M = [[-1,-1]]*128
    S = [[-1,-1]]*256
    global_time = 0
    logs = []


##Read from file 

def debug_status(process_id):
    print("Memoria M:", memory_available(M))
    print(M)
    print("Memoria S:", memory_available(S))
    print(S)
    
    if process_id in processes:
        print("Process memory of", process_id, ":")
        processes[process_id].print_pages()

