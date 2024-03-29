"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Trabajo final SO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Aurora Tijerina Berzosa     A01196690
Paul Vazquez Badillo        A00819877
Miguel Morales de la Vega	A00821541
"""

import Processor as Processor

#Main program
f = open("program_commands.txt", "r")
# PAGE_REPLACEMENT_ALGORITHM 1 for LRU
# PAGE_REPLACEMENT_ALGORITHM 0 for FIFO
Processor.PAGE_REPLACEMENT_ALGORITHM = 1
if f.mode == 'r':
    lines = f.readlines()
    for line in lines:
        command = line.split()
        try:
            if command[0] == "P":
                Processor.P(int(command[1]), int(command[2]))
            elif command[0] == "A":
                Processor.A(int(command[1]), int(command[2]), int(command[3]))
            elif command[0] == "L":
                Processor.L(int(command[1]))
            elif command[0] == "C":
                Processor.C(line)
            elif command[0] == "F":
                Processor.F()
            elif command[0] == "E":
                print("Fin del programa.")
                break
        except:
            print("Comando no válido")
            print()
f.close()
    

#FIFO
# Processor.PAGE_REPLACEMENT_ALGORITHM = 0
# Processor.P(2048, 1, 0)
# Processor.A(1,1,0)
# Processor.debug_status(2)
# Processor.A(33,1,1)
# Processor.P(33, 2, 0)
# Processor.debug_status(2)
# Processor.A(15,2,0)
# Processor.A(16,1,0)
# Processor.debug_status(1)
# Processor.L(2)
# Processor.debug_status(1)
# Processor.A(32,1,0)
# Processor.debug_status(1)
# Processor.F()
# Processor.debug_status(1)

#LRU
# 
# Processor.P(2048, 1)
# Processor.A(1,1,1)
# Processor.P(33, 2)
# Processor.A(15,2,0)
# Processor.A(16,1,0)
# Processor.L(2)
# Processor.A(32,1,0)
# Processor.P(400, 3)
# Processor.F()