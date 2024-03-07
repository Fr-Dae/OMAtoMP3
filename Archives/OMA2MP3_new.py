# OMA2MP3.py - OMA to MP3 
# convertion de fichier audio propio sony en fichier exploitable avec memoire json

import os
import subprocess
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK
import shutil

# Couleurs
ERROR_COLOR = "31"  		# Rouge
QUESTION_COLOR = "33"  		# Jaune
CONFIRMATION_COLOR = "36"  	# Cyan

# Fonction pour afficher du texte en couleur
def print_colored(text, color_code):
	print(f"\033[{color_code}m{text}\033[0m")

# Fonction principale
def main():
	print_colored("Veuillez saisir le chemin du répertoire d'entrée (ou du fichier .oma) : ", QUESTION_COLOR)
	input_path = input()

	if os.path.isfile(input_path):
		# Cas d'un fichier unique
		input_dir = os.path.dirname(input_path)
		input_files = [input_path]
	else:
		# Cas d'un dossier
		input_dir = input_path
		input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith('.oma')]

	if not input_files:
		print_colored("Aucun fichier .oma trouvé dans le répertoire spécifié.", ERROR_COLOR)
		return

	print_colored("Veuillez saisir le chemin du répertoire de sortie : ", QUESTION_COLOR)
	output_dir = input()

	if not os.path.exists(output_dir):
		print_colored("Répertoire de sortie non trouvé.", ERROR_COLOR)
		return

	if input_dir == output_dir:
		print_colored("Le répertoire d'entrée est le même que le répertoire de sortie. Veuillez spécifier un répertoire de sortie différent.", ERROR_COLOR)
		return

	# Appeler la fonction pour extraire les métadonnées des fichiers OMA
	for input_file in input_files:
		extract_metadata_to_json(input_file, output_dir)

	# Appeler la fonction pour convertir les fichiers OMA
#   for input_file in input_files:
#       convert_oma_files([input_file], output_dir)

# Fonction pour extraire les métadonnées d'un fichier OMA en JSON
def extract_metadata_to_json(input_file, output_dir):
	try:
		# Vérifier si le fichier OMA a des métadonnées valides
		audio = MP3(input_file)
		if audio.tags is not None:
			tags = audio.tags
			title = tags.get("TIT2", ["Unknown Title"])[0]
			artist = tags.get("TPE1", ["Unknown Artist"])[0]
			album = tags.get("TALB", ["Unknown Album"])[0]
			track = tags.get("TRCK", ["1"])[0]

			# Création d'un dictionnaire contenant les métadonnées
			metadata = {
				"title": title,
				"artist": artist,
				"album": album,
				"track": track
			}

			# Stockage des métadonnées dans un fichier JSON
			metadata_file = os.path.splitext(input_file)[0] + '.json'
			with open(metadata_file, 'w') as json_file:
				json.dump(metadata, json_file)

			print_colored(f"Métadonnées extraites : {metadata_file}", CONFIRMATION_COLOR)
		else:
			print_colored(f"Le fichier OMA ne contient pas de métadonnées valides : {input_file}", ERROR_COLOR)
	except Exception as e:
		print_colored(f"Erreur lors de l'extraction des métadonnées du fichier OMA {input_file}: {e}", ERROR_COLOR)


# Fonction pour convertir un fichier OMA en MP3
def convert_oma_files(input_file, output_dir):
	try:
		# Conversion du fichier OMA en MP3 (Input.OMA > Input.mp3)
		output_mp3 = os.path.splitext(input_file)[0] + '.mp3'
		ffmpeg_cmd = f"ffmpeg -i '{input_file}' '{output_mp3}' > /dev/null 2>&1"
		subprocess.run(ffmpeg_cmd, shell=True, check=True)

		# Vérifier si le fichier MP3 a des métadonnées valides avant de les extraire
		audio = MP3(output_mp3)
		if audio.tags is not None:
			tags = audio.tags
			title = tags.get("TIT2", ["Unknown Title"])[0]
			artist = tags.get("TPE1", ["Unknown Artist"])[0]
			album = tags.get("TALB", ["Unknown Album"])[0]
			track = tags.get("TRCK", ["1"])[0]

			# Création d'un dictionnaire contenant les métadonnées
			metadata = {
				"title": title,
				"artist": artist,
				"album": album,
				"track": track
			}
			# Stockage des métadonnées dans un fichier JSON
			metadata_file = os.path.splitext(output_mp3)[0] + '.json'
			with open(metadata_file, 'w') as json_file:
				json.dump(metadata, json_file)
				
			# Renommage du fichier MP3 en fonction des métadonnées (Input.mp3 > Output.MP3)
			new_filename = f"{track}_{artist}_{album}_{title}.mp3"
			final_mp3 = os.path.join(output_dir, new_filename)
			shutil.move(output_mp3, final_mp3)

			# Renommage du fichier MP3 en fonction des métadonnées (Input.mp3 > Output.MP3)
			new_filename = f"{track}_{artist}_{album}_{title}.mp3"
			final_mp3 = os.path.join(output_dir, new_filename)
			shutil.move(output_mp3, final_mp3)

