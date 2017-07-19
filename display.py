from RPi.GPIO import *
from PIL import Image
import time
 


def playPic(column, columnCount, ratio):
    speed = ratio/5
    dev = "/dev/spidev0.0"
    
    spidev = open(dev, "wb")
    
    
   
    
    for x in range(columnCount):
        spidev.write(column[x])
        spidev.flush()
        time.sleep(5/columnCount)
        #(ratio/speed)

    black = bytearray(64 * 3 + 1)

    spidev.write(black)
    spidev.flush()