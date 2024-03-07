# Step3-RenameMP3.sh Rename tmpMP3 to FinalMP3

# Renommer les fichiers MP3 à partir des fichiers JSON en remplaçant '/' par '-'
for json_file in ./*.json; do
    if [ -f "$json_file" ]; then
        track=$(jq -r '.OMG_TRACK' "$json_file")
        artist=$(jq -r '.artist' "$json_file")
        album=$(jq -r '.album' "$json_file")
        title=$(jq -r '.title' "$json_file")

        [ -n "$track" ] && [ -n "$artist" ] && [ -n "$album" ] && [ -n "$title" ] && {
            track="${track//\//-}"
            artist="${artist//\//-}"
            album="${album//\//-}"
            title="${title//\//-}"
            # rename
            new_filename="${track}_${artist}_${album}_${title}.mp3"
            mp3_file="${json_file%.json}.mp3"
            mv "$mp3_file" "$new_filename"
        }
    fi
done
