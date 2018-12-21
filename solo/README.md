# Roboc Project
## An OpenClassRoom exercise

### Prérequis
- Python 3

Le jeu à été uniquement sur Ubuntu, mais il devrait fonctionner sur Mac et 
Windows.

### Lancer le jeu
Aller dans le dossier contenant le script robotc.py
Utiliser la commande suivante (Ubuntu)

`python3 robotc.py`

### Contrôle du robot

Le robot est contrôlable grâce à des commandes entrées au clavier. Il doit 
exister les commandes suivantes :

- Z qui doit permettre de sauvegarder et quitter la partie en cours.
- N qui demande au robot de se déplacer vers le nord (c'est-à-dire le haut de 
votre écran).
- E qui demande au robot de se déplacer vers l'est (c'est-à-dire la droite de 
votre écran).
- S qui demande au robot de se déplacer vers le sud (c'est-à-dire le bas de 
votre écran).
- O qui demande au robot de se déplacer vers l'ouest (c'est-à-dire la gauche 
de votre écran).
Chacune des directions ci-dessus suivies d'un nombre permet d'avancer de 
plusieurs cases (par exemple E3 pour avancer de trois cases vers l'est).
- [1-3] naviguer dans les menus 
 

### Affichage du labyrinthe

Le labyrinthe est vu du dessus. Un symbole représente un obstacle ou votre 
propre robot. Vous pouvez vous référez à l'exemple ci-dessous pour voir 
quelques exemples de partie.

Pour reconnaître la nature des obstacles, on doit bien évidemment représenter 
chaque obstacle par un symbole différent. Sans quoi, difficile de différencier 
les murs des portes de sorties.
