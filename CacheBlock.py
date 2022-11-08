import Cache
import CacheSet
class CacheBlock:
    # Class attribute

    def __init__(self, cacheBlockSize, tag, validFlag, dirtyFlag, address, num):
        self.cacheSlotsInBlock = bytearray(cacheBlockSize)
        self.tag = tag
        self.validFlag = validFlag
        self.dirtyFlag = dirtyFlag
        self.address = address
        self.num = num

    def changeDirtyFlag(self, dirtyFlag):
        self.dirtyFlag = dirtyFlag

    def changeValidFlag(self, validFlag):
        self.validFlag = validFlag

    def getValidFlag(self):
        return self.validFlag

    def getDirtyFlag(self):
        return self.dirtyFlag

    def getCacheSlotsInBlock(self):
        return self.cacheSlotsInBlock

    def getTag(self):
        return self.tag

    def setTag(self, tag):
        self.tag = tag


