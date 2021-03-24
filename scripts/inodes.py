from .constants import INODEPOINTER, DEFINODESIZE
from sys import byteorder

class inode():
    def __init__(self, chunk, disk, block_size, i):
        self.chunk = chunk
        self.disk = disk
        self.block_size = block_size
        self.i = i
        
        self.parseInode(self.chunk, self.disk, self.block_size, self.i)

    def parseInode(self, chunk, disk, block_size, i):
        self.mode = int.from_bytes(chunk[0x0:0x2], byteorder=byteorder)
        self.size = int.from_bytes(chunk[0x4:0x8] + chunk[0x80:0x82], byteorder=byteorder)
        self.hard_links = int.from_bytes(chunk[0x1A:0x1B], byteorder=byteorder)
        self.deleted_time = int.from_bytes(chunk[0x14:0x18], byteorder=byteorder)
        self.block_count = int.from_bytes(chunk[0x1c:0x20] + chunk[0x98:0x9c], byteorder=byteorder)
        self.block_addressing = chunk[0x28:0x64]

        self.blocks = parse_inode_type(15, self.chunk, INODEPOINTER, block_size, disk, 0)

    def printInode(self):
        print("inode \t\t\t\t", self.i + 1)
        print("\t mode \t\t\t\t", self.mode)
        print("\t hard links \t\t\t", self.hard_links)
        print("\t size \t\t\t\t", self.size)
        print("\t deleted time \t\t\t", self.deleted_time)
        print("\t block count \t\t\t", self.block_count)


    def parseBlocks(self):
        data_from = b""
        old_position = self.disk.tell()

        for group in self.blocks:
            for block in group:
                self.disk.seek(block*self.block_size)
                data_from += self.disk.read(self.block_size)

        self.disk.seek(old_position)
        return data_from


#group descriptor - get from superblock, 0x8 lower and 0x28 upper bits
def parse_group_descriptor(byte):
    inode_table = int.from_bytes(byte[0x8:0xb] + byte[0x28:0x2b], byteorder=byteorder)
    free_inodes_count = int.from_bytes(byte[0xE:0x10] + byte[0x2E:0x30], byteorder=byteorder)

    return inode_table, free_inodes_count

def parse_extent(byte, block):
    #ee_block = int.from_bytes(byte[0:4], byteorder=byteorder)
    ee_len = int.from_bytes(byte[4:6], byteorder=byteorder)
    ee_pos = int.from_bytes(byte[8:12] + byte[6:8], byteorder=byteorder)
    
    return [*range(ee_pos, ee_pos+ee_len)]

def parse_extent_idx(byte, block):
    ei_block = int.from_bytes(byte[0:4], byteorder=byteorder)
    ei_leaf = int.from_bytes(byte[4:0xa], byteorder=byteorder)
    return ei_block, ei_leaf

def parse_extent_tree(byte, disk):
    #valid_entries = int.from_bytes(byte[0x2:0x4], byteorder=byteorder)
    entries_following_header = int.from_bytes(byte[0x4:0x6], byteorder=byteorder)
    depth = int.from_bytes(byte[0x6:0x8], byteorder=byteorder)
    blocks = []

    for block in range(entries_following_header):
        position = 12*(block+1)
        if depth == 0:
            blocks.append(parse_extent(byte[position:position+12], block))
        else:
            print(parse_extent_idx(byte[position:position+12], block))

    return blocks

def parse_inode_type(end, byte, length, block_size, disk, depth):
    magic_number = int.from_bytes(byte[0x0:0x2], byteorder=byteorder)

    if magic_number == 0xF30A:
        blocks = parse_extent_tree(byte, disk)
    else:
        blocks = []
        for i in range(end):
            inode_block = int.from_bytes(byte[i*length:(i+1)*length], byteorder=byteorder)
            if inode_block > 0:
                if depth == 0:
                    blocks.append(inode_block)
                else:
                    disk.seek(inode_block*block_size)
                    blocks.append(parse_inode_type(block_size//INODEPOINTER, disk.read(block_size), length, block_size, disk, depth-1))
        #data = parse_blocks(disk, blocks, block_size)
        

    return blocks

def parse_inode_table(disk, occupied, offset, start, block_size, block_group):
    disk.seek(start)
    disk.read(offset)

    inodes = []

    for i in range(occupied + 1):
        byte = disk.read(DEFINODESIZE)
        old_address = disk.tell()
        inodes.append(inode(byte, disk, block_size, i))

        disk.seek(old_address)

    return inodes