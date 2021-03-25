from .constants import SUPERBLOCKMAGICNUMBER, SUPERBLOCKSIZE
from sys import byteorder

class superblock():

    def __init__(self, chunk, block_group):
        self.chunk = chunk
        self.valid = True
        self.block_group = block_group

        self.parse()

    def parse(self):
        self.magic_number = int.from_bytes(self.chunk[0x38:0x3A], byteorder=byteorder)
        if not self.magic_number == SUPERBLOCKMAGICNUMBER:
            self.valid = False
            self.message = "Wrong superblock magic number"
            self.code = 100
            return

        self.desc_size = int.from_bytes(self.chunk[0xFE:0xFF], byteorder=byteorder)
        if not self.desc_size == 64:
            self.message = "Only 64 bit filesystem supported"
            self.code = 200
            self.valid = False
            return
            
        self.block_size = self.blockSize()
        self.total_inode = self.totalInode()
        self.total_block_count = int.from_bytes(self.chunk[0x4:0x8], byteorder=byteorder)
        self.free_inode = int.from_bytes(self.chunk[0xC:0xE], byteorder=byteorder)
        self.blocks_per_group = self.blocksPerGroup()
        self.clusters_per_group = int.from_bytes(self.chunk[0x24:0x28], byteorder=byteorder)
        self.inodes_per_group = int.from_bytes(self.chunk[0x28:0x2B], byteorder=byteorder)
        self.inode_size = int.from_bytes(self.chunk[0x58:0x5a], byteorder=byteorder)
        self.journal_inode = int.from_bytes(self.chunk[0xE0:0xE4], byteorder=byteorder)

    def blocksPerGroup(self):
        return int.from_bytes(self.chunk[0x20:0x24], byteorder=byteorder)

    def blockSize(self):
        return (2**10)*(2**int.from_bytes(self.chunk[0x18:0x1c], byteorder=byteorder))

    def totalInode(self):
        return int.from_bytes(self.chunk[0x0:0x3], byteorder=byteorder)

    def print(self, verbosity):
        text = "Superblock \t\t\t " + str(self.block_group) + " (valid " + str(self.valid) + ")\n"
        if self.valid:
            if verbosity > 0:
                text += "\t magic number \t\t\t " + str(self.magic_number) + "\n"
                text += "\t inode size \t\t\t" + str(self.inode_size) + "\n"
            if verbosity > 1:
                text += "\t desc size \t\t\t" + str(self.desc_size) + "\n"
                text += "\t block size \t\t\t" + str(self.block_size) + "\n"
                text += "\t total inode \t\t\t" + str(self.total_inode) + "\n"
            if verbosity > 2:
                text += "\t total block count \t\t" + str(self.total_block_count) + "\n"
                text += "\t free inode \t\t\t" + str(self.free_inode) + "\n"
                text += "\t blocks per group \t\t" + str(self.blocks_per_group) + "\n"
            if verbosity > 3:
                text += "\t clusters per group \t\t" + str(self.clusters_per_group) + "\n"
                text += "\t inodes per group \t\t" + str(self.inodes_per_group) + "\n"
                text += "\t journal inode \t\t\t" + str(self.journal_inode) + "\n"
        else:
            text += "\t Code \t\t\t\t " + str(self.code) + "\n"
            text += "\t Message \t\t\t " + str(self.message) + "\n"

        return text