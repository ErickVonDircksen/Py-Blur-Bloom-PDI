import sys
import timeit
import numpy as np
import cv2
# Universidade Tecnológica Federal do Paraná
#===============================================================================
# Alunos Erick H. Dircksen e André L. Gomes


INPUT_IMAGE =  'GT2.bmp'
K_SIZE = 3
ITER = 4
SIGMA = 4
ALPHA = 0.9

def bloomG(img):
    aux = 1
    img_out= img.copy()
    for aux in range(ITER):
        img_out+=cv2.GaussianBlur(img_out,(K_SIZE,K_SIZE),SIGMA + aux)
        aux *=2 
    return img_out    

def bloomBox(img):
    img_out= img.copy()
    for aux in range(ITER):
        img_out += cv2.blur(img_out,(K_SIZE,K_SIZE))   
        aux+=1 
    return img_out    

def blend(img,img2):
   
    return (img*ALPHA)+(img2*(1 - ALPHA))

def main ():

    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    img = img.reshape ((img.shape [0], img.shape [1], 3))
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # cria a escala de cinza que vai servir pra encontrar as fontes de luz
    
    img = img.astype (np.float32) / 255    
    
    (T, thresh) = cv2.threshold(gray, 0, 255,   #cria a mascara de luz, usando um thresholding automático provido pelo  cv2.THRESH_OTSU
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)        # threshold automático foi utilizado pra evitar ter que mudar manualmente para cada imagem.
    print("[INFO] otsu's thresholding value: {}".format(T)) # informa o threshold utilizado
    
    start_time = timeit.default_timer ()
   
    img2 = cv2.bitwise_and(img,img,mask=thresh) 

    blurred_mask_Box = bloomBox(img2) 
    
    blurred_mask = bloomG(img2) 

    final_image_Box = blend(img,blurred_mask_Box)
    final_image_G = blend(img,blurred_mask)
    
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    cv2.imwrite ('Box-output.png', final_image_Box * 255)
    cv2.imwrite ('Gaussian-output.png', final_image_G * 255)

if __name__ == '__main__':
    main ()
