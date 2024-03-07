# OMAtoMP3
Script python de conversion des fichier Walkman OMA en MP3 avec sauvegarde des metadonnée

## Language utilité
Python 3.8 et sh

OMA2json est un outil en ligne de commande permettant d'extraire les métadonnées des fichiers OMA (Sony OpenMG audio) et de les convertir en fichiers JSON. Ces métadonnées incluent des informations telles que le titre, l'artiste, l'album, le genre et le numéro de piste.

## Prérequis

Avant d'utiliser OMA2json, assurez-vous d'avoir les éléments suivants installés sur votre système :

	Python 3
	Les bibliothèques Python suivantes : mutagen, colorama, tqdm
	`pip install mutagen colorama tqdm`

## Installation

```properties
mkdir ./OMA2MP3
wget -o ./OMA2MP3/OMA2MP3.py
chmod -R 775 ./ 
```
## Utilisation

Pour extraire les métadonnées OMA des fichiers, utilisez la commande suivante :

`python3 OMA2json.py`

Suivez les instructions pour spécifier le chemin du répertoire d'entrée contenant les fichiers OMA. 
Le script traitera ensuite les fichiers, extraiera les métadonnées et générera des fichiers JSON correspondants dans le répertoire de sortie.

le script passera en revue les fichier dans le dossier indiquer, s'il trouve des OMA
il les convertira dans ./Result/ en tmp.mp3
les métadata seront extrait dans un fichier.json du même nom.
puis 
normalement, un dossier par auteur devrais etre creer.

atrac3p (atrac3plus) -> mp3 (libmp3lame)
encoder         : Lavc58.134.100 libmp3lame

## todo
- 01 - Définir couleur
- 02 - Définir barre de progression
- 03 - Définir erreur possible
- 04 - Définir origin (où le script est executer ./)
- 05 - Définir Input [user action] (la sources des fichier a traité)
- 06 - Définir Output [user action] (la destination des fichier , creer un dossier/Result si besoin)
- 07 - Définir le thread (50% par default)
- 08 - Définir json (metadata, memoire cache)
- 09 - Définir autor comme une valeur cache 
- 10 - Définir tmp_mp3 (fichier temporaire de transision)

- Acceder au dossier Input, parcourir la liste des dossier et fichier recursivement a la recherche de fichier OMA
- Sinon, indiqué que le chemin est invalide ou ne contient pas de OMA
- Par ordre croisant (taille) convertir les fichier OMA en tmp_MP3 (mulithread)

- Depuis le tmp_mp3, extraire information json metadata dans le output (le creer si absent)

- A partir des information contenue dans le json, renommer les fichier tmpMP3

- Organiser les fichier en creer des dossier par artiste et déplacer les fichier MP3 dedans.
- supprimer les fichier temporaire inutiles
- afficher un message pour confirmer que c'est fini.

sudo apt install parallel

Step1-OMAtoMP3.sh

Step2-MP3toJSON.sh

Step3-RenameMP3.sh

Step4-JSONtoMP3.py





