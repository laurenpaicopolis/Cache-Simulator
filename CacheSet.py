import Cache
import CacheBlock
class CacheSet:

    def __init__(self, num):
        self.num = num
        self.blocksInSet = []
        self.tags = []

    def getNum(self):
        return self.num

    def addBlockToCacheSet(self, cacheBlock):
        self.blocksInSet.append(cacheBlock)

    def addTagsToQueue(self, tagNum):
        self.tags.append(tagNum)

    def removeTagsFromQueue(self, tagNum):
        self.tags.remove(tagNum)

    def getBlocksInSet(self):
        return self.blocksInSet

    def getTagQueue(self):
        return self.tags

