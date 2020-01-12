import time

#from fourni import simulateur
from outils import \
    creer_image, \
    creer_caisse, creer_case_vide, creer_cible, creer_mur, creer_personnage, \
    coordonnee_x, coordonnee_y

# Constantes à utiliser

DISTANCE_ENTRE_CASE: int = 32  # distance par rapport à l'autre case
VALEUR_COUP: int = 50
X_PREMIERE_CASE: int = 20
Y_PREMIERE_CASE: int = 20


# Fonctions à développer

def jeu_en_cours(caisses: list, cibles: list) -> bool:
    """
    Fonction testant si le jeu est encore en cours et retournant un booléen comme réponse sur l'état de la partie.
    :param caisses: La liste des caisses du niveau en cours
    :param cibles: La liste des cibles du niveau en cours
    :return: True si la partie est finie, False sinon
    """
    if caisses in cibles:
        return True
    return False








def charger_niveau(joueur: list, caisses: list, cibles: list, murs: list, path: str):
    """
    Fonction permettant de charger depuis un fichier.txt et de remplir les différentes listes permettant le
    fonctionnement du jeu (joueur, caisses, murs, cibles)
    :param joueur: liste des personnages
    :param caisses: liste des caisses
    :param cibles: liste des cibles
    :param murs: liste des murs
    :param path: chemin du fichier.txt
    :return:
    """
        # Lecture des lignes du fichier et stockage dans une matrice 2D x:y telle que 9:6 
    mx = []
    cases_vides = []
    x = y = 0
    with open(path, 'r') as file_level:
        mx = file_level.readlines()            
        mx = [row.rstrip('\n') for row in mx]  

    # Recherche les differents éléments dans la matrice et crée l'image correspondante sur le board selon les fonctions outils données
    for i in range(len(mx)):
        x = int(X_PREMIERE_CASE + DISTANCE_ENTRE_CASE / 2 + i * 32)
        for j in range(len(mx[i])):
            y = int(Y_PREMIERE_CASE + DISTANCE_ENTRE_CASE / 2 + j *32)
            if mx[i][j] == '#': # Mur
                murs.append(creer_mur(x,y))
            elif mx[i][j] == '-': # Case_vide
                cases_vides.append(creer_case_vide(x,y))
            elif mx[i][j] == '.': # Cible
                cibles.append(creer_cible(x,y))
            elif mx[i][j] == '$':   # Caisse
                caisses.append(creer_caisse(x,y))
            elif mx[i][j] == '@':   # Personnage
                joueur.append(creer_personnage(x,y))


def mouvement(direction: str, can, joueur: list, murs: list, caisses: list, liste_image: list):
    """
    Fonction permettant de définir les cases de destinations (il y en a 2 si le joueur pousse une caisse) selon la
    direction choisie.
    :param direction: Direction dans laquelle le joueur se déplace (droite, gauche, haut, bas)
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param joueur: liste des joueurs
    :param murs: liste des murs

    :param caisses: liste des caisses
    :param liste_image: liste des images (murs, caisses etc...) détaillée dans l'énoncé
    :return:
    """

    if direction == 'droite':        
        xy_coord = creer_case_vide(coordonnee_x(joueur[0]) + 32, coordonnee_y(joueur[0]))
        xy_coord_suiv = creer_case_vide(coordonnee_x(joueur[0]) + 64, coordonnee_y(joueur[0]))

    elif direction == 'gauche':
        xy_coord = creer_case_vide(coordonnee_x(joueur[0] - 32), coordonnee_y(joueur[0]))
        xy_coord_suiv = creer_case_vide(coordonnee_x(joueur[0]) - 64, coordonnee_y(joueur[0]))

    elif direction == 'haut':
        xy_coord = creer_case_vide(coordonnee_x(joueur[0]), coordonnee_y(joueur[0]) - 32)
        xy_coord_suiv = creer_case_vide(coordonnee_x(joueur[0]), coordonnee_y(joueur[0])-64)

    else: # bas
        xy_coord = creer_case_vide(coordonnee_x(joueur[0]), coordonnee_y(joueur[0]) + 32)
        xy_coord_suiv = creer_case_vide(coordonnee_x(joueur[0]), coordonnee_y(joueur[0]) + 64)

    old_caisse = xy_coord # xy coord est un objet de type Case vide avec x,y correspondant

    effectuer_mouvement(xy_coord, xy_coord_suiv, old_caisse, caisses, murs, joueur, can, coordonnee_x(xy_coord_suiv), coordonnee_y(xy_coord_suiv), coordonnee_x(xy_coord), coordonnee_y(xy_coord), liste_image)



def effectuer_mouvement(coordonnee_destination, coordonnee_case_suivante, ancienne_caisse, caisses: list, murs: list, joueur: list, can, deplace_caisse_x: int, deplace_caisse_y: int, deplace_joueur_x: int, deplace_joueur_y: int, liste_image: list):
    """
    Fonction permettant d'effectuer le déplacement ou de ne pas l'effectuer si celui-ci n'est pas possible.
    Voir énoncé "Quelques règles".
    Cette methode est appelée par mouvement.
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
    """
    if coordonnee_destination in caisses:
        if coordonnee_case_suivante in caisses or coordonnee_case_suivante in murs:
            pass
        else:
            player_x: int = coordonnee_x(joueur[0])
            player_y: int = coordonnee_y(joueur[0])
            joueur.append(creer_personnage(deplace_joueur_x, deplace_joueur_y))
            creer_image(can, player_x, player_y, liste_image[6])
            


def chargement_score(scores_file_path: str, dict_scores: dict):
    """
    Fonction chargeant les scores depuis un fichier.txt et les stockent dans un dictionnaire
    :param scores_file_path: le chemin d'accès du fichier
    :param dict_scores:  le dictionnaire pour le stockage
    :return:
    """
    pass










def maj_score(niveau_en_cours: int, dict_scores: dict) -> str:
    """
    Fonction mettant à jour l'affichage des scores en stockant dans un str l'affichage visible
    sur la droite du jeu.
    ("Niveau x
      1) 7699
      2) ... ").
    :param niveau_en_cours: le numéro du niveau en cours
    :param dict_scores: le dictionnaire pour stockant les scores
    :return str: Le str contenant l'affichage pour les scores ("\n" pour passer à la ligne)
    """
    pass











def enregistre_score(temps_initial: float, nb_coups: int, score_base: int, dict_scores: dict,
                     niveau_en_cours: int) -> int:
    """
    Fonction enregistrant un nouveau score réalisé par le joueur. Le calcul de score est le suivant :
    score_base - (temps actuel - temps initial) - (nombre de coups * valeur d'un coup)
    Ce score est arrondi sans virgule et stocké en tant que int.
    :param temps_initial: le temps initial
    :param nb_coups: le nombre de coups que l'utilisateurs à fait (les mouvements)
    :param score_base: Le score de base identique pour chaque partie
    :param dict_scores: Le dictionnaire stockant les scores
    :param niveau_en_cours: Le numéro du niveau en cours
    :return: le score sous forme d'un int
    """
    pass










def update_score_file(scores_file_path: str, dict_scores: dict):
    """
    Fonction sauvegardant tous les scores dans le fichier.txt.
    :param scores_file_path: le chemin d'accès du fichier de stockage des scores
    :param dict_scores: Le dictionnaire stockant les scores
    :return:
    """
    pass








if __name__ == '__main__':
    #simulateur.simulate()
    os.system("fourni\simulateur.py")
    
