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
    

    expressions = [first_line, square_bracket_labels, curly_bracket_labels, repeats, embed_tag, recommender]
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

def remove_stopwords(data_words):
    """ (list of list of str) -> list of list of str
    """
    stop_words = stopwords.words('english')
    return[[word for word in song if word not in stop_words] for song in data_words]


def lemmatization(texts, allowed_postags=['NOUN', 'VERB', 'PROPN']):
    nlp = spacy.load("en_core_web_sm")
    texts_out= []
    for song in texts:
        doc = nlp(' '.join(song))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out