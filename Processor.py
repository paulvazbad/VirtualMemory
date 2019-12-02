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
global_time = 0     #in deciseconds for arithmetic purposes
logs = []
debug = False
swaps = 0

#Instances of process
processes = {}
SIZE_OF_PAGE = 16

#Algorithm
algorithm = [fifo, lru]
PAGE_REPLACEMENT_ALGORITHM = 0


# Add the page to memory (swap or insert)
def add_page_to_memory(new_process, page_number):
    global global_time
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
    #adds 1 sec to global time for adding page to M
    global_time += 10

def swap(process_to_insert_ID, process_to_insert_page_number):
    global global_time
    global swaps
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
    #adds 1 sec to global timer because of the extra operation of swapping out "process_to_switch"
    processes[process_to_insert_ID].page_faults += 1
    global_time += 10
    swaps += 1
    
# Ask for N-bytes in memory
def P(number_of_bytes, process_id):
    print("P", number_of_bytes, process_id)
    if(number_of_bytes > 2048):
        print("Proceso excede el limite de tamaño (2048 bytes)")
        print()
    elif(number_of_bytes > (memory_available(M) + memory_available(S))*16):
        print("Memoria insuficiente; puede liberar espacio quitando un proceso.")
        print()
    else:
        #Add process to list of processes
        number_of_pages  = math.ceil(number_of_bytes/SIZE_OF_PAGE) 
        new_process = Process(process_id, number_of_bytes, global_time)
        processes[process_id] = new_process
        #Create each page for the process
        for i in range(0,number_of_pages):
            add_page_to_memory(process_id, i)
        print("Se agregaron", number_of_bytes, "bytes de memoria real al proceso", process_id)
        if debug:
            debug_status()
        else:
            print("Memory of process", process_id, ":")
            processes[process_id].print_pages()
            print()

#Gets the real address of a page
def A(virtual_address, process_ID, modify):
    global global_time
    print("A", virtual_address, process_ID, modify)
    #Validates if process exists
    if(process_ID not in processes):
        print("Proceso no existente")
        print()
    #Validates if virtual address exists
    elif (virtual_address > processes[process_ID].size or virtual_address < 0):
        print("Dirección virtual no válida")
        print()
    else:
        #Gets page to execute
        page = processes[process_ID].table[int(virtual_address / SIZE_OF_PAGE)]
        if modify == 1:
            algorithm[PAGE_REPLACEMENT_ALGORITHM].touch(process_ID,page.ID)
            print("Página", int(virtual_address / SIZE_OF_PAGE), "del proceso", process_ID, "modificada/ejecutada.")
        print("Dirección virtual:", virtual_address)
        #If page is already in M it only calculates the real address
        if page.bit_memory:
            print("Dirección real (M):", (page.frame * SIZE_OF_PAGE + virtual_address % SIZE_OF_PAGE))
            global_time += 1
        #Page is on S, it has to be moved to M by swapping or directly putting it
        else:
            if debug:
                print("Fallo de página", process_ID, page.ID)
            # Inserts page into M
            add_page_to_memory(process_ID, page.ID)
            print("Dirección real (M):", (processes[process_ID].table[page.ID].frame * SIZE_OF_PAGE + virtual_address % SIZE_OF_PAGE))
        if debug:
            debug_status()
        else:
            print()

#Frees all the pages of a process
def L(process_id):
    global global_time
    print("L", process_id)
    if not (process_id in processes):
        print("Proceso no encontrado.")
        print()
    else:
        # Iterate in the process.table
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
            global_time += 1
        algorithm[PAGE_REPLACEMENT_ALGORITHM].delete_process(process_id)
        if(len(reales_liberados)>0):
            print("Se liberan los marcos de memoria real:", reales_liberados)
        if(len(swapping_liberados)>0):
            print("Se liberan los marcos de swapping", swapping_liberados)
        turnaround = (global_time - processes[process_id].timestamp)/10
        #Add to logs the information regarding the process
        log_string = "Proceso: " + str(process_id) +  " Turnaround: " + str(turnaround) + " Fallos de página: "+str(processes[process_id].page_faults)
        logs.append(log_string)
        # Delete process from list of processes
        del processes[process_id]
        if debug:
            debug_status()
        else:
            print()

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
    print("F")
    for process_id in list(processes):
        L(processes[process_id].id)
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
    print("Programa reinicializado")
    if debug:
        debug_status()
    else:
        print()

## Comentario
def C(comment):
    print(comment)

## Read from file 

## Debug display
def debug_status():
    print("Memoria M:", memory_available(M))
    print(M)
    print("Memoria S:", memory_available(S))
    print(S)
    
    for process in processes:
        print("Memory of process", process.id, ":")
        processes[process].print_pages()
