# thread.py - Gestion du multi thread pour le parallélisme de tâches complexes

import concurrent.futures
import os
from Modules.color import print_colored
from threading import Lock
from Modules.errors import handle_exception
from Modules.errors import handle_error
from Modules.color import CONFIRMATION_COLOR, ERROR_COLOR, QUESTION_COLOR, END_COLOR

# Fonction pour obtenir le nombre de threads disponibles
def get_thread_count():
	return os.cpu_count()

# Fonction pour effectuer une tâche de traitement sur un fichier
def process_file(file_path):
	# Insérez votre traitement de fichier ici (copie, conversion, etc.)
	# Par exemple, ici nous affichons le nom du fichier
	print(f"Traitement du fichier : {file_path}")

# Fonction principale pour le traitement en parallèle
def process_files_in_parallel(file_list):
	thread_count = get_thread_count()
	thread_usage = thread_count // 2 # Utilisation de 50% des threads disponibles
#   thread_usage = thread_count * 3 // 4  # Utilisation de 75% des threads disponibles
	print_colored(f"Utilisation de {thread_usage} threads sur {thread_count} disponibles.", print_colored.CONFIRMATION_COLOR)

	lock = Lock()  # Création d'un verrou pour gérer la concurrence lors de l'affichage

	# Exécution parallèle des tâches
	with concurrent.futures.ThreadPoolExecutor(max_workers=thread_usage) as executor:
		future_to_file = {executor.submit(process_file, file): file for file in file_list}
		for future in concurrent.futures.as_completed(future_to_file):
			file = future_to_file[future]
			try:
				future.result()
			except Exception as e:
				with lock:
					handle_exception(file, e)  # Utilisation de la fonction d'erreur définie

## Copy past me
#	from Modules.thread import process_file
#	if __name__ == "__main":
#	    input_files = ["file1.txt", "file2.txt", "file3.txt"]  # Remplacez par votre liste de fichiers à traiter
#	    process_files_in_parallel(input_files)
