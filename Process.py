"""
Clase que simula un proceso.
Atributos:
- id: identificador único de proceso
- table: diccionario de páginas 
- size: tamaño del proceso en bytes
- timestamp: tiempo en el que se creó el proceso
"""

class Process():
    def __init__(self,id,size, time):
        super().__init__()
        self.id = id
        self.size = size        #in bytes
        self.timestamp = time
        self.table = {}         #stores pages
        self.page_faults = 0
    
    def insert_page(self,page):
        if(self.table.get(page.ID, None) == None):
            self.table[page.ID] = page
        else:
            print("ERROR: Page already defined")
        
    def delete_page(self,page):
        del self.table[page.ID] 

    def update_page(self,page_id,frame,bit_memory):
        self.table[page_id].update_page(frame, bit_memory)


    def print_pages(self):
        print("page_id" +" | "+"Frame"+" | "+"Bit")
        for page in self.table.items():
            print("   ", page[1].ID, " | ", page[1].frame, " | ", page[1].bit_memory)
        
    
