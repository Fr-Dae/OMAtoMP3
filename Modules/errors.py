# Error.py - Gestion des erreurs communes
import threading
from Modules.color import print_colored
from Modules.color import CONFIRMATION_COLOR, ERROR_COLOR, QUESTION_COLOR, END_COLOR


def invalid_input_path():
	print_colored("Chemin d'entrée invalide. Le chemin doit pointer vers un fichier .oma ou un répertoire contenant des fichiers .oma.", ERROR_COLOR)

def no_oma_files_found():
	print_colored("Aucun fichier .oma trouvé dans le répertoire spécifié.", ERROR_COLOR)

def missing_mp3_file(json_file):
	print_colored(f"Fichier MP3 manquant pour {json_file}.", ERROR_COLOR)
	
def corrupted_json(json_files):
	print_colored("Erreur lors de la lecture du fichier JSON avec jq : {e}", ERROR_COLOR)	

def metadata_error(ouput_file, error_message):
	print_colored(f"Error extracting metadata from {ouput_file}: {error_message}", print_colored.ERROR_COLOR)

def metadata_extraction_error(input_file, error_message):
	print_colored(f"Erreur lors de l'extraction des métadonnées du fichier OMA {input_file}: {error_message}", ERROR_COLOR)

def metadata_error(ouput_file, error_message):
	print_colored(f"Error extracting metadata from {tmp_MP3}: {error_message}", print_colored.ERROR_COLOR)

def user_interrupted_operation():
	print_colored("Opération interrompue par l'utilisateur.", ERROR_COLOR)

lock = threading.Lock() # Verrou pour la gestion des impressions dans les threads

def print_colored(text, color_code):
	print(f"{color_code}{text}{Style.RESET_ALL}")

def handle_error(message, error_type=ERROR_COLOR):
	with lock:
		print_colored(message, error_type)

def handle_exception(file, e):
	with lock:
		print_colored(f"Erreur lors du traitement du fichier {file}: {e}", ERROR_COLOR)    

def OMA_not_found():
	print_colored("Aucun fichier OMA trouvé dans le répertoire spécifié.", ERROR_COLOR)

def ffmpeg_Error():
		print_colored(f"Erreur lors de la conversion de {oma_file} : {e.stderr}", print_colored.ERROR_COLOR)

def rename_error(file, e):
		print_colored(f"Impossible de renommer {tmp_MP3}")

## select error and copy past it
#	from Modules.error import invalid_input_path, no_oma_files_found, missing_mp3_file
#	
#	if not os.path.isfile(input_path):
#	    invalid_input_path()
#	    return
#	elif not input_files:
#	    no_oma_files_found()
#	    return
#	
#	# Si une erreur survient lors de l'extraction des métadonnées :
#	try:
#	    process_json()
#	except Exception as e:
#	    metadata_extraction_error(input_file, str(e))
#	
