import json
import re
import os
from helper_functions import create_connection, execute_query, execute_read_query

# The data folder contains the downloaded JSON files for every album. For each file, this will extract the lyrics for each track,
# do some preliminary cleaning, and save it into the database.

# Connect to SQL database
connection = create_connection('lyrics_nlp.sqlite')

# Create table for song lyrics
create_lyrics_table = '''
CREATE TABLE IF NOT EXISTS lyrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_title TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT NOT NULL,
    release_year INTEGER
    song_lyrics TEXT NOT NULL
);
'''
execute_query(connection, create_lyrics_table)

# Extract data from JSON files
directory = 'data'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        # Open JSON file and extract album information
        album = json.load(open(f))
        artist = album['artist']['name']
        album_title = album['name']
        year = album['release_date_components']['year']
        # **VALIDATION**
        # print(f'{album_title} by {artist}, released in {year}')

        # Find each track and extract lyrics
        for track in album['tracks']:
            song_title = track['song']['title']
            lyrics = track['song']['lyrics']
            # Remove first line (song title and contributors), song structure labels, and ending tag.
            first_line = r'^.*?\n'
            lyrics = re.sub(first_line, '', lyrics, count=1)

            structure_labels = r'\[.*?\]'
            lyrics = re.sub(structure_labels, '', lyrics)
            
            embed_tag = r'\d*Embed'
            lyrics = re.sub(embed_tag, '', lyrics)
            
            # Load track info and lyrics into database.
            insert_track = f'''
            INSERT INTO
                lyrics (song_title, artist, album, release_year, song_lyrics)
            VALUES
                ({song_title}, {artist}, {album_title}, {year}, {lyrics});
            '''
            execute_query(connection, insert_track)

# Create Artist Table
