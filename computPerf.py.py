import modele
import os
import json

dossier_image = "./Images"
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
            tab_pieces_etiquettes.append(label["label"])
        
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

print(comp_tab(['piece20', 'piece5', 'piece2'],['piece5', 'piece2', 'piece20']))

precision = test()
print(f"Pourcentage de précision global : {precision}%")
