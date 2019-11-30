class Page():
    # Bit_memory = 1 page is in M
    # Bit_memory = 0 page is in S
    bit_memory = 0
    frame = 0
    ID = 0

    def __init__(self, ID, frame, bit_memory):
        self.bit_memory = bit_memory
        self.frame = frame
        self.ID = ID

    def update_page(self, frame, bit_memory):
        self.frame = frame
        self.bit_memory = bit_memory
