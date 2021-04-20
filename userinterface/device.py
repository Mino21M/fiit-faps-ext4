from os import system

def getDevice(devices):
    print("Choose device or file (Default None)")

    for row, dev in enumerate(devices, start=1):
        print("[" + str(row) + "] \t\t" + dev.path)

    return input("[Number]: ") 

def getPartition(partitions):
    row = 1

    print("Choose partition (Default None)")

    for part in partitions:
        filesystem = part.fileSystem
        if filesystem:
            print("[" + str(row) + "] \t\t" + filesystem.type + " partition")
        row += 1

    return input("[Number]: ") 

def getTarget():
    print("Store recovered files in (Default None)")

    return input("[Folder]: ")