# Step2-MP3toJSON.py Extract metadata from tmpMP3 files and save it on json files
# Générez les fichier json a partir des mp3 et supprimer les info doublons
import os
import subprocess
from Modules.errors import user_interrupted_operation, missing_mp3_file, metadata_error
from Modules.color import print_colored
from Modules.color import CONFIRMATION_COLOR, ERROR_COLOR, QUESTION_COLOR, END_COLOR

def extract_metadata_and_save_to_json(tmp_MP3):
	try:
		cmd = [
			"ffmpeg",
			"-i", tmp_MP3,
			"-f", "ffmetadata",
			"-"
		]
		metadata_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
		metadata = {}
		lines = metadata_output.split('\n')[8:]  # Ignorer les 8 premières lignes
		for line in lines:
			if "=" in line:
				key, value = line.strip().split("=", 1)
				metadata[key] = value
		json_content = "{\n"
		for key, value in metadata.items():
			json_content += f'\t"{key}": "{value}",\n'
		json_content = json_content.rstrip(",\n") + "\n}"
		
		json_file = os.path.splitext(tmp_MP3)[0] + ".json"
		with open(json_file, 'w') as json_output:
			json_output.write(json_content)
	except subprocess.CalledProcessError as e:
		metadata_error(tmp_MP3, error_message)

def main():
	mp3_files = [f for f in os.listdir('./Result') if f.endswith('.mp3')]
	for tmp_MP3 in mp3_files:
		extract_metadata_and_save_to_json(f'./Result/{tmp_MP3}')

def read_json_with_jq(file_path):
	try:
		result = subprocess.check_output(['jq', '.', file_path], text=True)
		return result
	except subprocess.CalledProcessError as e:
		corrupted_json(str(e))
		return None

if __name__ == "__main":
	try:
		main()
	except KeyboardInterrupt:
		user_interrupted_operation()
