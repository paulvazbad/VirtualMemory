"""
Prioritiza un lista de IDs <Proceso, página> de acuerdo a su algoritmo de manejo de páginas FIFO.
Atributos:
- list: guarda la lista de IDs para manejar
Funcionaes:
- pop: saca el proceso más antiguo para almacenarlo en otra memoria.
- insert: se inserta un nuevo conjunto de ids al final e la lista
- delete_process: se eliminan los conjuntos de IDs de un proceso en específico
- print: imprime la lista de IDs en orden de prioridad
- touch: simula el uso del proceso. En caso de FIFO, la función no afecta en la prioridad.
"""

class FIFO():
    def __init__(self):
        super().__init__()
        self.list = []
    
    def pop(self):
        process_id, page_id = self.list.pop(0)
        return process_id, page_id

    def insert(self,process_id,page_id):
        self.list.append([process_id,page_id])

    def delete_process(self,process_id):
        indexes_to_delete = []
        counter = 0
        for index in range(len(self.list)):
            if self.list[index][0] == process_id:
                indexes_to_delete.append(index - counter)
                counter += 1
        for index in indexes_to_delete:
                self.list.pop(index)

    def print(self):
      for  ele in self.list:
        print(ele[0], ele[1])

    def touch(self,process_id,page_id):
        return 0

# FIFO = FIFO()

# FIFO.insert(3,0)
# FIFO.insert(2,0)
# FIFO.insert(3,1)
# FIFO.insert(2,3)
# FIFO.insert(3,2)
# FIFO.insert(2,2)

# FIFO.print()

# FIFO.delete_process(3)

# FIFO.print()