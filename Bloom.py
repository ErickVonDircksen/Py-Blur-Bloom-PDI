import sys
import timeit
import numpy as np
import cv2
# Universidade Tecnológica Federal do Paraná
#===============================================================================
# Alunos Erick H. Dircksen e André L. Gomes


INPUT_IMAGE =  'b01 - Original.bmp'
K_SIZE = 5
ITER = 5

def bloomG(img):
    aux = 1
    for aux in range(ITER):
        img+=cv2.GaussianBlur(img,(K_SIZE,K_SIZE),aux)
        aux *=2 
    return img    


def bloomBox(img):
    for aux in range(ITER):
        img += cv2.blur(img,(K_SIZE,K_SIZE))   
        aux+=1 
    return img    

def blend(img1,img2):
    height = img1.shape[0] 
    length = img1.shape[1] 
    
    for y in range(height):
            for x in range(length):
                if(img2[x][y] != 0).all():
                    img1[x][y]+= img2[x][y]

    return img1  

def main ():

    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()
    
    img = img.reshape ((img.shape [0], img.shape [1], 3))
    
    start_time = timeit.default_timer ()
   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    
    (T, thresh) = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print("[INFO] otsu's thresholding value: {}".format(T))
  
    img2 = cv2.bitwise_and(img,img,mask=thresh)
    
    final2 = blend(img,img2)
   
    final_img = bloomG(img) 
    


    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    
    cv2.imwrite ('01 - output.png', final2)


if __name__ == '__main__':
    main ()
