# OMA2json.py - Conversion des fichiers OMA en MP3 et extraction des métadonnées
__author__ = "Fr-Dae", "OpenAI"

import os
import json
import subprocess
from colorama import Fore, Style
from mutagen.mp3 import MP3
from tqdm import tqdm
from colorama import Fore, Style

# Couleurs
ERROR_COLOR = Fore.RED
QUESTION_COLOR = Fore.YELLOW
CONFIRMATION_COLOR = Fore.CYAN

# Fonction pour afficher du texte en couleur
def print_colored(text, color_code):
    print(f"{color_code}{text}{Style.RESET_ALL}")

# Fonction principale
def main():
    print_colored("Veuillez saisir le chemin du répertoire d'entrée (ou du fichier .oma) : ", QUESTION_COLOR)
    input_path = input()

    if os.path.isfile(input_path):
        # Cas d'un fichier unique
        input_files = [input_path]
    elif os.path.isdir(input_path):
        # Cas d'un dossier
        input_files = [os.path.join(root, filename) for root, _, filenames in os.walk(input_path) for filename in filenames if filename.lower().endswith('.oma')]
    else:
        print_colored("Chemin d'entrée invalide. Le chemin doit pointer vers un fichier .oma ou un répertoire contenant des fichiers .oma.", ERROR_COLOR)
        return

    if not input_files:
        print_colored("Aucun fichier .oma trouvé dans le répertoire spécifié.", ERROR_COLOR)
        return

    print_colored("Veuillez saisir le chemin du répertoire de sortie : ", QUESTION_COLOR)
    output_dir = input()

    # Créez le répertoire de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    total_files = len(input_files)
    metadata_found = False

    # Créez une barre de progression avec tqdm
    def pbar(iterable, total, desc):
        progress_bar = tqdm(total=total, desc=desc, dynamic_ncols=True, leave=False, position=0)
        for i, item in enumerate(iterable, start=1):
            progress_bar.update(1)
            yield item
            progress_bar.set_description(f"{desc} - {i}/{total}")
        progress_bar.close()

    for input_file in pbar(input_files, total_files, "Traitement en cours"):
        output_file = convert_oma_to_mp3(input_file, output_dir)
        if output_file:
            metadata = extract_metadata_from_mp3(output_file)
            if metadata:
                metadata_found = True
                json_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(output_file))[0]}.json")
                with open(json_file_path, 'w') as json_file:
                    json.dump(metadata, json_file, indent=4)

    if not metadata_found:
        print_colored("Aucune métadonnée trouvée pour les fichiers. Utilisation d'une méthode plus invasive.", ERROR_COLOR)

        for input_file in pbar(input_files, total_files, "Traitement en cours"):
            print(f"\nTraitement du fichier {input_files.index(input_file) + 1}/{total_files} : {input_file}")
            output_file = convert_oma_to_mp3(input_file, output_dir)
            if output_file:
                metadata = extract_metadata_from_mp3(output_file)
                if metadata:
                    json_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(output_file))[0]}.json")
                    with open(json_file_path, 'w') as json_file:
                        json.dump(metadata, json_file, indent=4)

    print_colored("Travail terminé.", CONFIRMATION_COLOR)

# Convert OMA to MP3
def convert_oma_to_mp3(input_file, output_dir):
    try:
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + ".mp3")
        subprocess.run(["ffmpeg", "-i", input_file, output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_file
    except Exception as e:
        return None

# Extract metadata from MP3
def extract_metadata_from_mp3(input_file):
    try:
        oma_tags = MP3(input_file)
        metadata = {}
        if 'title' in oma_tags:
            metadata['title'] = oma_tags['title'][0]
        if 'artist' in oma_tags:
            metadata['artist'] = oma_tags['artist'][0]
        if 'album' in oma_tags:
            metadata['album'] = oma_tags['album'][0]
        if 'genre' in oma_tags:
            metadata['genre'] = oma_tags['genre'][0]
        if 'track' in oma_tags:
            metadata['track'] = oma_tags['track'][0]
        return metadata
    except Exception as e:
        return None

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("Opération interrompue par l'utilisateur.", ERROR_COLOR)
