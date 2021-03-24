from .constants import JOURNALMAGICNUMBER
from sys import byteorder

def parse_journal_superblock(block_size, disk, block_group):
    jcontent = []
    with open("recover/b" + str(block_group) + "_i8.bin", "rb") as journal:
        content = journal.read(block_size)
        while content:
            magic_number = int.from_bytes(content[0x00:0x04], byteorder=byteorder)
            if magic_number == JOURNALMAGICNUMBER:
                jcontent.append(content)
            content = journal.read(block_size)
    
    for block in jcontent:
        block_type = int.from_bytes(block[0x07:0x08], byteorder=byteorder)
        if block_type == 1:
            data_block = int.from_bytes(block[0x0b:0xf] + block[0x14:0x18], byteorder=byteorder)
            disk.seek(data_block*block_size)
            
            content = disk.read(block_size)
        elif block_type == 2:
            print("Commit record")
        elif block_type == 4:
            ee_maxlen = int.from_bytes(block[0x10:0x14], byteorder=byteorder)

            print(ee_maxlen)
            