# imports
from Cache import*

# initialize cache
entireCache = Cache()
from CacheSet import CacheSet
from CacheBlock import CacheBlock

# Global Variables (I know there's a lot)
size = 65536
numberOfSets = 0
memory = bytearray(size)
associativityOfCache = 0
cacheBlockSize = 0
memoryAddressSize = 16
numberOfCacheBlocks = 0
writeBackOrThrough = ""
listOfInformation = []
smallAddressesWrittenTo = []
writeBackInfo = []
cacheEvictInfo = []
writeTime = False

# main: gets user input for cache block (size, associativity, address, write type etc)
def main():

  # global variables
  global memory
  global associativityOfCache
  global entireCache
  global numberOfSets
  global cacheBlockSize
  global memoryAddressSize
  global numberOfCacheBlocks
  global writeBackOrThrough
  global writeTime

  # variables
  userDone = "y"
  i = 0

  # initialize memory
  writeToMemoryOrCache(memory, size, 0, 0)

  # get user input
  sizeOfCache = int(input("Enter the size of the cache in bytes: "))
  cacheBlockSize = int(input("Enter the size of the cache block in bytes: "))
  associativityOfCache = int(input("Enter the associativity of the cache: "))
  writeBackOrThrough = input("Is this a write-back or write-through cache (b/t): ")

  print("\n")
  while writeBackOrThrough != "b" and writeBackOrThrough != "t":
    print("Please enter a valid input below")
    writeBackOrThrough = input("Is this a write or read back cache (b/t): ")


  # calculates number of cache blocks
  numberOfCacheBlocks = sizeOfCache // cacheBlockSize

  # calculates total number of sets
  numberOfSets = numberOfCacheBlocks // associativityOfCache

  # creates sets with cache block byte arrays inside of them
  # adds to entire cache
  while i < numberOfSets:
    cacheSetObj = CacheSet(i)

    # creates number of cache blocks based on associativity of cache
    for j in range(associativityOfCache):
      cacheBlock = CacheBlock(cacheBlockSize, -1, True, False, 0, j)
      cacheSetObj.addBlockToCacheSet(cacheBlock)  # add to set
      cacheSetObj.addTagsToQueue(cacheBlock.tag)  # tag to tag queue
    entireCache.addToBigCache(cacheSetObj)  # add to entire cache
    i += 1

  # gets user selected address
  try:
    while userDone == "y":
      address = int(input("Enter the memory address to use: "))
      while address % 4 != 0:
        address = int(input("Please enter a memory address divisible by 4: "))

      # gets user choice of write type
      readOrWrite = input("Is this a read or a write (r/w)? ")
      while readOrWrite != "r" and readOrWrite != "w":
        print("Please enter a valid input below")
        readOrWrite = input("Is this a read or a write (r/w)? ")
      if readOrWrite == "w":
        writeValue = int(input("Enter the value to write: "))
        writeTime = True
        writeWord(address, writeValue)
      if readOrWrite == "r":
        readWord(address)

      # asks if user would like to put in another address
      userDone = input("Would you like to keep going? (y/n) ")
      while userDone != "y" and userDone != "n":
        userDone = input("Would you like to keep going? (y/n) ")

    print("Cache Simulation Over")

  except:
    print("Invalid input! Please run program again.")

# initializes memory, puts values 0-256 4 bytes away from each other (size of a word)
# this is Jason's code!
def writeToMemoryOrCache(array, sizeTime, startValue, index):
  n = sizeTime // 4

  for i in range(n):
    value = 4 * i + startValue

    b0 = value & 255

    value = value // 256

    b1 = value & 255

    value = value // 256

    b2 = value & 255

    b3 = value // 256

    array[index] = b0

    array[index + 1] = b1

    array[index + 2] = b2

    array[index + 3] = b3

    index = index + 4


# calculateTagBlockIndexandCacheBlock calculates the tag size, offset size,
# and set size of address and returns sizes
def calculateTagBlockIndexandCacheBlock(memoryAddressSize, cacheBlockSize):
  # variables
  global numberOfSets
  found = False
  i = 0

  # calculates offset size by finding what 2^n
  # equals cache block size
  while not found:
    if pow(2, i) == cacheBlockSize:
      found = True
    else:
      i += 1
  offset = i

  # more variables
  t = 0
  found = False

  # calculates set field size by finding what 2^n
  # equals total number of sets
  while not found:
    if pow(2, t) == numberOfSets:
      found = True
    else:
      t += 1
  setField = t

  # calculates tag size
  tagSize = memoryAddressSize - offset - setField

  # returns values
  return offset, setField, tagSize

