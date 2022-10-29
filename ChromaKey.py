#===============================================================================
import cv2

#===============================================================================

INPUT_IMAGE =  '2.bmp'
INPUT_BACKGROND =  'background.jpg'
#===============================================================================
def giveMeTheMask(img):

 lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
 a_channel = lab[:,:,1] # melhor e mais simples maneira que encontramos descobrir com certa precisão oque é verde e oque não é.

 th = cv2.threshold(a_channel, 106, 255, cv2.THRESH_BINARY_INV)[1] # faz o thereshold com base no canal verde, de acordo com valor estabelecido (106 foi o mais adequado nos testes)

 th2 = cv2.threshold(a_channel, 106, 255, cv2.THRESH_BINARY)[1] 
 nogreenSorce = cv2.bitwise_or(img, img, mask = th2)
 #th = cv2.GaussianBlur(th,(3,3),1)
 th = cv2.bilateralFilter(th, 3,3, 1) # filtro bilateral é superior pois remove o aspeco de contorno nas bordas. 
 return th,nogreenSorce

def merge(mask,img_sorce,background):
 height = img_sorce.shape[1]
 width = img_sorce.shape[0]

 for y in range(height):
  for x in range(width):
   if mask[x,y] > 250:
    img_sorce[x,y] = background[x,y] # faz a troca binária se a mask for muito clara, oque representra sem muito verde
   elif mask[x,y] < 250 and mask[x,y] > 120:  
    img_sorce[x,y] = (((mask[x,y]/255))*background[x,y]) #aplica os pixels do backgrond de acordo com um peso, isso trata as bordos pois a mascara sofreu Blur.

 return img_sorce


background = cv2.imread(INPUT_BACKGROND)
img = cv2.imread(INPUT_IMAGE)

background = cv2.resize(background,(img.shape[1],img.shape[0])) 
mask,nogreenSorce = giveMeTheMask(img)

final_image = merge(mask,nogreenSorce,background)

cv2.imwrite('mask.jpg', mask)
cv2.imwrite('final-image2.jpg',final_image)

#===============================================================================