from .constants import DEFINODESIZE
from .inode import inode

class inodetable():
    
    def __init__(self, chunk, occupied):
        self.inodes = []
        self.occupied = occupied
        print(occupied)
        self.parse(chunk)

    def parse(self, chunk):
        self.inodes = []

        for ind in range(1, self.occupied):
            self.inodes.append(inode(chunk[ind*DEFINODESIZE:(ind+1)*DEFINODESIZE], ind))

    def print(self):
        print("\t iNode table")
        for ind in self.inodes:
            ind.print()