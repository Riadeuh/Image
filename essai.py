import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def to_black_n_white(img):

    segmentation_result_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Appliquer une opération de seuillage pour obtenir une image binaire
    _, seuil_image = cv2.threshold(segmentation_result_gris, 128, 255, cv2.THRESH_BINARY)
    return seuil_image

def to_gray(img):
    image_grise = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return image_grise

def detect_circles(img):
    img = cv2.GaussianBlur(img, (7, 7), 1.5)


    cimg = img
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.3, 60, param1=150, param2=70, minRadius=0, maxRadius=0)

    circles = np.uint16(np.around(circles))

    for c in circles[0, :]:
        cv2.circle(cimg, (c[0], c[1]), c[2], (0, 255, 0), 1)
        cv2.circle(cimg, (c[0], c[1]), 1, (0, 0, 255), 5)

    return cimg


img=cv2.imread ("Images/validation/270.jpg");
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v= cv2.split(hsv)
ret_h, th_h = cv2.threshold(h,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret_s, th_s = cv2.threshold(s,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret_v, th_v = cv2.threshold(v,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#Fusion th_h et th_s
th=cv2.bitwise_or(th_h,th_s)
#Ajouts de bord à l'image
bordersize=10
th=cv2.copyMakeBorder(th, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
#Remplissage des contours
im_floodfill = th.copy()
h, w = th.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
color = (0,255,0)
cv2.floodFill(im_floodfill, mask, (0,0), color)
im_floodfill_inv = cv2.bitwise_not(im_floodfill)
th = th | im_floodfill_inv
#Enlèvement des bord de l'image
th=th[bordersize: len(th)-bordersize,bordersize: len(th[0])-bordersize]
resultat=cv2.bitwise_and(img,img,mask = th)
image_noir = to_black_n_white(resultat)
print(image_noir[1007][521])
plt.imshow(img)
plt.show()
"""contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for i in range (0, len(contours)) :
    mask_BB_i = np.zeros((len(th),len(th[0])), np.uint8)
    x,y,w,h = cv2.boundingRect(contours[i])
    cv2.drawContours(mask_BB_i, contours, i, (255,255,255), -1)
    BB_i=cv2.bitwise_and(img,img,mask=mask_BB_i)
    if h >15 and w>15 :
        BB_i=BB_i[y:y+h,x:x+w]
        plt.imshow(BB_i)
        plt.show()"""


