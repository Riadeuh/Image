import numpy as np
import matplotlib.image as mplimg
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq
import cv2
import math
from PIL import Image

def k_moyenne(img, k):
    image = mplimg.imread(img) #lire l'image en parametre
    nb_cluster = k

    tableau_pixel = image.reshape((-1, 2)) #fait un tableau de i*j lignes avec RVB en colonne
    tableau_pixel = np.float32(tableau_pixel) #converir les données du tableau en float pour utiliser K-means


    couleurs_generales, _ = kmeans(obs=tableau_pixel, k_or_guess=nb_cluster) #on applique K-means



    etiquettes, _ = vq(tableau_pixel, couleurs_generales) #association d'une couelur general pixel par pixel

    couleurs_generales = np.uint8(couleurs_generales)
    tableau_pixel_clusterised = couleurs_generales[etiquettes]

    image_clusterised = tableau_pixel_clusterised.reshape(image.shape)

    return image_clusterised



def to_hsv(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v= cv2.split(hsv)
    ret_s, th_s = cv2.threshold(s,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return th_s


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

    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.3, 60, param1=150, param2=70, minRadius=0, maxRadius=0)

    circles = np.uint16(np.around(circles))

    for c in circles[0, :]:
        cv2.circle(cimg, (c[0], c[1]), c[2], (0, 255, 0), 1)
        cv2.circle(cimg, (c[0], c[1]), 1, (0, 0, 255), 5)
        print(c, math.pi* (c[2] ** 2))

    return cimg

def detect_circles2(img):
    result = cv2.Canny(img, threshold1=100, threshold2=200, apertureSize=3, L2gradient=False)
    return result

def final(img):
    #ALGO POUR K MOYENNE
    image = mplimg.imread(img)  # lire l'image en parametre

    tableau_pixel = image.reshape((-1, 2))  # fait un tableau de i*j lignes avec RVB en colonne
    tableau_pixel = np.float32(tableau_pixel)  # converir les données du tableau en float pour utiliser K-means

    couleurs_generales, _ = kmeans(obs=tableau_pixel, k_or_guess=3)  # on applique K-means

    etiquettes, _ = vq(tableau_pixel, couleurs_generales)  # association d'une couelur general pixel par pixel

    couleurs_generales = np.uint8(couleurs_generales)
    tableau_pixel_clusterised = couleurs_generales[etiquettes]

    image_clusterised = tableau_pixel_clusterised.reshape(image.shape)



    #PASSAGE EN NOIR ET BLANC
    segmentation_result_gris = cv2.cvtColor(image_clusterised, cv2.COLOR_BGR2GRAY)

    # Appliquer une opération de seuillage pour obtenir une image binaire
    _, seuil_image = cv2.threshold(segmentation_result_gris, 128, 255, cv2.THRESH_BINARY)




    #APPLICATION DU FLOU GAUSSIEN
    image_blurred = cv2.GaussianBlur(seuil_image, (7, 7), 6.5)




    #DECTECTION BORD TRANSFORMEE DE HOUGH

    image_copie = image.copy()
    image_blurred = cv2.GaussianBlur(image_blurred, (7, 7), 1.5)
    circles = cv2.HoughCircles(image_blurred, cv2.HOUGH_GRADIENT, 1.3, 60, param1=150, param2=70, minRadius=0, maxRadius=0)

    circles = np.uint16(np.around(circles))



    for c in circles[0, :]:
        cv2.circle(image_copie, (c[0], c[1]), c[2], (0, 255, 0), 3)
        cv2.circle(image_copie, (c[0], c[1]), 1, (0, 0, 255), 5)
        print(c[2], math.pi * (c[2] ** 2))

    plt.imshow(image_copie, cmap="gray")
    plt.show()

"""#SUPPRIMER LES CERCLES INDESIRABLES
    sorted_circles = sorted(circles, key=lambda x: x[2])
    for i in sorted_circles:
        for j in sorted_circles:
            rayon = i[2]
            distance = np.sqrt((i[0] - j[0])**2 + (i[1] - j[1])**2)
            if distance < rayon:
                sorted_circles.remove(j)
    
    #SUPPRIMER LES CERCLES INDESIRABLES 2.0
    for i in range(len(circles)):
        rayon = circles[i][2]
        for j in range(len(circles)):
            #Vérifier si le centre du cercle se trouve à l'intérieur du cercle le plus grand
            distance = np.sqrt((circles[i][0] - circles[j][0]) ** 2 + (circles[i][1] - circles[j][1]) ** 2)
            if distance < rayon:
                # Si le centre du cercle est à l'intérieur du cercle le plus grand, le supprimer
                filtered_circles = np.delete(filtered_circles, np.where((filtered_circles == circles[j]).all(axis=1)), axis=0)

    print(filtered_circles)

    for c in sorted_circles:
        cv2.circle(image_copie, (c[0], c[1]), c[2], (0, 255, 0), 3)
        cv2.circle(image_copie, (c[0], c[1]), 1, (0, 0, 255), 5)
        print(c, math.pi * (c[2] ** 2))"""










#avoir le diametre d'une piece
#calculer le rapport de ce diametre par rapport aux autres
#ecart-type le moins bas = bonne piece






"""
image_de_base = "Images/138.jpeg"
image_level1 = k_moyenne(image_de_base, 3)
image_level2 = to_black_n_white(image_level1)
image_level3 = cv2.GaussianBlur(image_level2, (7, 7), 6.5)
image_level3 = detect_circles2(image_level3)


plt.imshow(image_level3, cmap="gray")
plt.show()
"""

"""
image_de_base = "Images/10.jpg"
image_de_base = mplimg.imread(image_de_base) #lire l'image en parametre
hsv = cv2.cvtColor(image_de_base, cv2.COLOR_BGR2HSV)
h,s,v= cv2.split(hsv)
ret_h, th_h = cv2.threshold(h,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret_s, th_s = cv2.threshold(s,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret_v, th_v = cv2.threshold(v,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


plt.imshow(th_h, cmap="gray")
plt.show()
plt.imshow(th_s, cmap="gray")
plt.show()
plt.imshow(th_v, cmap="gray")
plt.show()
"""




to_hsv("Image/266.jpg")

#137
#138
#139
#157
#162
#163
#164
#165
#170
#171
#172
#173