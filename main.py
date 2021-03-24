from scripts.inodes import parse_group_descriptor, parse_inode_table
from scripts.journal import parse_journal_superblock
from scripts.device import getDevice, getPartition
from scripts.superblock import parse_superblock
from scripts.constants import SUPERBLOCKSIZE, BOOTSECTORSIZE
from sys import byteorder
import parted
import psutil


def parse_block_group(disk, block_group, START, block_size):
    disk.seek(block_group*block_size)

    magic_number, block_size, desc_size, total_inode, free_inode, inodes_per_group, journal_inode, blocks_per_group, total_block_count, clusters_per_group = parse_superblock(disk.read(SUPERBLOCKSIZE))

    #for block_group in range((recover['partition'].getLength()*recover['device'].sectorSize)//):
    #Skip due to different block size and superblock size and bootsector size
    disk.read(block_size - SUPERBLOCKSIZE - BOOTSECTORSIZE)

    #group descriptor - get from superblock, 0x8 lower and 0x28 upper bits
    inode_table, free_inodes_count = parse_group_descriptor(disk.read(block_size))

    #inode table - 0x14 deletion time, 0x1a hard links count, 0x0=0x8000 regular file, check for huge_file flag 0x20=0x40000 if yes then cant recover,
    #0x4 Lower + 0x6c upper file / dir size, 0x80 size of inode
    inodes = parse_inode_table(disk, inodes_per_group - free_inodes_count, inode_table*block_size, START, block_size, block_group)

    #Now check journal for more information if there are any deleted files
    parse_journal_superblock(block_size, disk, block_group)

    return inodes

def main():
    recover = getDevice()
    recover = getPartition(recover)
    inodes = []

    with open(recover['device'].path, 'rb') as disk:
        START=recover['partition'].geometry.start*recover['device'].sectorSize
        disk.seek(START + BOOTSECTORSIZE)

        magic_number, block_size, desc_size, total_inode, free_inode, inodes_per_group, journal_inode, blocks_per_group, total_block_count, clusters_per_group = parse_superblock(disk.read(SUPERBLOCKSIZE))

        inodes.append(parse_block_group(disk, START + BOOTSECTORSIZE, START, 1))
        for block_group in range(blocks_per_group, total_block_count, blocks_per_group*2):
            inodes.append(parse_block_group(disk, block_group, START, block_size))

        for inode in inodes:
            for ino in inode:
                print(ino.printInode())

main()