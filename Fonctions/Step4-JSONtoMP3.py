## Step4-JSONtoMP3.py
import os
import subprocess
import json
import shutil
from Modules.errors import user_interrupted_operation, missing_mp3_file
from Modules.color import print_colored
from Modules.color import CONFIRMATION_COLOR, ERROR_COLOR, QUESTION_COLOR, END_COLOR
from Modules.pbar import create_progress_bar

# Fonction pour traiter un fichier JSON
def process_json(json_file):
	if not os.path.isfile(json_file):
		return  # Ignorer les fichiers qui ne sont pas réguliers

	with open(json_file, 'r') as json_data:
		data = json.load(json_data)
	
	author = data.get('artist', 'Divers')  # Remplacer les auteurs vides par "Divers"
	cleaned_author = ''.join(c if c.isalnum() or c.isspace() else '-' for c in author).rstrip('-')
	
	# Vérifier si le dossier de l'auteur nettoyé existe déjà
	existing_author = next((d for d in os.listdir('.') if os.path.isdir(d) and d.lower() == cleaned_author.lower()), None)

	# Déplacer le fichier MP3 dans le dossier de l'auteur correspondant
	mp3_file = os.path.splitext(json_file)[0] + '.mp3'
	if os.path.exists(mp3_file):
		destination_dir = existing_author if existing_author else cleaned_author
		os.makedirs(destination_dir, exist_ok=True)
		new_mp3_file = os.path.join(destination_dir, os.path.basename(mp3_file))
		os.rename(mp3_file, new_mp3_file)
	else:
		missing_mp3_file(json_file)

# Parcourir les fichiers JSON dans le répertoire actuel
json_files = [f for f in os.listdir('.') if f.endswith('.json')]

for json_file in json_files:
	process_json(json_file)

if __name__ == "__main":
	try:
		main()
	except KeyboardInterrupt:
		user_interrupted_operation()
