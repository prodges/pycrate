from fourni.personnage import Personnage
from fourni.caisse import Caisse
from fourni.cible import Cible
from fourni.mur import Mur
from fourni.case_vide import CaseVide



def creer_image(can, absci, ordone, image):
    '''
    Fonction qui permet de créer/remplacer une image dans le canvas. Pour l'utiliser il faut préciser :
    :param can: un canvas (faites abstraction de ce que c'est et marquez : can
    :param absci: une coordonnée dans l'axe des abscisses ( coordonnée x)
    :param ordone: une coordonnée dans l'axe des ordonnées ( coordonnée y)
    :param image: une image tirée de la liste d'image (voir énoncé pour quelle image choisir via quel index)
    :return:
    '''
    can.create_image(absci, ordone, image=image)


def creer_mur(x,y):
    '''
    Fonction permettant de créer un mur.
    :param x: coordonnée en x du mur à créer
    :param y:coordonnée en y du mur à créer
    :return: la variable mur
    '''
    return Mur(x,y)


def creer_caisse(x,y):
    '''
    Fonction permettant de créer une caisse.
    :param x: coordonnée en x de la caisse à créer
    :param y:coordonnée en y de la caisse à créer
    :return: la variable caisse
    '''
    return Caisse(x,y)

def creer_cible(x,y):
    '''
    Fonction permettant de créer une cible.
    :param x: coordonnée en x de la cible à créer
    :param y:coordonnée en y de la cible à créer
    :return: la variable cible
    '''
    return Cible(x,y)


def creer_personnage(x,y):
    '''
    Fonction permettant de créer un personnage.
    :param x: coordonnée en x du personnage à créer
    :param y:coordonnée en y du personnage à créer
    :return: la variable personnage
    '''
    return Personnage(x,y)


def creer_case_vide(x,y):
    '''
    Fonction permettant de créer une case vide.
    :param x: coordonnée en x de la case vide à créer
    :param y:coordonnée en y de la case vide à créer
    :return: la variable case vide
    '''
    return CaseVide(x,y)


def coordonnee_x(variable):
    '''
    Fonction permettant de retourner la coordonnée en x de la variable.
    :param variable: la variable (Personnage,Caisse, CaseVide, Cible, Mur)
    :return: la coordonnée en x de la variable
    '''
    return variable.get_x()


def coordonnee_y(variable):
    '''
    Fonction permettant de retourner la coordonnée en y de la variable.
    :param variable: la variable (Personnage,Caisse, CaseVide, Cible, Mur)
    :return: la coordonnée en y de la variable
    '''
    return variable.get_y()


def est_egal_a(variable1,variable2):
    '''
    Fonction permettant de tester l'égalité entre 2 variables (Personnage,Caisse, CaseVide, Cible, Mur)
    :param variable1: variable (Personnage,Caisse, CaseVide, Cible, Mur)
    :param variable2: variable (Personnage,Caisse, CaseVide, Cible, Mur)
    :return: Booléen (True si les deux variables sont identiques, False sinon)
    '''
    return variable1.__eq__(variable2)