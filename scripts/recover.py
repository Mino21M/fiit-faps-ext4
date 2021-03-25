from userinterface.progress import start, update
from userinterface.output import outputer
from scripts.constants import BOOTSECTORSIZE
from scripts.device import device
from scripts.group import group

GROUPPOSITIONS =  [0, 32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 4096000]

class recover():

    def __init__(self):
        self.device = device()
        self.partition_offset = self.device.partition.geometry.start*self.device.device.sectorSize
        self.groups = []
        self.sections = self.create()
        
        if self.device.valid:
            self.parse()

        outputer(self.print())

    def parse(self):
        for num, group_number in enumerate(GROUPPOSITIONS):
           self.groups.append(self.group(num, group_number))

    def group(self, num, group_number):
        gr = group(group_number, self.device.disk_file, BOOTSECTORSIZE, self.device.directory, self.partition_offset)
        update(self.sections, num)
        
        return gr


    def create(self):
        sections = []

        for _ in GROUPPOSITIONS:
            section = "GROUP"
            sections.append(section)

        start(sections)
        return sections


    def print(self, verbosity=0):
        text = "DATA RECOVERY TOOL\n"
        text += "Device \t\t\t\t " + self.device.device.path + "\n"
        text += "Partition \t\t\t " + self.device.partition.fileSystem.type + " (" + str(self.device.partition.number) + ", " + str(self.device.partition.getLength("MB")) + "MB)\n"

        if not self.device.valid:
            text += "\t Code \t\t\t\t" + str(self.device.code) + "\n"
            text += "\t Message \t\t\t" + str(self.device.message) + "\n"
        else:
            for group in self.groups:
                text += group.print(verbosity)

        return text
