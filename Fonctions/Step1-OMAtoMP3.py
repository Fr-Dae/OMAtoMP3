# Step1-OMAtoMP3.py Convertir OMA en tmp_MP3 input
import os
import ffmpeg
from Modules.errors import OMA_not_found, ffmpeg_Error, user_interrupted_operation
from Modules.color import print_colored
from Modules.color import CONFIRMATION_COLOR, ERROR_COLOR, QUESTION_COLOR, END_COLOR
from Modules.thread import process_files_in_parallel
from Modules.pbar import create_progress_bar

tmp_MP3 = None

# Parcourir le fichier ou dossier INPUT récursivement
def list_oma_files_by_size(directory):
	oma_files = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			if file.lower().endswith('.oma'):
				oma_files.append(os.path.join(root, file))
	# Trier les fichiers OMA par ordre croissant de taille
	oma_files.sort(key=lambda x: os.path.getsize(x))
	return oma_files

def main():
	input_directory = "INPUT"
	oma_files = list_oma_files_by_size(input_directory)
	
	if oma_files:  # Lister les fichiers OMA présents
		print("Fichiers OMA trouvés ")
	else:
		OMA_not_found()

def convert_oma_to_mp3(oma_file, output_dir):
	# Obtenez le nom de fichier sans l'extension
	file_name = os.path.splitext(os.path.basename(oma_file))[0]
	# Définissez le chemin de sortie du fichier MP3
	tmp_MP3 = os.path.join(output_dir, f"{file_name}.mp3")
	
	try:
		# Utilisez create_progress_bar pour créer la barre de progression
		total_files = len(oma_files)
		for input_file in create_progress_bar(oma_files, total_files, "Conversion en cours"):
			print_colored(f"Conversion de {input_file} en {tmp_MP3}.", print_colored.CONFIRMATION_COLOR)
			(
				ffmpeg
				.input(input_file)
				.output(tmp_MP3)
				.run(overwrite_output=True)
			)
	except ffmpeg.Error as e:
		ffmpeg_Error()

if __name__ == "__main":
	try:
		process_files_in_parallel(oma_files, output_directory, convert_oma_to_mp3)
	except KeyboardInterrupt:
		user_interrupted_operation()

