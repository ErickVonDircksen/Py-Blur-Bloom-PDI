from pickle import TRUE
import sys
import timeit
import numpy as np
import cv2

#INPUT_IMAGE =  'test_small.bmp'
INPUT_IMAGE =  'b01 - Original.bmp'
ALTURA_MIN = 4
LARGURA_MIN = 4
N_PIXELS_MIN = 4

def naiveBlur(img,height,length):
    soma = 0
    img_B = img.copy()

    for y in range(2,height-2,1):
        for x in range(2,length-2,1): #range funcionando para a imagem b não para a imagem a ???????
            for (i, j) in box8(x,y):  
                 soma +=  img[i][j]
                  

            img_B[x][y]= soma/9 
            soma = 0   
    return img_B  


def splitBlur(img,height,length):
    img_X = img.copy() # copy cria uma imagem nova, não apenas aponta a imagem nova pra antiga. 
    img_Y = img.copy()
    soma_Y = 0
    soma_X = 0
    for y in range(2,height-2,1):
        for x in range(2,length-2,1): #range funcionando para a imagem b não para a imagem a ???????
            for (i, j) in box3_Y(x,y):  
                 soma_Y +=  img[i][j]
            for (i, j) in box3_X(x,y):  
                 soma_X +=  img[i][j]                 
                  

            img_X[x][y]= soma_X/3 
            img_Y[x][y]= soma_Y/3
            soma_Y = 0   
            soma_X = 0

 
    return cv2.addWeighted(img_X,0.5,img_Y,0.5,0) # faz a união das duas imgens:   cv.addWeighted(imagem1,peso,imagem2,peso,gamma) 
    
def integralBlur(img,height,length):
 img_B = img.copy() 
 cv2.integral(img)

 return 0   


def box3_X(x,y):
    return [(x - 1, y), (x,y), (x + 1, y)]

def box3_Y(x,y):
    return [(x, y - 1),(x,y), (x, y + 1)]

def box8(x,y):
    return [(x - 1, y), (x,y), (x + 1, y), (x, y - 1), (x, y + 1),(x - 1, y+1), (x + 1, y+1), (x-1, y - 1), (x+1, y - 1)]

def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    height = img.shape[0] 
    length = img.shape[1]   

    start_time = timeit.default_timer ()
    
    img_B=splitBlur(img,height,length)

    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    cv2.imshow ('01 - output.png', img_B) 
    cv2.imwrite ('01 - output.png', img_B)

    
   # # É uma boa prática manter o shape com 3 valores, independente da imagem ser
   # # colorida ou não. Também já convertemos para float32.
   # img = img.reshape ((img.shape [0], img.shape [1], 1))
   # img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    #img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
   # if NEGATIVO:
       # img = 1 - img
    #img = binariza (img, THRESHOLD)
    #cv2.imshow ('01 - binarizada', img)
    #cv2.imwrite ('01 - binarizada.png', img*255)

    #start_time = timeit.default_timer ()
    #componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    #n_componentes = len (componentes)
    #print ('Tempo: %f' % (timeit.default_timer () - start_time))
    #print ('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    #for c in componentes:
       # cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    #cv2.imshow ('02 - out', img_out)
    #cv2.imwrite ('02 - out.png', img_out*255)
    #cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()