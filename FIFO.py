class FIFO():
    def __init__(self):
        super().__init__()
        self.list = []
    
    def pop(self):
        process_id, page_id = self.list.pop(0)
        return process_id,page_id
    
    def front(self):
        process_id, page_id = self.list.pop(0)
        return process_id,page_id

    def insert(self,process_id,page_id):
        self.list.append([process_id,page_id])

    def print(self):
      for  ele in self.list:
        print(str(ele[0]) + " " + str(ele[1]))