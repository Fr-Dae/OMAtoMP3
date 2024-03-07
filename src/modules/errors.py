"""Erreurs possibles durant l'exécution du programme."""


class NoOMAFilesError(Exception):
    def __init__(self):
        super().__init__("Aucun fichier .oma trouvé dans le répertoire spécifié.")


class FFMPEGError(Exception):
    def __init__(self, file: str):
        super().__init__(f"Erreur FFMPEG avec le fichier {file}.")
