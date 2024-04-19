import modele
import os
import json

dossier_image = "./Images/validation"
dossier_image_etiquettes = "./Images_etiquettes"

def test() :
    """Calcule la véracité de l'algorithme de reconnaissance

    Args :
        null

    Return :
        Le pourcentage de précision de l'algorithme

    """
    total_pieces = 0
    pieces_correctes = 0

    for image in os.listdir(dossier_image_etiquettes) :

        #création du chemin de l'image dans le dossier étiquettes
        chemin_etiquettes = os.path.join(dossier_image_etiquettes,image)

        #création de la variable qui va contenir les pieces de chaque images étiquettées
        tab_pieces_etiquettes = []

        #ouverture du fichier json
        with open(chemin_etiquettes) as f :
            donnees = json.load(f)
        
        for label in donnees["shapes"] :
            tab_pieces_etiquettes.append((label["label"], trouve_centre_piece(label)))

        
        print(tab_pieces_etiquettes)

        #création de la variable qui va contenir les pieces de chaque images
        tab_pieces = modele.modele(donnees["imagePath"])

        ratio = comp_tab(tab_pieces_etiquettes, tab_pieces)
        print(f"Ratio de précision pour l'image {image}: {ratio}")

        total_pieces += len(tab_pieces_etiquettes)
        pieces_correctes += int(ratio.split('/')[0])

    precision = (pieces_correctes / total_pieces) * 100
    return precision




def comp_tab(tab_e,tab_n) :
    """Compare le tableau de pièces étiquettées et le tableau de pièces résultant de l'algo

    Args :
        tab_e (tab) : tableau de pièces étiquettées
        tab_n (tab) : tableau de pièces normal

    Returns :
        Le ratio de pièces correctement détéctées

    """
    set1 = set(tab_e)
    set2 = set(tab_n)
    
    common_elements_count = sum(1 for elem in set1 if elem in set2)
    
    return f"{common_elements_count}/{len(tab_e)}"

def trouve_centre_piece(piece) :
    """Trouve pour une pièce son centre en fonction des coordonnées établies sur label.me

    Args :
      piece : pièce dont on veut trouver le centre

    Returns : 
      Le point central de la pièce
    
    """
    nb_points = nb_points = len(piece["points"])
    if nb_points == 0:
        return None  # Gestion d'une liste vide

    somme_x = sum(point[0] for point in piece["points"])
    somme_y = sum(point[1] for point in piece["points"])

    centre_x = somme_x / nb_points
    centre_y = somme_y / nb_points

    return (centre_x, centre_y)

print(comp_tab([('piece20',(381,476)),('piece1',(400,500))],[('piece1',(400,500)),('piece20',(381,476))]))

#precision = test()
#print(f"Pourcentage de précision global : {precision}%")

piece = {
      "label": "piece2e",
      "points": [
        [
          513.0,
          512.0
        ],
        [
          557.0,
          504.0
        ],
        [
          603.0,
          510.0
        ],
        [
          635.0,
          536.0
        ],
        [
          667.0,
          572.0
        ],
        [
          673.0,
          618.0
        ],
        [
          667.0,
          666.0
        ],
        [
          633.0,
          710.0
        ],
        [
          589.0,
          728.0
        ],
        [
          529.0,
          730.0
        ],
        [
          479.0,
          704.0
        ],
        [
          447.0,
          650.0
        ],
        [
          449.0,
          578.0
        ],
        [
          475.0,
          538.0
        ]
      ],
      "shape_type": "polygon",
      "flags": {}
    }

print(trouve_centre_piece(piece))

#Essayer de comparer le centre a 20 000 pixels pres pour une précision plus grande