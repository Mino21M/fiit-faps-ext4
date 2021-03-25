from scripts.inodetable import inodetable
from scripts.journal import journal
from scripts.superblock import superblock
from scripts.groupdescriptor import groupdescriptor
from scripts.constants import SUPERBLOCKSIZE

class group():

    def __init__(self, group_number, disk_file, padding, recovery_folder, partition_offset):
        self.disk_file = disk_file
        self.disk_file.seek(padding + partition_offset)
        self.superblock = superblock(self.disk_file.read(SUPERBLOCKSIZE), group_number)

        if self.superblock.valid:
            self.disk_file.seek(self.superblock.block_size + partition_offset)
            self.groupdescriptor = groupdescriptor(self.disk_file.read(self.superblock.block_size))

            self.disk_file.seek(self.superblock.block_size * self.groupdescriptor.inode_table + partition_offset)
            self.inodetable = inodetable(self.disk_file.read(self.superblock.block_size), self.superblock.inodes_per_group, self.superblock.inode_size, group_number)
            
            journal_inode = self.inodetable.inodes[self.superblock.journal_inode - 1]
            journal_file = journal_inode.getData(self.disk_file, self.superblock.block_size)
            self.journal = journal(journal_file,  self.superblock.block_size, disk_file, self.superblock.inode_size, recovery_folder)

    def print(self, verbosity):
        text = self.superblock.print(verbosity)

        if self.superblock.valid:
            text += self.groupdescriptor.print(verbosity)
            text += self.inodetable.print(verbosity)
            text += self.journal.print(verbosity)

        return text