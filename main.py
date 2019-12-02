import Processor as Processor

#Main program

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
Processor.PAGE_REPLACEMENT_ALGORITHM = 1
Processor.P(2048, 1, 0)
Processor.A(1,1,1)
Processor.debug_status(1)
Processor.P(33, 2, 0)
Processor.debug_status(2)
Processor.A(15,2,0)
Processor.A(16,1,0)
Processor.debug_status(1)
Processor.L(2)
Processor.debug_status(1)
Processor.A(32,1,0)
Processor.debug_status(1)
Processor.P(400, 3, 0)
Processor.debug_status(3)
Processor.F()
Processor.debug_status(1)