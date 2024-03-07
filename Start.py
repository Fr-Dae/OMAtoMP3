# Start.py - OMA to MP3
# script 0 qui défini l'environnement et les fonctions commune.
__author__ = 'Fr_Dae'

import os
import subprocess
from Modules.pbar import create_progress_bar
from Modules.color import print_colored
from Modules.color import CONFIRMATION_COLOR, ERROR_COLOR, QUESTION_COLOR, END_COLOR
from Modules.errors import handle_error, user_interrupted_operation

# Fonction pour obtenir le chemin du dossier "Modules"
def get_modules_path():
	return os.path.join(os.path.dirname(__file__), 'Modules')

# Fonction pour obtenir le chemin du dossier "Fonctions"
def get_fonctions_path():
	return os.path.join(os.path.dirname(__file__), 'Fonctions')

# Utilisation des fonctions pour obtenir les chemins
modules_path = get_modules_path()
fonctions_path = get_fonctions_path()

# Fonction pour obtenir le répertoire d'origine
def get_origin_path():
	return os.path.dirname(os.path.realpath(__file__))

# Fonction pour obtenir le chemin d'entrée
def get_input():
	print_colored = input("Veuillez saisir le chemin du répertoire d'entrée (ou du fichier .oma) : ", print_colored.QUESTION_COLOR)
	input_path = input().strip()
	return input_path

# Fonction pour obtenir le chemin de sortie
def get_output():
	print_colored("Veuillez saisir le chemin du répertoire de sortie : ", print_colored.QUESTION_COLOR)
	output_path = input().strip()
	return output_path

# Fonction principale
def main():
	origin = get_origin_path()  # Obtenir le répertoire d'origine du script

	input_path = get_input()
	output_path = get_output()

	# Gestion du dossier de sortie
	if output_path == "./":
		output_dir = os.path.join(origin, "Result")
	elif output_path.startswith("~/"):
		output_dir = os.path.expanduser(output_path)
	else:
		output_dir = output_path

	# Créez le répertoire de sortie s'il n'existe pas
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	
	# Obtenez la liste des fichiers d'entrée (à définir en fonction de vos besoins)
	input_files = []  # À compléter avec vos fichiers d'entrée
	total_files = len(input_files)
	metadata_found = False

	# Utilisez create_progress_bar pour afficher une barre de progression
	for input_file in create_progress_bar(input_files, total_files, "Traitement en cours"):
		# Votre traitement ici
		rename_tmp_mp3(input_file)  # Renommez le fichier temporaire MP3
		pass

	if not metadata_found:
		print_colored("Aucune métadonnée trouvée pour les fichiers. Utilisation d'une méthode plus invasive.", print_colored.ERROR_COLOR)

		# Utilisez à nouveau create_progress_bar pour le traitement plus invasif si nécessaire
		for input_file in create_progress_bar(input_files, total_files, "Traitement en cours"):
			print(f"\nTraitement du fichier {input_files.index(input_file) + 1}/{total_files} : {input_file}")
			# Votre traitement plus invasif ici
			pass

# Exécution des scripts
subprocess.run(["python", "Fonctions/Step1-OMAtoMP3.py"], check=True)
subprocess.run(["python", "Fonctions/Step2-MP3toJSON.py"], check=True)
subprocess.run(["python", "Fonctions/Step3-RenameMP3.py"], check=True)
subprocess.run(["python", "Fonctions/Step4-JSONtoMP3.py"], check=True)

print_colored("Travail terminé.", CONFIRMATION_COLOR)

# Supprimer les fichiers JSON
json_files = [f for f in os.listdir('.') if f.endswith('.json')]
for json_file in json_files:
	os.remove(json_file)

print("Ménage des dossiers vides")
# Supprimer les dossiers vides
for root, dirs, files in os.walk('.'):
	for directory in dirs:
		dir_path = os.path.join(root, directory)
		if not os.listdir(dir_path):
			os.rmdir(dir_path)

if __name__ == "__main":
	try:
		process_json()
	except KeyboardInterrupt:
		user_interrupted_operation()

