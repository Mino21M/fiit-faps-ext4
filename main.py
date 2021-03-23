from multiprocessing import cpu_count
from sys import byteorder
import parted
import psutil
from os import path, remove
from hashlib import md5

BOOTSECTORSIZE = 1024
SUPERBLOCKSIZE = 1024
GROUPDESCSIZE = 64

def errors(val, msg):
    print(msg)
    exit(val)

#google "ext4 superblock location" and ext4.wiki.kernel.org should give more info
#Maybe make this too multi threaded
#Superblock - veriify if 64 bit is enabled 0xFE - if not then abort, block size 0x18 32bits
def parse_superblock(byte):
    magic_number = int.from_bytes(byte[0x38:0x3A], byteorder=byteorder)
    if not magic_number == 0xEF53:
        errors(3, "Unknown error: magic number not 61267 / 0xEF53")
        
    block_size = (2**10)*(2**int.from_bytes(byte[0x18:0x1c], byteorder=byteorder))

    desc_size = int.from_bytes(byte[0xFE:0xFF], byteorder=byteorder)
    if not desc_size == 64:
        errors(100, "Program error: ext4 filesystem cant be parsed by this program / s_desc_size != 64")

    total_inode = int.from_bytes(byte[0x0:0x3], byteorder=byteorder)
    free_inode = int.from_bytes(byte[0xC:0xE], byteorder=byteorder)
    inodes_per_group = int.from_bytes(byte[0x28:0x2B], byteorder=byteorder)


    return magic_number, block_size, desc_size, total_inode, free_inode, inodes_per_group
    ########################
    # POZOR NA 0x150 THE SUPERBLOCK TAM SU ZVYSNE HODNOTY PRE 64bit
    ########################

    #0x04 file size 32bits
    #0x6C file size remaining 32 bits
    #0x14 Deletion time
    #0x1A hard link count
    #0x0 0x8000 - regular file
    #return array of inodes + file names and possible also only deleted files


#group descriptor - get from superblock, 0x8 lower and 0x28 upper bits
def parse_group_descriptor(byte):
    inode_table = int.from_bytes(byte[0x8:0xb] + byte[0x28:0x2b], byteorder=byteorder)
    
    return inode_table

#make this multithreaded with cpu_count()
def undelete_files(inodes, destination):
    pass
    #recover deleted files to directory

def create_image_from(device):
    img = 'backup.img'
    bytes_chunk = 1024
    if path.exists(img):
        remove(img)
    with open(device, 'rb') as dev:
        with open(img, 'wb') as fil:
            buf = dev.read(bytes_chunk)
            while buf:
                fil.write(buf)
                buf = dev.read(bytes_chunk)
    return img

devices = parted.getAllDevices()
for row, dev in enumerate(devices, start=1):
    print("[" + str(row) + "] \t\t" + dev.path)
chosen = input("Choose device or file (Default None) [Number]: ") 

try:
    chosen = int(chosen) - 1
    if chosen < 0 or chosen > len(devices) - 1:
        errors(2, "Invalid number: out of range")
    device = devices[chosen].path
except ValueError:
    if not path.exists(chosen):
        errors(2, "Invalid file: file does not exist")
    device = chosen

recover = {'disk': None, 'partition': None, 'device': None}

recover['device'] = parted.getDevice(device)
recover['disk'] = parted.newDisk(recover['device'])

row = 1
for part in recover['disk'].partitions:
    filesystem = part.fileSystem
    if filesystem and filesystem.type == "ext4":
        #print more information here!!!
        print("[" + str(row) + "] \t\t" + filesystem.type + " partition")
        row += 1
    
chosen = input("Choose partition (Default None) [Number]: ") 
try:
    chosen = int(chosen) - 1
    if chosen < 0 or chosen > len(recover['disk'].partitions) - 1:
        errors(2, "Invalid number: out of range")
    recover['partition'] = recover['disk'].partitions[chosen]
except ValueError:
    errors(2, "Invalid number: not number")

with open(recover['device'].path, 'rb') as disk:
    disk.seek(recover['partition'].geometry.start*recover['device'].sectorSize + BOOTSECTORSIZE)
    ending = recover['partition'].geometry.end*recover['device'].sectorSize

    #Superblock - veriify if 64 bit is enabled 0xFE - if not then abort, block size 0x18 32bits
    magic_number, block_size, desc_size, total_inode, free_inode, inodes_per_group = parse_superblock(disk.read(SUPERBLOCKSIZE))

    #Skip due to different block size and superblock size and bootsector size
    disk.read(block_size-SUPERBLOCKSIZE-BOOTSECTORSIZE)

    #group descriptor - get from superblock, 0x8 lower and 0x28 upper bits
    inode_table = parse_group_descriptor(disk.read(block_size))

    #inode table - 0x14 deletion time, 0x1a hard links count, 0x0=0x8000 regular file, check for huge_file flag 0x20=0x40000 if yes then cant recover,
    #0x4 Lower + 0x6c upper file / dir size, 0x80 size of inode
    

    #print(chunk)