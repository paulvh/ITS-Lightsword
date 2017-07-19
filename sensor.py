import smbus
import math
import time 

 
def read_byte(reg):
    bus = smbus.SMBus(1)
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    bus = smbus.SMBus(1)
    address = 0x68
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 


 
#print("Gyroskop")
#print("--------")
 
#gyroskop_xout = read_word_2c(0x43)
#gyroskop_yout = read_word_2c(0x45)
#gyroskop_zout = read_word_2c(0x47)
 
#print("gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131))
#print("gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131))
#print("gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131))



def getReadings():    
     # Register
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c
    
    bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
    address = 0x68       # via i2cdetect
    
    # Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)
    
    beschleunigung_xout = read_word_2c(0x3b)
    beschleunigung_yout = read_word_2c(0x3d)
    beschleunigung_zout = read_word_2c(0x3f)
 
    x = beschleunigung_xout / 16384.0
    y = beschleunigung_yout / 16384.0
    z = beschleunigung_zout / 16384.0
    
    return x,y,z
    
    
   


#    xDeg, yDeg = getAngle()
avec = [0]*10000
velocity = 0  

def getSpeed(x,y,z):    
    global avec
    global velocity
    a = math.sqrt(x*x+y*y+z*z)
    print(x)
    avec.append(a)
    avec.pop(0)
    svec = sorted(avec)
    a_md = svec[ len(svec)//2 ]
    c = a_md - a
    velocity += c
    #print("%10.3f"%velocity)

#while True:
    #x,y,z = getReadings()
    #getSpeed(x,y,z)
    
def getOrientation():
    x,y,z = getReadings()
    xDeg = get_x_rotation(x, y, z)
    yDeg = get_y_rotation(x, y, z)
    
        
    if -40 <= xDeg <= 40 and -130 <= yDeg <= -50:
        orientation = 180 
        
        
    elif 50 <= xDeg <= 130:
        orientation = 90
         
        
    elif -130 <= xDeg <= -50:
        orientation = 270
        
    else:
        orientation = 0
        
    return orientation