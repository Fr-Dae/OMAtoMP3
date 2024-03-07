# Step1-OMAtoMP3.py Convertir OMA en tmp_MP3 input

import os
import ffmpeg
from Modules.errors import OMA_not_found
from Modules.color import print_colored

# Parcourir le fichier ou dossier INPUT recursivement
def list_oma_files(directory):
	oma_files = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			if file.lower().endswith('.oma'):
				oma_files.append(os.path.join(root, file))
	return oma_files

def main():
	input_directory = "INPUT"
	oma_files = list_oma_files(input_directory)
	
	if oma_files: # Lister les fichier OMA présent
		print("Fichiers OMA trouvés :")
		for oma_file in oma_files:
			print(oma_file)
	else:
		OMA_not_found()

def list_oma_files_by_size(directory):
	oma_files = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			if file.lower().endswith('.oma'):
				oma_files.append(os.path.join(root, file))
	# Trier les fichiers OMA par ordre croissant de taille
	oma_files.sort(key=lambda x: os.path.getsize(x))
	return oma_files

def convert_oma_to_mp3(oma_file, output_dir):
	# Obtenez le nom de fichier sans l'extension
	file_name = os.path.splitext(os.path.basename(oma_file))[0]
	# Définissez le chemin de sortie du fichier MP3
	mp3_file = os.path.join(output_dir, f"{file_name}.mp3")
	print_colored(f"Conversion de {oma_file} en {mp3_file}.", print_colored.CONFIRMATION_COLOR)
	
	try:
		# Utilisez ffmpeg-python pour effectuer la conversion
		(
			ffmpeg
			.input(oma_file)
			.output(mp3_file)
			.run(overwrite_output=True)
		)
	except ffmpeg.Error as e:
		print_colored(f"Erreur lors de la conversion de {oma_file} : {e.stderr}", print_colored.ERROR_COLOR)






# Par ordre croisant (taille) Convertir les fichier OMA via FFMPEG en tmpMP3
parallel --bar --jobs 50% 'ffmpeg -i {} -c:a libmp3lame {.}.mp3' ::: /home/dae/Musique/Walkman/OMGAUDIO2/10F00/*.OMA

# Par ordre croisant (taille) Copier les fichier tmpMP3 vers OUTPUT
cp ~/Musique/Walkman/OMGAUDIO2/10F00/*.mp3 ./Result/ | pv -lep -s $(find ~/Musique/Walkman/OMGAUDIO2/10F00 -maxdepth 1 -type f -name "*.mp3" | wc -l)


# supprimer les fichier tmpMP3 de INPUT

find *.OMA
	total_files = len(input_files)

# Initialisation de la variable tmpMP3 à None
tmpMP3 = None

# Fonction pour renommer le fichier temporaire MP3
def rename_tmp_mp3(input_file):
	global tmpMP3
	tmpMP3 = f"{os.path.splitext(os.path.basename(input_file))[0]}.mp3"

# Copie de input vers output/Result

rm ~/Musique/Walkman/OMGAUDIO2/10F00/*.mp3


if __name__ == "__main":
	main()
