# Step3-RenameMP3.py Rename tmpMP3 to FinalMP3
# Renommer les fichiers MP3 à partir des fichiers JSON en remplaçant '/' par '-'
import os
import json
import subprocess
from Modules.errors import user_interrupted_operation, rename_error
from Modules.color import print_colored
from Modules.color import CONFIRMATION_COLOR, ERROR_COLOR, QUESTION_COLOR, END_COLOR

def replace_characters(text):
	return text.replace('/', '-')

def main():
	json_files = [f for f in os.listdir('.') if f.endswith('.json')]
	
	for json_file in json_files:
		if os.path.isfile(json_file):
			with open(json_file) as json_data:
				data = json.load(json_data)
				
			track = data.get('OMG_TRACK', '')
			artist = data.get('artist', '')
			album = data.get('album', '')
			title = data.get('title', '')
			
			if track and artist and album and title:
				track = replace_characters(track)
				artist = replace_characters(artist)
				album = replace_characters(album)
				title = replace_characters(title)
				
				mp3_file = f"{track}_{artist}_{album}_{title}.mp3"
#               mp3_file = f"{track}_{title}_{artist}_{album}_.mp3"
				tmp_MP3 = json_file.replace('.json', '.mp3')
				
				try:
					os.rename(tmp_MP3, mp3_file)
				except OSError:
					rename_error(json_file, e)

if __name__ == "__main":
	try:
		main()
	except KeyboardInterrupt:
		user_interrupted_operation()
