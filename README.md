# Cache-Simulator
This project simulates the behavior of a hardware memory cache.

Here's an excerpt from the assignment:

# Data Structures

Here’s how I approached this: by considering the fundamental component of a cache to be a set, consisting
of one or more cache blocks. Each set then has n blocks, where n is the associativity. So, for example, a
two-way associative cache of size 64K with 64-byte blocks will have 1024 blocks and 512 sets.
So, you can model your cache as a group of sets (for example, as an array of sets). You might also choose to
model the cache as a group of cache blocks, with some efficient way to mark set membership for each block.
Each cache block will need a tag and two additional attributes: dirty/clean and valid/invalid (although the
valid/invalid attribute is used only for a write-back cache).
The cache data structure itself can be a global variable.
Use the least-recently-used (LRU) algorithm to control block replacement: if you need to replace one of the
blocks in a set, then pick the block that was least recently used. The key data structure you’ll need in order
to implement LRU is a tag queue. The tag queue can be an array of integers.
Each set will have a tag queue. Initialize the tag queue for each set to invalid values, such as -1.
Here’s an example of how the queue will work. Suppose the queue is currently [4, 8, 12, 16], and that the
most recently accessed tag is in the last position.
 - then after an access having tag=4, the queue will be [8, 12, 16, 4]
 - and then after an access having tag=12, the queue will be [8, 16, 4, 12]
 - and then after an access having tag=4, the queue will be [8, 16, 12, 4]
 - and then after an access having tag=6, the queue will be [16, 12, 4, 6]
 - and then after another access having tag=4, the queue will be [16, 12, 6, 4]

In this way, the least-recently accessed tag is always in the first position.

At a high level, your cache consists of a group of arrays representing the cache blocks. Each of these arrays
will have auxiliary information with it (a tag, the dirty/clean and valid/invalid bits, some way to show which
set this array belongs to). A read from memory thus consists of copying a range of values from your memory
array to one of the arrays representing a cache block. A write to memory consists of copying a value to one
of these arrays. The setting for write-through vs. write-back will determine when and if you also copy data
from one of the cache-block arrays back to your memory array.

# Output

In order to observe the behavior of the simulated cache, print output describing what happens in response
to a read or write. For example, with a 65K memory (16-bit addresses), a 1K cache, 64-byte blocks, and
associativity = 1, then in response to a read from address 56132, your functions should print out a string in
this form:
```
[addr=56132 index=13 tag=54: read miss + replace; word=56132 (56128 - 56191)]
```
If there is a read or write miss with a replacement necessary, then print out which tag, in which block index
was evicted (the block index is the index of a block in its set):
```
[evict tag 4, in blockIndex 0]
```
And after each read or write, print the tag queue for the set that was accessed, in this format:
```
[ 12 20 32 54 ]
```
Check: 56132 = 110110 1101 000100, so the block offset is 000100 = 4; four bits are needed for the index
(1024 / 64 = 16), giving the index 1101; and the tag is 110110 = 54.

So in general, after each read, print information in this format:
```
[addr=17536 index=2 tag=68: read miss + replace; word=17536 (17536 - 17599)]
[evict tag 32, in blockIndex 1]
[write back (8320 - 8383)]
[ 36 44 64 68 ]
```
Print the eviction information only for a read miss + replace, and print the write-back info only for a
write-back cache (and only if the evicted cache block is dirty).
After every write, print information in this format:
```
[addr=8320 index=2 tag=32: write miss + replace; word=7 (8320 - 8383)]
[evict tag 28, in blockIndex 1]
[write back (7296 - 7359)]
[ 16 12 20 32 ]
```
And again, print the eviction information only for a write miss + replace, and print the write-back info only
for a write-back cache (and only if the evicted cache block is dirty).
