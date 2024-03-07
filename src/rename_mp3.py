"""Renommage de fichiers MP3."""

import os

from modules import log
from modules.process import write_mp3


if __name__ == '__main__':

    print("""
    Avertissement: Cet outil étant dérivé de OMA2MP3, il lit puis réécrit
    chaque fichier MP3, au lieu de les déplacer. Pour traiter une grande
    quantité de fichiers, privilégier l'utilisation d'un outil adapté.
    """)

    # Récupération des entrées
    log.question("Veuillez saisir le chemin du répertoire d'entrée (ou du fichier .mp3) : ", end='')
    input_path = input().strip()
    log.question("Veuillez saisir le chemin du répertoire de sortie : ", end='')
    output_path = input().strip()

    # Création du dossier de destination s'il n'existe pas déjà
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Si un simple fichier .mp3 a été donné, on le déplace
    if os.path.isfile(input_path) and input_path.lower().endswith('.mp3'):
        with open(input_path, 'rb') as mp3_file:
            write_mp3(output_path, mp3_file)

    # Sinon, un dossier a été donné : on convertit tous ses fichiers .oma
    else:

        # Liste de fichiers à traiter
        file_list = [
            os.path.join(root, file)
            for root, _, files in os.walk(input_path)
            for file in files
            if file.lower().endswith('.mp3')
        ]

        # Déplacement des fichiers
        for path in file_list:
            with open(path, 'rb') as mp3_file:
                write_mp3(output_path, mp3_file)
