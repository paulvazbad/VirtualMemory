## Script to count program lines

file_names = ["FIFO.py", "LRU.py", "main.py", "Page.py", "Process.py", "Processor.py"]

counter = 0
counter_total = 0
for file in file_names:
    f = open(file, "r")
    if f.mode == 'r':
        lines = f.readlines()
        for line in lines:
            command = line.split()
            if command != []:
                counter_total += 1
                if "#" not in command[0]:
                    counter += 1
print("Líneas de código: ", counter)
print("Líneas totales: ", counter_total)