# findAddressInCacheorMemory: locates memory address either in main memory
# or cache block, completes cache evictions and cache hits/misses
def findAddressInCacheorMemory(address):

  # Global variables (there's a lot!)
  global entireCache
  global memory
  global associativityOfCache
  global cacheBlockSize
  global numberOfCacheBlocks
  global memoryAddressSize
  global numberOfCacheBlocks
  global size
  global listOfInformation
  global writeTime
  global smallAddressesWrittenTo
  global writeBackInfo
  global cacheEvictInfo

  # variables
  setFound = False

  # calculate offset, set, and tag size
  offsetSize, setFieldSize, tagSize = calculateTagBlockIndexandCacheBlock(memoryAddressSize, cacheBlockSize)

  # calculates remaining bits for tag
  remainingBitsForTag = offsetSize + setFieldSize

  # moves over down address
  newAddress = address // pow(2, offsetSize)

  # get set from address
  set = newAddress % pow(2, setFieldSize)

  # get tag
  tag = address // pow(2, remainingBitsForTag )

  # if the address is greater than 0 and less than total size of main memory
  if 0 <= address < size:
    j = 0
    t = 0

    # gets list of sets
    listOfSets = entireCache.getBigCache()

    # finds the corresponding set to memory address
    while j < len(listOfSets) and setFound is False:

      # if set number equals set needed, get corresponding set
      if listOfSets[j].num == set:
        cacheSetSelected = listOfSets[j] # get corresponding set
        setFound = True # set to true b/c found
      j += 1

    # get tag queue from corresponding set
    tagQueue = cacheSetSelected.getTagQueue()

    # variables
    cacheMiss = True
    cacheEvict = True
    memoryAlreadyWrittenTo = False
    found = False

    # look for tag in tag queue, if not there then cache miss
    while t < len(tagQueue):

      # if tag already in queue matches tag, cache hit
      if tagQueue[t] == tag:

        # set both to false due to cache hit
        cacheMiss = False
        cacheEvict = False

        # get cache set list of cache blocks with matching tag
        cacheBlockSelected1 = cacheSetSelected.getBlocksInSet()

        # iterate through set until cache block with matching tag is found
        for item in range(len(cacheBlockSelected1)):

          # if found and has not been found previously, select cache block
          if cacheBlockSelected1[item].tag == tag and found is False:
            cacheBlockSelected = cacheBlockSelected1[item] # get cache block

            # checks to see if the memory has been already been written to with a value < 256
            # will change how value is read from cache block
            for memoryAddress in smallAddressesWrittenTo:
              if memoryAddress == address:
                memoryAlreadyWrittenTo = True

            # calculate location address in cache selected for value
            cacheAddress = address - cacheBlockSelected.address

            # get 64 array of memory from block selected
            cacheBlockArray = cacheBlockSelected.getCacheSlotsInBlock()

            # if the address is bigger than 256 or the value previously written is bigger
            # than 256, calculate original value
            if address > 256 and memoryAlreadyWrittenTo is False:
              remainder = cacheBlockArray[cacheAddress] # get remainder storage in block
              commonFactor = cacheBlockArray[cacheAddress + 1] # get common factor with 256
              partOfAddress = commonFactor * 256 # get largest multiple of 256 < address
              fullValue = partOfAddress + remainder # calculate original value of block

            # the address or value previously written is less than 256
            else:
              fullValue = cacheBlockArray[cacheAddress]

            # append information to list
            listOfInformation.append("address=" + str(address))
            listOfInformation.append("index=" + str(set))
            listOfInformation.append("blockIndex=" + str(cacheBlockSelected.num))
            listOfInformation.append("tag=" + str(tag))

            # just a read from memory
            if not writeTime:
              listOfInformation.append("read hit")
              listOfInformation.append("word=" + str(fullValue))

            # a write from memory
            else:
              listOfInformation.append("write hit")
            listOfInformation.append("(" + str(cacheBlockSelected.address) + " - " +
                                     str(cacheBlockSelected.address + (cacheBlockSize - 1)) + ")")

            # update tag queue
            tagQueue.remove(tag)
            tagQueue.append(tag)

            # reset values
            found = True
      t += 1

    # if the cacheMiss is true
    if cacheMiss is True:

      # get cache block array
      blocksInSet = cacheSetSelected.getBlocksInSet()

      # check if there is an open cache block
      for u in range(associativityOfCache):

        # an open cache block!
        if blocksInSet[u].validFlag is True and cacheEvict is True:
          cacheEvict = False
          cacheBlockSelected = blocksInSet[u] # get open cache block

      # if there is an open cache block, find address in main memory and place it into cache block
      if cacheEvict is False:

        # set new address of cache block
        cacheBlockSelected.address = address
        blockInMainMemory = address // cacheBlockSize # finds 64 byte block in main memory of address
        startingAddressOfBlock = blockInMainMemory * cacheBlockSize # computes start of block in main memory

        # get 64 bit cache block array
        cacheBlockArray = cacheBlockSelected.getCacheSlotsInBlock()
        cacheBlockSelected.setTag(tag) # set tag
        cacheBlockSelected.changeValidFlag(False) # change valid flag

        # checks to see if the memory has been already been written to with a value < 256
        # will change how value is read from cache block
        for memoryAddress in smallAddressesWrittenTo:
          if memoryAddress == address:
            memoryAlreadyWrittenTo = True

        # if the address is bigger than 256 or the value previously written is bigger
        # than 256, calculate original value before written to memory
        if address > 256 and memoryAlreadyWrittenTo is False:
          remainder = memory[address]
          commonFactor = memory[address + 1]
          partOfAddress = commonFactor * 256
          fullValue = partOfAddress + remainder

        # the address or value previously written is less than 256
        else:
          fullValue = memory[address]

        # append information to list
        listOfInformation.append("address=" + str(address))
        listOfInformation.append("index=" + str(set))
        listOfInformation.append("blockIndex=" + str(cacheBlockSelected.num))
        listOfInformation.append("tag=" + str(tag))
        listOfInformation.append("read miss")
        listOfInformation.append("word=" + str(fullValue))
        listOfInformation.append("(" + str(startingAddressOfBlock) +" - " +
                                 str(startingAddressOfBlock + (cacheBlockSize - 1)) +")")

        # copy memory address from memory into cache block
        for i in range(cacheBlockSize):
          cacheBlockArray[i] = memory[startingAddressOfBlock + i]

        # update tag queue
        tagQueue.pop(0)
        tagQueue.append(tag)

      #if a cache evict must happen, no open cache blocks
      elif cacheEvict:

        # removes tag from queue
        tagToEvict = tagQueue[0]
        tagQueue.pop(0)

        # finds cacheBlock to evict based on least recently used tag
        for u in range(associativityOfCache):
          if blocksInSet[u].tag == tagToEvict:
            cacheBlockSelected = blocksInSet[u]

        # if the cache block to be evicted is dirty, write back contents to
        # main memory
        if cacheBlockSelected.dirtyFlag == True:

          # get address from cache block
          addressOfBlock = cacheBlockSelected.address
          blockInMainMemory = addressOfBlock // cacheBlockSize # finds 64 byte block in main memory of address
          startingAddressOfBlock = blockInMainMemory * cacheBlockSize # finds starting address of block in main memory
          cacheBlockArray = cacheBlockSelected.getCacheSlotsInBlock()

          # append info for write back
          writeBackInfo.append("write back (" + str(addressOfBlock) + " - " + str(addressOfBlock + (cacheBlockSize - 1)) + ")")

          # copy cache block array back to memory
          for i in range(cacheBlockSize):
            memory[startingAddressOfBlock + i] = cacheBlockArray[i]

          # set cache block back to not dirty
          cacheBlockSelected.dirtyFlag = False

        # clears cache block array
        cacheBlockSelected.cacheSlotsInBlock = bytearray(cacheBlockSize)

        # set new address for cache block
        cacheBlockSelected.address = address
        blockInMainMemory = address // cacheBlockSize # finds 64 byte block in main memory of address
        startingAddressOfBlock = blockInMainMemory * cacheBlockSize # computes start of block in main memory
        cacheBlockArray = cacheBlockSelected.getCacheSlotsInBlock()
        cacheBlockSelected.setTag(tag) # set new tag

        # checks to see if the memory has been already been written to with a value < 256
        # will change how value is read from cache block
        for memoryAddress in smallAddressesWrittenTo:
          if memoryAddress == address:
            memoryAlreadyWrittenTo = True

        # if the address is bigger than 256 or the value previously written is bigger
        # than 256, calculate original value before written to memory
        if address > 256 and memoryAlreadyWrittenTo is False:
          remainder = memory[address]
          commonFactor = memory[address + 1]
          partOfAddress = commonFactor * 256
          fullValue = partOfAddress + remainder
        else:
          fullValue = memory[address]

        # copies memory address to cache block
        for i in range(cacheBlockSize):
          cacheBlockArray[i] = memory[startingAddressOfBlock + i]

        # add tag to tag queue
        tagQueue.append(tag)

        # append information to list
        listOfInformation.append("address=" + str(address))
        listOfInformation.append("index=" + str(set))
        listOfInformation.append("tag=" + str(tag))

        # just a read from memory
        if not writeTime:
          listOfInformation.append("read miss + replace")
          listOfInformation.append("word=" + str(fullValue))

        # a write from memory
        else:
          listOfInformation.append("write miss + replace")
        listOfInformation.append("(" + str(startingAddressOfBlock) + " - " +
                                 str(startingAddressOfBlock + (cacheBlockSize - 1)) + ")")

    # print information about cache reads/writes
    if writeTime is False:
      print(listOfInformation)
    if cacheEvict:
      cacheEvictInfo.append("evict tag " + str(tagToEvict) + ", in blockIndex " + str(cacheBlockSelected.num))
      if not writeTime:
        print(cacheEvictInfo)
        if len(writeBackInfo) != 0:
          print(writeBackInfo)
        writeBackInfo.clear()
        cacheEvictInfo.clear()
    writeTime = False

    # returns cache block information
    return tagQueue,  cacheBlockSelected, cacheBlockArray

