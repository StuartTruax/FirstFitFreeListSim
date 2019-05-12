
# Memory Allocation using the First Fit Free List method

by Stuart Truax, 2019-5

__Summary__: This is some python code that simulates the behavior of the C library functions `malloc` and `free`. The underlying data structure is a linked list whose records represent blocks of memory with __address__ and __size__ metadata. The linked list structure itself is called the __free list__. The smallest unit of allocatable memory is defined by the __page size__. The behvaior of the respective functions is defined below:

`malloc` - The memory is allocated according to the first fit method. The free list is searched for a block of memory greater than or equal in size to the request. If the block of memory found is larger than the requested size, then the remainder is _split_ off and added to the free list as new record.

`free` - Freeing blocks of memory means updating the record for the freed block and also _merging_ the newly freed blocks with any contiguous blocks that might also be free. This operation is known as __coalescence__ [1]. This means that, again, a search is performed upon every invocation of `free`.


![alt text](sim.png)

### Further Reading:

[1] https://www.memorymanagement.org/mmref/alloc.html

[2] https://en.wikipedia.org/wiki/C_dynamic_memory_allocation


### Required Files and Libraries

`FFLFMemAlloc.py` - Implementation of the free list.

`test_FFLFMemAlloc.py` - `pytest` tests.

`FirstFitFreeListSim.ipynb` - Jupyter notebook with animated simulation of random memory requests.

Python 2.7

`matplotlib`

`numpy`


## Simulation: Memory Allocation under Random Requests

Random amounts of memory will be requested, allocated and possibly freed in the below simulation loop. The animation shows the heap. The allocated memory blocks are black and the free blocks are white.
