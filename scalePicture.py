from PIL import Image

def scalePicture(filename, orientation):
    
    img = Image.open(filename).convert("RGB")
    
    global basepixel 
    basepixel = 64
    
    if orientation == 90:
        img = img.rotate(270)
    else:
        img = img.rotate(orientation)
    print(orientation)
    
    width = img.size[0]
    height = img.size[1]
    ratio = width/height
    delay = int(height/basepixel)
    if width > 300:
        img = img.resize((300,basepixel), resample=0)
        delay /=int(width/300)
        width = 300    
    else:
        img = img.resize((width,basepixel), resample=0)
    img.save("scaled-%s"%filename)
    
    return (width+1+int(delay)), int(delay), ratio
            
def convertPicture(columnCount, delay, img, orientation):
    
    pixels = img.load()
    width = img.size[0]
    height = img.size[1]

    #Gamma Korrektur-Tabelle (8 zu 7 Bit)
    gamma = bytearray(256)
    for i in range(256):
        gamma[i] = 0x80 | int(0.2 * pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)
    
    #Tabelle für die R,G und B Bytes (Liste von Bytearrays)
    column = [0 for x in range(columnCount)]
    for x in range(columnCount):
    	column[x] = bytearray(height * 3 + 1)
    
    address = [0 for x in range(basepixel)]

    #Adressierungstabelle für die Pixel erstellen
    for n in range(32):
        m = 2*n
        address[n] = 63 - m
        address[63-n] = 64 - (m+1)
    
    #Lade Bildpixel in die Tabelle
    for x in range(columnCount):
        for y in range(basepixel):
           
            if orientation == 90 or orientation == 180:
                if y <= 31:
                    if (delay-1) < x < (columnCount-1):
                        value = pixels[x-delay, address[y]]   
                    else:
                        value = (0, 0, 0) 
                else: 
                    if x >= (columnCount - (delay+1)):
                        value = (0, 0, 0)
                    else:
                        value = pixels[x, address[y]]
            else:
                
                if y > 31:
                    if (delay-1) < x < (columnCount-1):
                        value = pixels[x-delay, address[y]]   
                    else:
                        value = (0, 0, 0) 
                else: 
                    if x >= (columnCount - (delay+1)):
                        value = (0, 0, 0)
                    else:
                        #print(x, y, columnCount);
                        value = pixels[x, address[y]]
                
            y3 = y * 3
            column[x][y3]     = gamma[value[1]]
            column[x][y3 + 1] = gamma[value[0]]
            column[x][y3 + 2] = gamma[value[2]]
            if x == (columnCount-1) and y == 63:
                print(value)
    return column
             
             
