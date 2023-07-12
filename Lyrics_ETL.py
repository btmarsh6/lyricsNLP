import json
import re
import os

# The data folder contains the downloaded JSON files for every album. For each file, this will extract the lyrics for each track,
# do some preliminary cleaning, and save it into the database.
directory = 'data'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        # Open JSON file and extract album information
        album = json.load(open(f))
        artist = album['artist']['name']
        album_title = album['name']
        year = album['release_date_components']['year']
        print(f'{album_title} by {artist}, released in {year}')

        # Find each track and extract lyrics
        for track in album['tracks']:
            song_title = track['song']['title']
            lyrics = track['song']['lyrics']
            # Remove first line (song title and contributors), song structure labels, and ending tag.
            first_line = r'^.*?\n'
            lyrics = re.sub(first_line, '', lyrics, count=1)

            brackets = r'\[.*?\]'
            lyrics = re.sub(brackets, '', lyrics)
            
            lyrics = lyrics[:-5]

            # Load track info and lyrics into database.
