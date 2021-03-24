from scripts.recover import recover
from sys import byteorder
import parted
import psutil

#ERRORS
#100 - 199: user errors
#200 - 299: not implemented
#300 +    : other catched errors - bugs
"""

def parse_block_group(disk, block_group, START, block_size):
    groupper = group()
    disk.seek(block_group*block_size)

    groupper.superblock = superblock(disk.read(SUPERBLOCKSIZE), block_group)

    if groupper.superblock.valid:
        #Skip due to different block size and superblock size and bootsector size
        disk.read(block_size - SUPERBLOCKSIZE - BOOTSECTORSIZE)

        #group descriptor - get from superblock, 0x8 lower and 0x28 upper bits
        groupper.groupdescriptor = groupdescriptor(disk.read(block_size))

        #inode table - 0x14 deletion time, 0x1a hard links count, 0x0=0x8000 regular file, check for huge_file flag 0x20=0x40000 if yes then cant recover,
        #0x4 Lower + 0x6c upper file / dir size, 0x80 size of inode
        groupper.inodetable = inodetable(disk, groupper.superblock.inodes_per_group - groupper.groupdescriptor.free_inodes_count, groupper.groupdescriptor.inode_table*block_size, START, groupper.superblock.block_size, groupper.superblock.block_group)

        #Now check journal for more information if there are any deleted files
        groupper.journ = journal(block_size, disk, block_group)

    return groupper

def main():
    recover = getDevice()
    recover = getPartition(recover)
    recover['inodes'] = []
    recover['superblocks'] = []

    with open(recover['device'].path, 'rb') as disk:
        START=recover['partition'].geometry.start*recover['device'].sectorSize
        disk.seek(START + BOOTSECTORSIZE)

        chunk = disk.read(SUPERBLOCKSIZE)
        

        for block_group in range(blocks_per_group, total_block_count, blocks_per_group*2):
            recover['inodes'].append(parse_block_group(disk, block_group, START, recover['superblocks'][0].block_size))

        for inode in recover['inodes']:
            for ino in inode:
                print(ino.printInode())

"""

recover()
