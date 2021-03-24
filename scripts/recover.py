from scripts.device import device
from scripts.group import group

class recover():

    def __init__(self):
        self.device = device()
        self.groups = []
        
        if self.device.valid:
            self.parse()
            self.recovery()

        self.print()

    def parse(self):
        for group_number in [0, 32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 4096000]:
            gr = group(group_number, self.device.disk_file, 1024)
            self.groups.append(gr)
            if not gr.superblock.valid:
                break

    def recovery(self):
        first_valid_group = None
        #Find first valid group to start recovery
        for group in self.groups:
            if group.superblock.valid:
                first_valid_group = group
                break
        
        #Find iNodes that are on the same spot in inode table
        for num, inode in enumerate(first_valid_group.inodetable.inodes):
            if inode.deleted_time == 0 and inode.hard_links == 0:
                continue
            for group in self.groups:
                if not group.superblock.valid:
                    continue
                if group.inodetable.inodes[num].ind == inode.ind:
                    print("INODES!!!! to recover", num)

    def print(self):
        print("***********************")
        print("Device \t\t\t\t", self.device.chosen_device)
        print("Partition \t\t\t", self.device.chosen_partition)
        if not self.device.valid:
            print("\t Code \t\t\t\t", self.device.code)
            print("\t Message \t\t\t", self.device.message)
        else:
            for group in self.groups:
                group.print()
        print("***********************")
