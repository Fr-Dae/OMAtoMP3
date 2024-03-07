# Organiser les fichiers MP3 en parallèle
#!/bin/bash

# Fonction pour traiter un fichier JSON
process_json() {
    json_file="$1"
    [ ! -f "$json_file" ] && return  # Ignorer les fichiers qui ne sont pas réguliers

    author=$(jq -r '.artist' "$json_file")
    [ -z "$author" ] || author="Divers"  # Remplacer les auteurs vides par "Divers"

    cleaned_author=$(echo "$author" | tr -dC '\r' | tr '[:space:]' '-')
    cleaned_author=${cleaned_author%%-}

    existing_author=$(find . -maxdepth 1 -type d -iname "$cleaned_author" | head -n 1)

    [ -n "$existing_author" ] && mv "${json_file%.json}.mp3" "$existing_author/" || (mkdir -p "$cleaned_author" && mv "${json_file%.json}.mp3" "$cleaned_author/")
}

# Parcourir les fichiers JSON dans le dossier actuel et traiter en parallèle
find . -name '*.json' | parallel --bar --jobs 50% process_json

