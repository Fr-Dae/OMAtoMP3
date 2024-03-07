## OMA2MP3.py - OMA to MP3

import os
import subprocess
import shutil
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK
import concurrent.futures
import multiprocessing

def get_max_threads():
    # Obtenez le nombre de cœurs CPU disponibles
    max_threads = multiprocessing.cpu_count()
    # Utilisez la moitié du nombre de threads disponibles
    return max_threads // 2

def print_red(text):
    RED = '\033[91m'
    END = '\033[0m'
    print(RED + text + END)

def print_yellow(text):
    YELLOW = '\033[93m'
    END = '\033[0m'
    print(YELLOW + text + END)

def print_cyan(text):
    CYAN = '\033[96m'
    END = '\033[0m'
    print(CYAN + text + END)

def process_oma_file(input_oma_file, result_dir, total_files, converted_files, metadata_cache):
    try:
        # Chemins des fichiers d'entrée et de sortie
        input_mp3_file = os.path.join(result_dir, f'tmp_{os.path.splitext(os.path.basename(input_oma_file))[0]}.mp3')
        json_file = os.path.join(result_dir, f'tmp_{os.path.splitext(os.path.basename(input_oma_file))[0]}.json')
        output_mp3_file = os.path.join(result_dir, f'{os.path.splitext(os.path.basename(input_oma_file))[0]}.mp3')

        if not os.path.exists(input_mp3_file):
            # Conversion du fichier OMA en MP3 s'il n'existe pas déjà
            convert_oma_to_mp3_file(input_oma_file, input_mp3_file)

        # Vérifiez si les métadonnées sont déjà en cache
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as json_in:
                metadata = json.load(json_in)
        else:
            # Extraction des métadonnées en utilisant Mutagen
            tags = extract_metadata(input_mp3_file)

            # Créez un dictionnaire de métadonnées utiles
            metadata = {
                "title": tags.get("TIT2", ["Unknown Title"])[0],
                "artist": tags.get("TPE1", ["Unknown Artist"])[0],
                "album": tags.get("TALB", ["Unknown Album"])[0],
                "track": tags.get("TRCK", ["1"])[0]
            }

            # Écrivez les métadonnées dans un fichier JSON
            with open(json_file, 'w', encoding='utf-8') as json_out:
                json.dump(metadata, json_out, ensure_ascii=False, indent=4)

        # Renommage du fichier MP3 avec le bon titre
        rename_mp3_with_metadata(input_mp3_file, metadata)


    except Exception as e:
        print_red(f"Erreur lors de la conversion du fichier {os.path.basename(input_oma_file)}: {e}")

def convert_oma_to_mp3_file(input_oma_file, output_mp3_file):
    # Convertir le fichier OMA en MP3 en utilisant un outil approprié (par exemple, ffmpeg)
    ffmpeg_cmd = f"ffmpeg -i '{input_oma_file}' '{output_mp3_file}' -y >> convert.log 2>&1"
    subprocess.run(ffmpeg_cmd, shell=True, check=True)

def organize_mp3_by_artists(result_dir):
    mp3_files = [f for f in os.listdir(result_dir) if f.lower().endswith('.mp3')]
    metadata_cache = {}

    for mp3_file in mp3_files:
        json_file = os.path.join(result_dir, f'{os.path.splitext(mp3_file)[0]}.json')
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as json_in:
                metadata = json.load(json_in)
                artist = metadata.get("artist", "Unknown Artist")
                artist_dir = os.path.join(result_dir, artist)
                os.makedirs(artist_dir, exist_ok=True)
                shutil.move(os.path.join(result_dir, mp3_file), os.path.join(artist_dir, mp3_file))
            os.remove(json_file)

def main():
    print_yellow("Veuillez saisir le chemin du répertoire d'entrée :")
    input_path = input()
    print_yellow("Veuillez saisir le chemin du répertoire de sortie :")
    output_dir = input()

    convert_oma_to_mp3_file(input_path, output_dir)
    organize_mp3_by_artists(os.path.join(output_dir, 'Result'))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_red("\nOpération interrompue par l'utilisateur.")