#            # Suppression du fichier JSON temporaire
#            os.remove(metadata_file)

			print_colored(f"Conversion terminée : {new_filename}", CONFIRMATION_COLOR)

		else:
			print_colored(f"Le fichier MP3 ne contient pas de métadonnées valides : {input_file}", ERROR_COLOR)
	except Exception as e:
		print_colored(f"Erreur lors de la conversion du fichier {input_file}: {e}", ERROR_COLOR)

# Fonction pour organiser les fichiers MP3 par artiste
def organize_mp3_by_artist(output_dir):
	artist_folders = {}  # Dictionnaire pour stocker les chemins des dossiers d'artistes

	# Parcourir les fichiers JSON dans le répertoire de sortie
	for root, _, files in os.walk(output_dir):
		for file in files:
			if file.endswith('.json'):
				json_file = os.path.join(root, file)
				with open(json_file, 'r') as json_data:
					data = json.load(json_data)
					artist = data.get("artist", "Unknown Artist")

					# Normalisation du nom de l'artiste (convertir en minuscules et supprimer "The ")
					normalized_artist = artist.lower().replace("the ", "")

					# Créer un dossier pour l'artiste s'il n'existe pas déjà
					artist_folder = os.path.join(output_dir, normalized_artist)
					if not os.path.exists(artist_folder):
						os.makedirs(artist_folder)
					artist_folders[normalized_artist] = artist_folder

	# Déplacer les fichiers MP3 correspondants dans les dossiers d'artistes
	for artist, artist_folder in artist_folders.items():
		for root, _, files in os.walk(output_dir):
			for file in files:
				if file.endswith('.mp3'):
					mp3_file = os.path.join(root, file)
					with open(os.path.splitext(mp3_file)[0] + '.json', 'r') as json_data:
						data = json.load(json_data)
						mp3_artist = data.get("artist", "Unknown Artist")
						# Normalisation du nom de l'artiste dans les fichiers MP3 pour la correspondance
						normalized_mp3_artist = mp3_artist.lower().replace("the ", "")
						if normalized_mp3_artist == artist:
							shutil.move(mp3_file, os.path.join(artist_folder, file))

	# Suppression du fichier JSON temporaire
#	os.remove(metadata_file)

# Fonction pour convertir un dossier récursivement
def convert_oma_in_directory(input_dir, output_dir):
	oma_files = []
	for root, dirs, files in os.walk(input_dir):
		for file in files:
			if file.lower().endswith('.oma'):
				oma_files.append(os.path.join(root, file))

	if not oma_files:
		print_colored("Aucun fichier .oma trouvé dans le répertoire spécifié.", ERROR_COLOR)
		return

	result_dir = os.path.join(output_dir, 'Result')
	os.makedirs(result_dir, exist_ok=True)

	total_files = len(oma_files)
	converted_files = 0

	oma_files.sort(key=lambda x: os.path.getsize(x))

	for oma_file in oma_files:
		input_file = oma_file
		convert_oma_file(input_file, result_dir)
		converted_files += 1
		print_colored(f"Conversion terminée ({converted_files}/{total_files}). Fichier OMA : {oma_file}", CONFIRMATION_COLOR)

	# Compteur de progression
	total_files = len(oma_files)
	converted_files = 0

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print_colored("Opération interrompue par l'utilisateur.", ERROR_COLOR)
