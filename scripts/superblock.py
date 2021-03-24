from .constants import SUPERBLOCKMAGICNUMBER, SUPERBLOCKSIZE, errors
from sys import byteorder

#google "ext4 superblock location" and ext4.wiki.kernel.org should give more info
#Maybe make this too multi threaded
#Superblock - veriify if 64 bit is enabled 0xFE - if not then abort, block size 0x18 32bits
def parse_superblock(byte):
    magic_number = int.from_bytes(byte[0x38:0x3A], byteorder=byteorder)
    if not magic_number == SUPERBLOCKMAGICNUMBER:
        errors(3, "Unknown error: magic number not 61267 / 0xEF53")
        
    block_size = (2**10)*(2**int.from_bytes(byte[0x18:0x1c], byteorder=byteorder))

    desc_size = int.from_bytes(byte[0xFE:0xFF], byteorder=byteorder)
    if not desc_size == 64:
        errors(100, "Program error: ext4 filesystem cant be parsed by this program / s_desc_size != 64")

    total_inode = int.from_bytes(byte[0x0:0x3], byteorder=byteorder)
    total_block_count = int.from_bytes(byte[0x4:0x8], byteorder=byteorder)
    free_inode = int.from_bytes(byte[0xC:0xE], byteorder=byteorder)
    blocks_per_group = int.from_bytes(byte[0x20:0x24], byteorder=byteorder)
    clusters_per_group = int.from_bytes(byte[0x24:0x28], byteorder=byteorder)
    inodes_per_group = int.from_bytes(byte[0x28:0x2B], byteorder=byteorder)
    journal_inode = int.from_bytes(byte[0xE0:0xE4], byteorder=byteorder)


    return magic_number, block_size, desc_size, total_inode, free_inode, inodes_per_group, journal_inode, blocks_per_group, total_block_count, clusters_per_group