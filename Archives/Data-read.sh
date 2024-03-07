#!/bin/bash

# Demander à l'utilisateur de saisir le nom du fichier .dat
read -p "Veuillez saisir le nom du fichier .dat à ouvrir : " nom_fichier

if [ -f "$nom_fichier" ]; then
    # Afficher le contenu du fichier
    cat "$nom_fichier"
else
    echo "Le fichier spécifié n'a pas été trouvé."
fi
