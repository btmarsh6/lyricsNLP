import re
import sqlite3
from sqlite3 import Error
import string

def remove_punc(text):
    text_list = [char for char in text if not char in string.punctuation]
    return ''.join(text_list)

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
    recommender = r'You might also like$'
    

    expressions = [first_line, square_bracket_labels, curly_bracket_labels, repeats, embed_tag, recommender]
    for expression in expressions:
        lyrics = re.sub(expression, '', lyrics)
    
    # Strip punctuation 
    lyrics = remove_punc(lyrics)
    return lyrics


# Functions to help execute SQL commands

def create_connection(path):
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


def execute_read_query(connection, query):
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f'The error {e} occurred.')

