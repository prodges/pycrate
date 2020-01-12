
from fourni import simulateur
from outils import est_egal_a, coordonnee_x, coordonnee_y, creer_caisse, creer_case_vide, creer_cible, creer_image, \
    creer_mur, creer_personnage

import time
import os



# Fonctions à développer

def jeu_en_cours(caisses, cibles)->bool:
    '''
    Fonction testant si le jeu est encore en cours et retournant un booléen comme réponse sur l'état de la partie.
    :param caisses: La liste des caisses du niveau en cours
    :param cibles: La liste des cibles du niveau en cours
    :return: True si la partie est finie, False sinon
    '''
    #if caisses in cibles:
    #    return True
    #return False
    pass

def charger_niveau(joueur, caisses, cibles, murs, path):
    '''
    Fonction permettant de charger depuis un fichier.txt et de remplir les différentes listes permettant le
    fonctionnement du jeu (joueur, caisses, murs, cibles)
    :param joueur: liste des personnages
    :param caisses: liste des caisses
    :param cibles: liste des cibles
    :param murs: liste des murs
    :param path: Chemin du fichier.txt
    :return:
    '''
    listeEndroitsVides: list = []
    fichier = open(path,'r')
    lignes: list = fichier.readlines()
    cptLigne: int = 0

    for ligne in lignes:
        y: int = int(Y_PREMIERE_CASE + DISTANCE_ENTRE_CASE / 2 + cptLigne * 32)
        cptColonnes: int = 0
        for caractere in ligne:
            x: int = int(X_PREMIERE_CASE + DISTANCE_ENTRE_CASE / 2 + cptColonnes * 32)
            if caractere == '#':
                murs.append(creer_mur(x,y))
            elif caractere == '@':
                joueur.append(creer_personnage(x,y))
            elif caractere == '.':
                cibles.append(creer_cible(x,y))
            elif caractere == '$':
                caisses.append(creer_caisse(x,y))
            elif caractere == '-':
                listeEndroitsVides.append(creer_case_vide(x,y))
            cptColonnes += 1
        cptLigne += 1
    fichier.close()


def mouvement(direction, can, joueur, murs, caisses, liste_image):
    '''
    Fonction permettant de définir les cases de destinations (il y en a 2 si le joueur pousse une caisse) selon la
    direction choisie.
    :param direction: Direction dans laquelle le joueur se déplace (droite, gauche, haut, bas)
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param joueur: liste des joueurs
    :param murs: liste des murs
    :param caisses: liste des caisses
    :param liste_image: liste des images (murs, caisses etc...) détaillée dans l'énoncé
    :return:
    '''
    coordonnee_dest = None
    if direction == 'droite':
        coordonnee_dest = creer_case_vide(coordonnee_x(joueur[0])+32,coordonnee_y(joueur[0]))
        coordonnee_dest2 = creer_case_vide(coordonnee_x(joueur[0])+64,coordonnee_y(joueur[0]))
    elif direction == 'gauche':
        coordonnee_dest = creer_case_vide(coordonnee_x(joueur[0])-32,coordonnee_y(joueur[0]))
        coordonnee_dest2 = creer_case_vide(coordonnee_x(joueur[0])-64,coordonnee_y(joueur[0]))
    elif direction == 'haut':
        coordonnee_dest = creer_case_vide(coordonnee_x(joueur[0]),coordonnee_y(joueur[0])-32)
        coordonnee_dest2 = creer_case_vide(coordonnee_x(joueur[0]),coordonnee_y(joueur[0])-64)
    else:
        coordonnee_dest = creer_case_vide(coordonnee_x(joueur[0]),coordonnee_y(joueur[0])+32)
        coordonnee_dest2 = creer_case_vide(coordonnee_x(joueur[0]),coordonnee_y(joueur[0])+64)

    ancienne_caisse = coordonnee_dest
    effectuer_mouvement(coordonnee_dest,coordonnee_dest2,ancienne_caisse,caisses,murs,joueur,can,coordonnee_x(coordonnee_dest2),coordonnee_y(coordonnee_dest2),coordonnee_x(coordonnee_dest),coordonnee_y(coordonnee_dest),liste_image)



