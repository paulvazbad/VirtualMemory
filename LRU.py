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
            print("The page has been used.")
    
    def pop(self):
        return self.list.pop()
    
    def insert(self,process_id,page_id):
        self.list.insert(0,[process_id,page_id])

    def print(self):
      for  ele in self.list:
        print(str(ele[0]) + " " + str(ele[1]))