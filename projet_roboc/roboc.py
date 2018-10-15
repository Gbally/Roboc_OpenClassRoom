#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# XXX
# =============================================================================
#            XXX
# =============================================================================
# PROJECT : XXX
# FILE : roboc.py
# DESCRIPTION :
"""
XXX

Requirements:
XXX

========= ============== ======================================================
Version   Date           Comment
========= ============== ======================================================
0.1.0     2018/10/15     Creation
========= ============== ======================================================
"""

# [IMPORTS]--------------------------------------------------------------------
import os

from carte import Carte

# [MODULE INFO]----------------------------------------------------------------
__author__ = 'Guillaume Bally'
__date__ = '2018/10/15'
__copyright__ = 'XXX'
__version__ = '0.1.0'
__maintainer__ = 'Guillaume Bally'
__email__ = 'XXX'

# [GLOBALS] -------------------------------------------------------------------




# [CLASS]----------------------------------------------------------------------

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

map = Carte

# On charge les cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-3].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
            # Création d'une carte, à compléter

# On affiche les cartes existantes
print("Labyrinthes existants :")
for i, carte in enumerate(cartes):
    print("  {} - {}".format(i + 1, carte.nom))

# Si il y a une partie sauvegardée, on l'affiche, à compléter

# ... Complétez le programme ...
