# Prioritiza un lista de IDs <Proceso, página> de acuerdo a su algoritmo de manejo de páginas FIFO.
# Atributos:
# - list: guarda la lista de IDs para manejar
# Funciones:
# - pop: saca el proceso más antiguo para almacenarlo en otra memoria.
# - insert: se inserta un nuevo conjunto de ids al final e la lista
# - delete_process: se eliminan los conjuntos de IDs de un proceso en específico
# - print: imprime la lista de IDs en orden de prioridad
# - touch: simula el uso del proceso. En caso de LRU, la función pone al final los IDs especificados.


class LRU():
    def __init__(self):
        super().__init__()
        self.list = []
    
    def touch(self,process_id,page_id):
        i = 0
        size = len(self.list)
        found = False
        while(not found  and i<size):
            ele = self.list[i]
            found = (ele[0]==process_id and ele[1]==page_id)
            if(not found):
                i = i+1
        if(not found):
            print("Process-Page" + str(process_id) +"-"+str(page_id)+ "not found in LRU")
        else:
            del self.list[i]
            self.insert(process_id,page_id)
    
    def pop(self):
        return self.list.pop()

    def delete_process(self,process_id):
        indexes_to_delete = []
        counter = 0
        for index in range(len(self.list)):
            if self.list[index][0] == process_id:
                indexes_to_delete.append(index - counter)
                counter += 1
        for index in indexes_to_delete:
                self.list.pop(index)
    
    def insert(self,process_id,page_id):
        self.list.insert(0,[process_id,page_id])

    def print(self):
      for  ele in self.list:
        print(str(ele[0]) + " " + str(ele[1]))