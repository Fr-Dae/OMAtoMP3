# OMA2MP3.py - OMA to MP3

import os
import subprocess
import shutil
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK

def main():
    print("\033[93mVeuillez saisir le chemin du répertoire d'entrée : \033[0m")
    input_path = input()
    print("\033[93mVeuillez saisir le chemin du répertoire de sortie (ou appuyez sur Entrée pour utiliser le dossier d'exécution actuel) : \033[0m")
    output_dir = input()
    
    if not output_dir:  # Si l'utilisateur appuie sur Entrée pour le dossier de sortie, utilisez le dossier d'exécution actuel
        output_dir = os.path.dirname(os.path.abspath(__file__))
    else:  # Sinon, créez le dossier de sortie spécifié par l'utilisateur s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
    
    result_dir = os.path.join(output_dir, "Result")  # Créez le dossier "Result" dans le dossier de sortie
    os.makedirs(result_dir, exist_ok=True)

def convert_oma_to_mp3_file(input_oma_file, output_mp3_file):
    # Convertir le fichier OMA en MP3 en utilisant un outil approprié (par exemple, ffmpeg)
    ffmpeg_cmd = f"ffmpeg -i '{input_oma_file}' '{output_mp3_file}' -y >> convert.log 2>&1"
    subprocess.run(ffmpeg_cmd, shell=True, check=True)

def extract_metadata(input_mp3_file):
    # Extraction des métadonnées en utilisant Mutagen
    audio = MP3(input_mp3_file)
    return audio.tags

def write_metadata_to_json(json_file, metadata):
    # Écriture des métadonnées dans un fichier JSON
    with open(json_file, 'w', encoding='utf-8') as json_out:
        json.dump(metadata, json_out, ensure_ascii=False, indent=4)

def rename_mp3_with_metadata(output_mp3_file, metadata):
    # Renommage du fichier MP3 avec le bon titre
    new_filename = f"{metadata['track']}_{metadata['artist']}_{metadata['album']}_{metadata['title']}.mp3"
    os.rename[output_mp3_file, os.path.join(os.path.dirname(output_mp3_file), new_filename)]

def convert_oma_to_mp3(input_path, output_dir):
    # Créez un sous-répertoire "Result" dans le répertoire de sortie si nécessaire
    result_dir = os.path.join(output_dir, 'Result')
    os.makedirs(result_dir, exist_ok=True)

    # Obtenez une liste des fichiers .oma et .mp3 dans le répertoire d'entrée, triés par taille
    oma_files = sorted([f for f in os.listdir(input_path) if f.lower().endswith('.oma')], key=lambda f: os.path.getsize(os.path.join(input_path, f)))

    if not oma_files:
        print("\033[91mAucun fichier .oma trouvé dans le répertoire spécifié.\033[0m")
        return

    # Compteur de progression
    total_files = len(oma_files)
    converted_files = 0

    for oma_file in oma_files:
        try:
            # Chemins des fichiers d'entrée et de sortie
            input_oma_file = os.path.join(input_path, oma_file)
            input_mp3_file = os.path.join(input_path, f'tmp_{os.path.splitext(oma_file)[0]}.mp3')
            json_file = os.path.join(input_path, f'tmp_{os.path.splitext(oma_file)[0]}.json')
            output_mp3_file = os.path.join(result_dir, f'{os.path.splitext(oma_file)[0]}.mp3')

            if not os.path.exists(input_mp3_file):
                # Conversion du fichier OMA en MP3 s'il n'existe pas déjà
                convert_oma_to_mp3_file(input_oma_file, input_mp3_file)

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
            write_metadata_to_json(json_file, metadata)

            # Renommage du fichier MP3 avec le bon titre
            rename_mp3_with_metadata(input_mp3_file, metadata)

            # Mise à jour de la progression
            converted_files += 1
            print(f"\033[96mConversion terminée ({converted_files}/{total_files}). Fichier MP3 : {output_mp3_file}\033[0m")

        except Exception as e:
            print(f"\033[91mErreur lors de la conversion du fichier {oma_file}: {e}\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\033[91m\nOpération interrompue par l'utilisateur.\033[0m")
