from lyricsgenius import Genius
import os
import pandas as pd

def get_artist_album(df):
    artist = df['Artist']
    album_name = df['Album']
    return artist, album_name

def download_lyrics(df):
    """
    Takes the dataframe of artist/albums and downloads the lyrics for each album as a JSON file.
    """
    artist, album_name = get_artist_album(df)
    try:
        album = genius.search_album(album_name, artist)
        album.save_lyrics(overwrite=True)
    except:
        print(f'Failed on: {album_name} by {artist}')

# Import list of albums
album_list_df = pd.read_excel('album_list.xlsx')

# Initialize genius object
token = os.environ['GENIUS_TOKEN']
genius = Genius(token)

# Download lyrics files
album_list_df.apply(download_lyrics, axis=1)