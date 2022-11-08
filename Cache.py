import CacheSet
import CacheBlock
class Cache:
    # Class attribute
    bigCache = []

    def setWriteType(self, writeType):
        self.writeType = writeType

    def addToBigCache(self, CacheSet):
        self.bigCache.append(CacheSet)

    def getBigCache(self):
        return self.bigCache

