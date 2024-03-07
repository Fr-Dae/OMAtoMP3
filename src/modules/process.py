"""Conversion de fichier OMA en MP3."""

import tempfile
import os
import subprocess

from collections import defaultdict
from string import Formatter

import taglib

from constants import DEST_FORMAT
from modules import errors


def write_mp3(dest_dir: str, file) -> None:
    """Écrire le fichier .mp3 au bon emplacement."""

    # Récupérations des tags MP3
    # vers un dictionnaire « defaultdict », c'est-à-dire qui a une valeur par
    # défault (ici « Unkown ») si une des valeurs n'est pas définie
    with taglib.File(file.name) as song:
        tags = defaultdict(lambda: 'Unkown')
        for key, values in song.tags.items():
            tags[key] = '-'.join(values)

    # Formattage du chemin de destination avec les tags
    formatter = Formatter()
    dest_path = [dest_dir] + [
        formatter.vformat(x, (), tags) for x in DEST_FORMAT
    ]

    # Création du dossier de destination s'il n’existe pas déjà
    dest_dir_str = os.path.join(*dest_path[:-1])
    if not os.path.exists(dest_dir_str):
        os.makedirs(dest_dir_str)

    # Écriture du fichier MP3 dans le fichier de destination
    dest_path_str = os.path.join(*dest_path)
    with open(dest_path_str, 'wb') as mp3_file:
        mp3_file.write(file.read())


def convert(oma_file: str, dest_dir: str) -> None:
    """Convertir un fichier OMA en MP3 au bon emplacement."""

    # On utilise un fichier temporaire dans /tmp, comme ça pas besoin de
    # créer des fichiers intermédiaires dans le dossier de destination et de les
    # supprimer à la main après
    with tempfile.NamedTemporaryFile(suffix='.mp3') as tmp_mp3:

        # Conversion du fichier OMA en MP3 vers `tmp_mp3`
        # Je lance la commande à la main au lieu d'utiliser une librairie
        # pour avoir plus de contrôle et pouvoir corriger notamment le problème
        # d'inputs en arrière-plan
        try:
            subprocess.run(
                ['ffmpeg', '-y', '-i', oma_file, tmp_mp3.name],
                input='',
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except:
            raise errors.FFMPEGError(oma_file)

        # Écriture du fichier .mp3 au bon endroit
        write_mp3(dest_dir, tmp_mp3)
