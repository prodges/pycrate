from tkinter import *
from os import listdir
import time
import pyCrate

level_folder_path = '.\\niveaux'
scores_file_path = '.\\scores\\scores.txt'
joueur = []
caisses = []
cibles = []
murs = []
liste_image = []
nb_coups = 0
started: bool = False
can = None
nb_file = 1
DISTANCE_ENTRE_CASE = 32  # distance par rapport à l'autre case
score_start = False
SCORE_BASE = 10000
niveau_en_cours = 0
temps_initial = 0
dict_scores = {}


# fonction qui ferme l'application
def quitter(fenetre):
    fenetre.quit()
    fenetre.destroy()


# fonction qui utilise le fichier texte du nom nivo1.txt, pour
# creer la liste ch du niveau 1


def affichage_jeu(can, liste_image):
    for j in murs:
        pyCrate.creer_image(can, j.get_x(), j.get_y(), liste_image[0])
    for j in cibles:
        pyCrate.creer_image(can, j.get_x(), j.get_y(), liste_image[1])
    for j in caisses:
        pyCrate.creer_image(can, j.get_x(), j.get_y(), liste_image[2])
        for c in cibles:
            if j.__eq__(c):
                pyCrate.creer_image(can, j.get_x(), j.get_y(), liste_image[3])
    for j in joueur:
        pyCrate.creer_image(can, j.get_x(), j.get_y(), liste_image[4])
        for c in cibles:
            if j.get_x() == c.get_x() and j.get_y() == c.get_y():
                pyCrate.creer_image(can, j.get_x(), j.get_y(), liste_image[5])


def charger_niveau(path, fenetre, can, liste_image):
    global started, joueur, caisses, cibles, murs, niveau_en_cours, temps_initial
    tmp_str = path.split("level")[1]
    niveau_en_cours = tmp_str.split(".")[0]
    can.delete(ALL)
    joueur, caisses, cibles, murs = [], [], [], []
    pyCrate.charger_niveau(joueur, caisses, cibles, murs, path)
    affichage_jeu(can, liste_image)
    can.bind_all("<Right>", lambda event, f=fenetre: droite(f))
    can.bind_all("<Left>", lambda event, f=fenetre: gauche(f))
    can.bind_all("<Up>", lambda event, f=fenetre: haut(f))
    can.bind_all("<Down>", lambda event, f=fenetre: bas(f))
    can.pack()
    refresh_score()
    started = True
    temps_initial = time.time()


# fonction qui creer une fenetre popup
def PopupAide():
    popup = Toplevel()
    popup.title("Instructions")
    bouton = Button(popup, text="Fermer", command=popup.withdraw)
    bouton.pack()


## Vérifier la commande
def load_levels(filemenu, fenetre, can, liste_image):
    files = [f for f in listdir(level_folder_path) if f.endswith('.txt')]
    cpt_niveau = 1
    for file in files:
        tag = "Niveau " + str(cpt_niveau)
        path = level_folder_path + "\\" + file
        filemenu.add_command(label=tag, command=lambda x=path: charger_niveau(x, fenetre, can, liste_image))
        cpt_niveau += 1


def init_menu(fenetre, can, liste_image):
    menu = Menu(fenetre)
    fenetre.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="Choix du niveau", menu=filemenu)
    load_levels(filemenu, fenetre, can, liste_image)
    menu.add_command(label="Exit", command=lambda fenetre=fenetre: update_score_file(fenetre))


def check_status(liste_image, can):
    global started
    if pyCrate.jeu_en_cours(caisses, cibles) and started == True:
        affichage_jeu(can, liste_image)
        save_score(temps_initial, nb_coups)
        can.bind_all("<Right>")
        can.bind_all("<Left>")
        can.bind_all("<Up>")
        can.bind_all("<Down>")
        started = False
    else:
        affichage_jeu(can, liste_image)


def mouvement(direction):
    pyCrate.mouvement(direction, can, joueur, murs, caisses, liste_image)


def droite(fenetre):
    global nb_coups
    if started:
        mouvement("droite")
    nb_coups += 1
    check_status(liste_image, can)


def gauche(fenetre):
    global nb_coups
    if started:
        mouvement("gauche")
    nb_coups += 1
    check_status(liste_image, can)


def haut(fenetre):
    global nb_coups
    if started:
        mouvement("haut")
    nb_coups += 1
    check_status(liste_image, can)


def bas(fenetre):
    global nb_coups
    if started:
        mouvement("bas")
    nb_coups += 1
    check_status(liste_image, can)


def load_scores():
    global scores_file_path
    pyCrate.chargement_score(scores_file_path, dict_scores)


def refresh_score():
    score_affichage = pyCrate.maj_score(niveau_en_cours, dict_scores)
    score_label.config(text=score_affichage)


def save_score(temps_initial, nb_coups):
    score = pyCrate.enregistre_score(temps_initial, nb_coups, SCORE_BASE, dict_scores, niveau_en_cours)
    for i in range(0, len(dict_scores[niveau_en_cours]) - 1):
        if int(score) > float(dict_scores[niveau_en_cours][i]):
            tmp = dict_scores[niveau_en_cours][i]
            dict_scores[niveau_en_cours][i] = score
            score = tmp
    refresh_score()


def update_score_file(fenetre):
    pyCrate.update_score_file(scores_file_path, dict_scores)
    quitter(fenetre)


fenetre = Tk()
fenetre.title('Projet 631-1')
# Référence sur les images (obligatoire avec tkinter)

img_mur = PhotoImage(file='.\\images\\wall.gif')
img_cible = PhotoImage(file=".\\images\\dock.gif")
img_boite = PhotoImage(file=".\\images\\box.gif")
img_boite_correcte = PhotoImage(file=".\\images\\box_docked.gif")
img_joueur = PhotoImage(file=".\\images\\worker.gif")
img_joueur_cible = PhotoImage(file=".\\images\\worker_dock.gif")
img_sol = PhotoImage(file=".\\images\\floor.gif")
liste_image.append(img_mur)
liste_image.append(img_cible)
liste_image.append(img_boite)
liste_image.append(img_boite_correcte)
liste_image.append(img_joueur)
liste_image.append(img_joueur_cible)
liste_image.append(img_sol)
can = Canvas(fenetre, height=760, width=1000, bg="#fedcb2")
can.pack(side=LEFT)
score_label = Label(fenetre, anchor="nw", font="Cooper", justify="left", bg="#d8c09e", fg="black",
                    text=load_scores(), height=21, width=38)
score_label.pack()
init_menu(fenetre, can, liste_image)

t = Label(fenetre, anchor="s", font="Cooper", bg="#d8c09e", fg="black", pady="20",
          text="_______________________________________\n\nRègles du jeu \n \n Déplacez le personnage à l'aide des flèches \n du clavier afin de placer toutes les caisses\n sur les emplacements.",
          height=18, width=38)
t.pack(side=LEFT)
fenetre.resizable(height=0, width=0)
fenetre.protocol("WM_DELETE_WINDOW", lambda fenetre=fenetre: update_score_file(fenetre))
fenetre.mainloop()
