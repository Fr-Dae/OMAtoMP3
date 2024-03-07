# pbar.py

from tqdm import tqdm

# Créez une barre de progression avec tqdm
def create_progress_bar(iterable, total, desc):
	progress_bar = tqdm(total=total, desc=desc, dynamic_ncols=True, leave=False, position=0)
	for i, item in enumerate(iterable, start=1):
		progress_bar.update(1)
		yield item
		progress_bar.set_description(f"{desc} - {i}/{total}")
	progress_bar.close()

## Copy past this on other script !
#	from Modules.pbar import create_progress_bar
#	total_files = len(input_files)
#	
#	# Utilisez create_progress_bar pour créer la barre de progression:
#	for input_file in create_progress_bar(input_files, total_files, "Traitement en cours"):
#		# Votre traitement ici
#		# Par exemple, vous pouvez appeler convert_oma_to_mp3, extract_metadata_from_mp3, etc.