# writeWord: writes word to given address
def writeWord(address, word):

  # global variables
  global writeBackOrThrough
  global listOfInformation
  global smallAddressesWrittenTo
  global writeBackInfo
  global cacheEvictInfo

  # finds cache block in cache memory to use
  tagQueue, cacheBlockSelected, cacheBlockArray = findAddressInCacheorMemory(address)

  # if user selected writeback, change dirty flag and only
  # change address value in cache
  listOfInformation.insert(5,"word=" + str(word))
  print(listOfInformation)

  # print cache information if necessary
  if len(cacheEvictInfo) != 0:
    print(cacheEvictInfo)
  if len(writeBackInfo) != 0:
    print(writeBackInfo)
  print(tagQueue)

  # If user selected write back, write only to cache
  if writeBackOrThrough == "b":

    # change cache block to dirty
    cacheBlockSelected.changeDirtyFlag(True)

    # calculate location address in cache selected for value
    cacheAddress = address - cacheBlockSelected.address

    # write word to cache block depending on size
    if word > 256:

      # calculate what to write
      secondByte = word // 256
      multipleOf256 = secondByte * 256
      firstByte = word - multipleOf256

      # write to cache
      cacheBlockArray[cacheAddress] = firstByte
      cacheBlockArray[cacheAddress + 1] = secondByte

    else:
      # write to cache
      cacheBlockArray[cacheAddress] = word

      # add small value written (used for reading from memory purposes)
      smallAddressesWrittenTo.append(address)

  # if user selected write through, change cache and memory at address
  if writeBackOrThrough == "t":

    # calculate location address in cache selected for value
    cacheAddress = address - cacheBlockSelected.address

    # write word to cache block and memory depending on size
    if word > 256:

      # calculate what to write
      secondByte = word // 256
      multipleOf256 = secondByte * 256
      firstByte = word - multipleOf256

      # write to cache
      cacheBlockArray[cacheAddress] = firstByte
      cacheBlockArray[cacheAddress + 1] = secondByte

      # write to memory
      memory[address] = firstByte
      memory[address + 1] = secondByte

    else:
      # write to cache and memory
      cacheBlockArray[cacheAddress] = word
      memory[address] = word

      # add small value written (used for reading from memory purposes)
      smallAddressesWrittenTo.append(address)

  # clear all lists
  listOfInformation.clear()
  writeBackInfo.clear()
  cacheEvictInfo.clear()

# readWord: receives address and reads memory from address
def readWord(address):

  # read/find cache block to use
  tagQueue, cacheBlockSelected, cacheBlockArray = findAddressInCacheorMemory(address)
  print(tagQueue)

  # clear list
  listOfInformation.clear()

main()

