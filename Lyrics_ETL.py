import pandas as pd
import json
import os
from helper_functions import create_connection, execute_query, execute_insert_values_query, execute_read_query, clean_lyrics

# The data folder contains the downloaded JSON files for every album. For each file, this will extract the lyrics for each track,
# do some preliminary cleaning, and save it into the database.

# Connect to SQL database
connection = create_connection('lyrics_nlp.sqlite')

# Create table for song lyrics
create_lyrics_table = """
CREATE TABLE IF NOT EXISTS lyrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_title TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT NOT NULL,
    release_year INTEGER,
    song_lyrics TEXT NOT NULL
);
"""
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
            
            # Some albums do not have lyrics for all tracks. Skip over these ones.
            if lyrics != "":
                # Remove first line (song title and contributors), song structure labels, and ending tag.
                lyrics = clean_lyrics(lyrics)
                
                # Load track info and lyrics into database.
                insert_track = """
                INSERT INTO
                    lyrics (song_title, artist, album, release_year, song_lyrics)
                VALUES (?, ?, ?, ?, ?);
                """
                values = (song_title, artist, album_title, year, lyrics)

                execute_insert_values_query(connection, insert_track, values)
                # print(album_title) # to help find errors
print('Lyrics Table Complete.')
print('Creating Artists Table...')
# Create Artist Table
# Import album_list table and reduce to just single entry for each artist.
artist_df = pd.read_excel('album_list.xlsx')
artist_df.drop(columns='Album', inplace=True)
artist_df.drop_duplicates(inplace=True)

# Create table in database
create_artists_table = """
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    region TEXT NOT NULL
);
"""
execute_query(connection, create_artists_table)

# Insert artist df into database table.
artist_df.to_sql('artists', connection, if_exists='replace', index=False)
connection.commit()


# Report Database details
song_count_query = '''
    SELECT COUNT(*) FROM lyrics;
    '''
song_count = execute_read_query(connection, song_count_query)

artist_count_query = '''
    SELECT COUNT(*) FROM artists;
    '''
artist_count = execute_read_query(connection, artist_count_query)
print(f'Database contains lyrics to {song_count[0][0]} songs from {artist_count[0][0]} artists.')