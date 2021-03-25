from .constants import JOURNALMAGICNUMBER
from sys import byteorder

class journal():

    def __init__(self, journal_file, block_size, disk_file):
        self.desc = 0
        self.comm = 0
        self.supr = 0
        self.jcontent = []
        self.block_size = block_size
        self.disk_file = disk_file

        self.get(journal_file)
        self.parse()

    def get(self, journal_file):
        for offset in range(len(journal_file)//self.block_size):
            content = journal_file[offset*self.block_size:(offset + 1)*self.block_size]
            magic_number = int.from_bytes(content[0x00:0x04], byteorder=byteorder)
            if magic_number == JOURNALMAGICNUMBER:
                self.jcontent.append(content)
        
    def parse(self):
        for block in self.jcontent:
            block_type = int.from_bytes(block[0x07:0x08], byteorder=byteorder)
            if block_type == 1:
                print(''.join('\\x{:02x}'.format(letter) for letter in block[0:20]))
                self.desc +=1

                data_block = int.from_bytes(block[0x0b:0xf] + block[0x14:0x18], byteorder=byteorder)
                self.disk_file.seek(data_block*self.block_size)
                content = self.disk_file.read(self.block_size)
                self.descriptor(content)
            elif block_type == 2:
                self.comm +=1
            elif block_type == 4:
                self.supr +=1
                #ee_maxlen = int.from_bytes(block[0x10:0x14], byteorder=byteorder)
                #print(ee_maxlen)

    def print(self):
        print("\t Journal")
        print("\t\t Descriptor records \t\t", self.desc)
        print("\t\t Commit records \t\t", self.comm)
        print("\t\t Superblock records \t\t", self.supr)
            
    def descriptor(self, content):
        print(''.join('\\x{:02x}'.format(letter) for letter in content[0:20]))