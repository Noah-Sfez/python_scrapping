Démarrer l'environnement de développement  : 
env/Scripts/activate

Installer les modules dans requirements.txt : 
pip install -r requirements.txt

Lancer le script présent dans app.py


PHASE 1 : 
Récupération de l'url de la page d'un livre sur la page d'accueil
Une fois la l'url dédiée, je récupère toutes les informations nécessaires sur le livre
J'ajoute toutes les informations dans un fichier csv : book.csv

PHASE 2 : 
Modification du code pour en faisant des fonctions pour éviter de réécrire plusieurs les mêmes lignes
Je récupère dedans l'url d'une catégorie, et une fois l'url stockée, je scrappe les données de tous les livres de la catégorie
Si il y'a plusieurs pages à l'intérieur de la catégorie, je passe à la page suivante, une fois tous les livres de la page scrappés

PHASE 3 : 
On ajoute les images des livres que l'on a consulté sur le site, directement dans le dossier images, en renommant les images avec le nom 
des livres.

PHASE 4 : 
On boucle en récupérant tous les livres de toutes les catégories du site. 
Pour chaque catégorie on va créer un fichier csv avec le nom de la catégorie ainsi qu'un dossier pour pouvoir stocker toutes les images des livres
de la catégorie.
Pour chaque catégorie on va stocker toutes les données des livres dans le fichier csv correspondant. 

PHASE 5 : 
On créé le diagramme pour la répartition des livres dans les différentes catégories
On créé également un histogramme pour obtenir le prix moyen des livres dans chaque catégorie