from math import floor
import sys
import timeit
import numpy as np
import cv2
# Universidade Tecnológica Federal do Paraná
#===============================================================================
# Partially working code.




INPUT_IMAGE =  'b01 - Original.bmp'
K_SIZE = 9

def naiveBlur(img, height, length, channels):
    soma = 0
    img_B = img.copy()
    pixels_janela = 0
    margin= floor(K_SIZE/2)

    for z in range(channels):
        for y in range(margin,height-margin):
            for x in range(margin,length-margin):
                for i in range(-K_SIZE, 0):
                    for j in range(0,K_SIZE):
                        if(y+i >= 0 and y+i < length-1 and x+j >= 0 and x+j < height-1):
                            soma += img[y + i, x + j, z]                  
                            pixels_janela += 1
                if(pixels_janela != 0):
                    img_B[y, x, z]= soma/pixels_janela
                pixels_janela=0
                soma = 0   
    return img_B  


def splitBlur(img, height, length, channels):
    img_X = img.copy()
    img_Y = img.copy()
    margin= floor(K_SIZE/2)
    soma_Y = 0
    soma_X = 0
    pixels_janela = 0
    for z in range(channels):
        for y in range(margin,height-margin):
            for x in range(margin,length-margin):
                for i in range(int(-K_SIZE), 0):
                    if(y+i >= 0 and y+i < length-1):
                        soma_Y += img[y + i, x, z]
                        pixels_janela += 1
                if(pixels_janela != 0):
                    img_Y [y, x, z] = soma_Y/pixels_janela
                pixels_janela=0
                soma_Y = 0

    for z in range(channels):
        for y in range(margin,height-margin):
            for x in range(margin,length-margin):
                for j in range(0, int(K_SIZE)):
                    if(x >= 0 and x + j < length-1):
                        soma_X += img_Y[y, x + j, z]
                        pixels_janela += 1
                if(pixels_janela != 0):
                    img_X [y, x, z] = soma_X/pixels_janela
                pixels_janela=0
                soma_X = 0

    return img_X
    

        
def integralBlur(img,height,length,channels):
    img = img.astype (np.float32) / 255
    img_B = img.copy() 

    intg_img = cv2.integral(img)
   
    margin= floor(K_SIZE/2)

    for z in range(channels):
        for y in range(margin,height-margin):
            for x in range(margin,length-margin):
                img_B[x,y,z]= box_value(intg_img,x,y,z)

    return img_B  

def box_value(intg_img,x,y,z):
   
    a= intg_img[x-floor((K_SIZE/2)),y-floor((K_SIZE/2)),z]

    b= intg_img[x-floor((K_SIZE/2)),y+floor((K_SIZE/2)),z]
    
    c= intg_img[x+floor((K_SIZE/2)),y-floor((K_SIZE/2)),z] 

    d= intg_img[x+floor((K_SIZE/2)),y+floor((K_SIZE/2)),z]
  
    return d - b - c + a 

def main ():

    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    height = img.shape[0] 
    length = img.shape[1] 
    channels = img.shape[2]  
    img = img.reshape ((img.shape [0], img.shape [1], 3))
   
    start_time = timeit.default_timer ()
    
    #img_B=naiveBlur(img, height, length, channels)

    #img_B=splitBlur(img, height, length, channels)

    #img_B=integralBlur(img, height, length, channels)

    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    
    cv2.imwrite ('01 - output.png', img_B)


if __name__ == '__main__':
    main ()



