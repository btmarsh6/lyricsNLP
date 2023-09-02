import re
import sqlite3
from sqlite3 import Error
from gensim.utils import simple_preprocess
import spacy
from nltk.corpus import stopwords

def clean_lyrics(lyrics):
    """ (str) -> str
    Takes the raw lyrics string from the JSON files and prepares it to be stored in the database.
    """
    # Remove first line (contributors and song title)
    first_line = r'^.*Lyrics'

    # Remove tags in the text indicating song structure (verse, chorus, etc.)
    square_bracket_labels = r'\[.*?\]'

    curly_bracket_labels = r'\{.*?\}'

    repeats = r'(?i)repeat \d+x'
    
    # Remove embed tag at end of lyrics.
    embed_tag = r'\d*Embed'

    # Remove 'You might also like'
    recommender = r'You might also like'
    
    # Remove ticket ad
    ticket_tag = r'See .*? LiveGet tickets as low as \$\d*'


    expressions = [first_line, square_bracket_labels, curly_bracket_labels, repeats, embed_tag, recommender, ticket_tag]
    for expression in expressions:
        lyrics = re.sub(expression, '', lyrics)
    
    return lyrics


# Functions to help execute SQL commands

def create_connection(path):
    """ (str) -> Connection obj
    """
    connection = None
    try:
        connection = sqlite3.connect(path)
        print('Connection to SQLite DB successful!')
    except Error as e:
        print(f'The error {e} occurred.')
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query executed successfully!')
    except Error as e:
        print(f'The error {e} occurred.')

def execute_insert_values_query(connection, query, values):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        print('Query executed successfully!')
    except Error as e:
        print(f'The error {e} occurred.')

def execute_read_query(connection, query):
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f'The error {e} occurred.')

# LDA Model Building Functions

# Preprocessing

def sent_to_words(songs):
    """ (list of str) -> generator object
    Takes list of song lyrics, tokenizes words and cleans up text using Gensim's preprocess
    """
    for song in songs:
        yield(simple_preprocess(str(song), deacc=True))


def remove_stopwords(song):
    """ (str) -> str
    """
    # create stopword list
    stop_words = stopwords.words('english')
    additional_stopwords = ['get', 'got', 'gonna', 'gon', 'feat', 'ft','featuring', 'uh', 'uhh', 'uh-huh', 'huh', "'bout", 'oh', "goin'", "doin'", 'gotta', 'da', 'em', 'like', 'yeah']
    for word in additional_stopwords:
        stop_words.append(word)

    # lowercase, tokenize and deaccent
    word_list = simple_preprocess(song)
    
    return ' '.join([lyric for lyric in word_list if lyric not in stop_words])



def lemmatization(texts, allowed_postags=['NOUN', 'VERB', 'PROPN']):
    nlp = spacy.load("en_core_web_sm")
    texts_out= []
    for song in texts:
        doc = nlp(' '.join(song))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def chunk_song(song, chunk_size):
    """ (str, int) --> list of str
    Splits the full text of the song into chunks of lines. Number of lines per chunk determined by chunk_size
    """
    new_line = r'.+'
    song_split = re.findall(new_line, song)

    chunk = []
    for i in range(0, len(song_split), chunk_size):
        current_set = song_split[i:i+chunk_size]
        concatenated_set = " ".join(current_set)
        chunk.append(concatenated_set)
    
    return chunk

def remove_non_songs(df):
    """
    Remove rows from dataframe that are track lists or other non-songs.
    """
    # Filters
    tracklist_filter = df['song_title'].str.contains('Tracklist')
    album_art_filter = df['song_title'].str.contains('Album Art')
    cover_art_filter = df['song_title'].str.contains('Cover Art')

    # Indices of filtered rows
    non_songs_index = df[tracklist_filter|album_art_filter|cover_art_filter].index.tolist()

    clean_df = df.drop(index=non_songs_index)
    
    return clean_df