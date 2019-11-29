class FIFO():
    def __init__(self):
        super().__init__()
        self.list = []
    
    def pop(self):
        return self.list.pop(0)
    
    def front(self):
        return self.list.pop(0)

    def insert(self,process_id,page_id):
        self.list.append([process_id,page_id])

    def print(self):
      for  ele in self.list:
        print(str(ele[0]) + " " + str(ele[1]))