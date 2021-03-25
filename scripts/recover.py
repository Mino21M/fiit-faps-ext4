from userinterface.output import outputer
from scripts.device import device
from scripts.group import group

GROUPPOSITIONS =  [0, 32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 4096000]

class recover():

    def __init__(self):
        self.device = device()
        self.partition_offset = self.device.partition.geometry.start*self.device.device.sectorSize
        self.groups = []
        
        if self.device.valid:
            self.parse()

        outputer(self.print())

    def parse(self):
        for group_number in GROUPPOSITIONS:
            gr = group(group_number, self.device.disk_file, 1024, self.device.directory, self.partition_offset)
            self.groups.append(gr)

    def print(self, verbosity=0):
        text = "DATA RECOVERY TOOL\n"
        text += "Device \t\t\t\t " + self.device.device.path + "\n"
        text += "Partition \t\t\t " + self.device.partition.fileSystem.type + " (" + self.device.partition.name + ")\n"

        if not self.device.valid:
            text += "\t Code \t\t\t\t" + str(self.device.code) + "\n"
            text += "\t Message \t\t\t" + str(self.device.message) + "\n"
        else:
            for group in self.groups:
                text += group.print(verbosity)

        return text