def effectuer_mouvement(coordonnee_destination, coordonnee_case_suivante, ancienne_caisse, caisses, murs, joueur, can,
                        deplace_caisse_x, deplace_caisse_y, deplace_joueur_x, deplace_joueur_y, liste_image):
    '''
    Fonction permettant d'effectuer le déplacement ou de ne pas l'effectuer si celui-ci n'est pas possible. Voir énoncé
    "Quelques règles". Cette methode est appelée par mouvement.
    :param coordonnee_destination: variable CaseVide ayant possiblement des coordonnées identiques à une autre variable
    (murs, caisse, casevide)
    :param coordonnee_case_suivante: variable CaseVide ayant possiblement des coordonnées identiques à une autre variable
    (murs, caisse, casevide) mais représente la case après coordonnee_destination
    :param ancienne_caisse: variable utile pour supprimer l'ancienne caisse (après avoir déplacé celle-ci)
    :param caisses: liste des caisses
    :param murs: liste des murs
    :param joueur: liste des joueurs
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param deplace_caisse_x: coordonnée à laquelle la caisse va être déplacée en x (si le joueur pousse une caisse)
    :param deplace_caisse_y: coordonnée à laquelle la caisse va être déplacée en y (si le joueur pousse une caisse)
    :param deplace_joueur_x: coordonnée en x à laquelle le joueur va être après le mouvement
    :param deplace_joueur_y: coordonnée en y à laquelle le joueur va être après le mouvement
    :param liste_image: liste des images (murs, caisses etc...) détaillée dans l'énoncé
    :return:
    '''
    if coordonnee_destination in caisses:
        if coordonnee_case_suivante in caisses or coordonnee_case_suivante in murs:
            pass
        else:
            x_joueur: int = coordonnee_x(joueur[0])
            y_joueur: int = coordonnee_y(joueur[0])
            caisses.append(creer_caisse(deplace_caisse_x,deplace_caisse_y))
            creer_image(can,deplace_caisse_x,deplace_caisse_y,liste_image[2])
            caisses.remove(ancienne_caisse)
            joueur.append(creer_personnage(deplace_joueur_x,deplace_joueur_y))
            creer_image(can,x_joueur,y_joueur,liste_image[6])
            # joueur.pop(0)
            joueur.remove(joueur[0])
    elif coordonnee_destination in murs:
        pass
    else:
        x_joueur: int = coordonnee_x(joueur[0])
        y_joueur: int = coordonnee_y(joueur[0])
        joueur.append(creer_personnage(deplace_joueur_x,deplace_joueur_y))
        creer_image(can,x_joueur,y_joueur,liste_image[6])
        joueur.pop(0)



def chargement_score(scores_file_path, dict_scores):
    '''
    Fonction chargeant les scores depuis un fichier.txt et les stockent dans un dictionnaire
    :param scores_file_path: le chemin d'accès du fichier
    :param dict_scores:  le dictionnaire pour le stockage
    :return:
    '''
    pass


def maj_score(niveau_en_cours, dict_scores)-> str:
    '''
    Fonction mettant à jour l'affichage des scores en stockant dans un str l'affichage visible
    sur la droite du jeu.
    ("Niveau x
      1) 7699
      2) ... ").
    :param niveau_en_cours: le numéro du niveau en cours
    :param dict_scores: le dictionnaire pour stockant les scores
    :return str: Le str contenant l'affichage pour les scores ("\n" pour passer à la ligne)
    '''
    pass


def enregistre_score(temps_initial, nb_coups, score_base, dict_scores, niveau_en_cours)-> int:
    '''
    Fonction enregistrant un nouveau score réalisé par le joueur. Le calcul de score est le suivant :
    score_base - (temps actuel - temps initial) - (nombre de coups * valeur d'un coup)
    Ce score est arrondi sans virgule et stocké en tant que int.
    :param temps_initial: le temps initial
    :param nb_coups: le nombre de coups que l'utilisateurs à fait (les mouvements)
    :param score_base: Le score de base identique pour chaque partie
    :param dict_scores: Le dictionnaire stockant les scores
    :param niveau_en_cours: Le numéro du niveau en cours
    :return: le score sous forme d'un int
    '''
    pass


def update_score_file(scores_file_path, dict_scores):
    '''
    Fonction sauvegardant tous les scores dans le fichier.txt.
    :param scores_file_path: le chemin d'accès du fichier de stockage des scores
    :param dict_scores: Le dictionnaire stockant les scores
    :return:
    '''
    pass


# Constantes à utiliser

DISTANCE_ENTRE_CASE = 32  # distance par rapport à l'autre case
VALEUR_COUP = 50
X_PREMIERE_CASE = 20
Y_PREMIERE_CASE = 20

# Ne pas modifier !
if __name__ == '__main__':
    #os.system("fourni\simulateur.py")
    simulateur.simulate()
