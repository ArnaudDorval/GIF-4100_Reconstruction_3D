# Planification du projet de reconstruction 3D

## Étapes:
Inspiré de https://en.wikipedia.org/wiki/Computer_stereo_vision#Outline

1. Pré-traitement: Retirer les distortions des caméras (https://en.wikipedia.org/wiki/Distortion_(optics)),

il va peut-être falloir faire une calibration des caméras grâce à une grille d’échecs. Exemple dans Matlab: https://www.youtube.com/watch?v=x6YIwoQBBxA. Il reste à vérifier si les lentilles de nos webcams sont assez bonnes pour ne pas nécessiter ce type de calibration

2. Image rectification (https://en.wikipedia.org/wiki/Image_rectification)

(NON NÉCESSAIRE, car nos deux caméra ont des plans images coplanaires)

3. Stereo matching (https://www.cs.cmu.edu/~16385/s17/Slides/13.2_Stereo_Matching.pdf)

Permet de prendre chaque pixel dans l’image de caméra 1 et trouver le pixel correspondant dans l’image de caméra 2. On a qu’à scanner la ligne horizontale à la même hauteur dans l’image 2. On peut y aller par bloc de pixels similaires comme montré à la page 7 du pdf. Pour optimiser les calculs, on pourrait faire nos calculs sur des tableaux numpy 2d.

4. Projection sur un nuage de points 3d

Grâce aux coordonnées d’un point (x1, y1) dans l’image 1, on trouve le rayon projecteur qui passe par ce point. Puis, on trouve le rayon projecteur qui passe par le point correspondant (x2, y2) dans l’image 2. Ensuite, on trouve l’intersection entre les deux rayons projecteurs ce qui nous donne le point en 3D (x, y, z). On peut ensuite sauvegarder ces points dans un fichier .ply et le visualiser dans un logiciel comme MeshLab.

## Technos à utiliser:
- Python
- Numpy
- OpenCV

## Ressources:

https://medium.com/analytics-vidhya/depth-sensing-and-3d-reconstruction-512ed121aa60

https://github.com/opencv/opencv/blob/master/samples/python/stereo_match.py

https://en.wikipedia.org/wiki/Computer_stereo_vision
