from scalePicture import *
from display import *
import RPi.GPIO as GPIO
import socket
import time
from sensor import *


GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#UDP_IP = "127.24.1.1"
#UDP_PORT = 8889

#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind((UDP_IP, UDP_PORT))
#filename0 = "HAW.JPEG"
filename0 = "1.JPG"
#filename0 = "red.png"
#filename0 = "gregor."jpg
#filename0 = "pacm00n.png"
#filename0 = "Timo2.JPG"
#filename = "farbtest.png"
#filename1 = "dota.jpeg"
#filename0 = "Milhouse.JPG"
#filename = "Edeler.PNG"
#filename0 = "IMG-20170630-WA0000.jpg"
#filename0 = "Keule.JPG"
#filename = "edeler2.jpg"
#filename1 = "dreieck.jpg"
#filename = "EundP.JPG"
orientation = 0

#orientation = getOrientation()

#udpserver
sequence = 0
while True:
    #data, addr = sock.recvfrom(1024)
    #filename = data

    input_state = GPIO.input(14)
    
    if input_state == False and sequence == 0:
        print("Button Pressed")
        orientation = getOrientation()
        time.sleep(0.2)
        columnCount, delay, ratio = scalePicture(filename0, orientation)
        img = Image.open("scaled-%s"%filename0)
        columns = convertPicture(columnCount, delay, img, orientation)
        playPic(columns, columnCount, ratio)
        #sequence += 1
        input_state = True
        print("Bild durchgelaufen")
           
    if input_state == False and sequence == 1:
        print("Button Pressed")
        orientation = getOrientation()
        time.sleep(0.2)
        columnCount, delay, ratio = scalePicture(filename1, orientation)
        img = Image.open("scaled-%s"%filename1)
        columns = convertPicture(columnCount, delay, img, orientation)
        playPic(columns, columnCount, ratio)
        sequence += 1
        input_state = True
        print("Bild durchgelaufen")
            
    if input_state == False and sequence == 2:
        print("Button Pressed")
        orientation = getOrientation()
        time.sleep(0.2)
        columnCount, delay, ratio = scalePicture(filename2, orientation)
        img = Image.open("scaled-%s"%filename2)
        columns = convertPicture(columnCount, delay, img, orientation)
        playPic(columns, columnCount, ratio)
        sequence = 0
        input_state = True
        print("Bild durchgelaufen")
        