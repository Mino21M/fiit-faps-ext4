from scripts.recover import recover
from sys import byteorder
import parted
import psutil

#ERRORS
#100 - 199: user errors
#200 - 299: not implemented
#300 +    : other catched errors - bugs

#Verbosity
#0 - basic output
#1 - low output
#2 - medium output
#3 - high output
#4 - full output

recover()
