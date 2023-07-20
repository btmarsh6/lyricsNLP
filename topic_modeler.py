import nltk
import gensim
import pyLDAvis
import nlp
nltk.download('stopwords')
import pandas as pd
import numpy as np
import gensim.corpora as corpora
from gensim.models import CoherenceModel
import pyLDAvis.gensim
import matplotlib.pyplot as plt
%matplotlib inline
from helper_functions import create_connection, sent_to_words, remove_stopwords, lemmatization

# Load data
connection = create_connection('lyrics_nlp.sqlite')
query = 'SELECT * FROM lyrics'
df = pd.read_sql(query, connection, index_col='id')

# Pre-processing
data = df.song_lyrics.values.tolist()

# Tokenize each song into list of individual words
data_words = list(sent_to_words(data))
# Remove stop words
words_no_stop = remove_stopwords(data_words)
# Lemmatize words
words_lemmatized = lemmatization(words_no_stop)
