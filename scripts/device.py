from os import path, remove
from .constants import errors
import parted

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


def getDevice():
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

    return recover

def getPartition(recover):
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
    
    return recover