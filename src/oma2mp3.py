"""Conversion de fichiers OMA en MP3."""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm

from modules import errors, log, process


if __name__ == '__main__':

    # Récupération des entrées
    log.question("Veuillez saisir le chemin du répertoire d'entrée (ou du fichier .oma) : ", end='')
    input_path = input().strip()
    log.question("Veuillez saisir le chemin du répertoire de sortie : ", end='')
    output_path = input().strip()

    # Inutile de traiter séparément les cas « ./ », « ~ » et « / », Python le
    # gère déjà

    # Création du dossier de destination s'il n'existe pas déjà
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:

        # Si un simple fichier .oma a été donné, on le convertit
        if os.path.isfile(input_path) and input_path.lower().endswith('.oma'):
            process.convert(input_path, output_path)

        # Sinon, un dossier a été donné : on convertit tous ses fichiers .oma
        else:

            # Liste de fichiers à traiter
            file_list = [
                os.path.join(root, file)
                for root, _, files in os.walk(input_path)
                for file in files
                if file.lower().endswith('.oma')
            ]

            # Erreur s'il n'y a aucun fichier .oma
            if len(file_list) == 0:
                raise errors.NoOMAFilesError()

            # Barre de progression
            file_number = len(file_list)
            progress_bar = tqdm.tqdm(
                total=file_number, dynamic_ncols=True, leave=False, position=0
            )

            # Exécution en parallèle
            with ThreadPoolExecutor() as executor:
                futures = []
                for file in file_list:
                    futures.append(executor.submit(process.convert, file, output_path))

                # Pour chaque future complétée
                for future in as_completed(futures):

                    # S'il y a une erreur, l'afficher
                    # Sinon, ajouter 1 à la valeur de la barre de progression
                    try:
                        future.result()
                        progress_bar.update(1)
                    except Exception as error:
                        log.error(str(error))

    # Si l'utilisateur interrompt le traitement
    except KeyboardInterrupt:
        log.error("Opération interrompue par l'utilisateur.")

    # S’il y a une autre erreur, on l'affiche en rouge
    except Exception as error:
        log.error(str(error))
