# MP3toJSON.sh Extract metadata from tmpMP3 files and save it on json files

# Générez les fichier json a partir des mp3 et supprimer les info doublons
for file in ./Result/*.mp3; do
  metadata=$(ffmpeg -i "$file" -f ffmetadata - 2>&1 | grep -E "title|artist|album|genre|track|OMG_TRACK")
  metadata=$(echo "$metadata" | tail -n +9)  # Supprimer les 8 premières lignes
  json="{"
  while IFS= read -r line; do
	IFS== read -ra pair <<< "$line"
	key="${pair[0]}"
	value="${pair[1]}"
	json="$json\n\t\"$key\":\"$value\","
  done <<< "$metadata"
  json="${json%,}"  # Supprimer la virgule finale
  json="$json\n}"
  # Supprimer les espaces inutiles dans les clés du JSON
  json=$(echo "$json" | sed -e 's/^[ \t]*//' -e 's/[ \t]*$//')
  echo -e "$json" > "${file%.*}.json"
done
