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

from helper_functions import create_connection, sent_to_words, remove_stopwords, lemmatization
from pprint import pprint

# Load data
connection = create_connection('lyrics_nlp.sqlite')
query = 'SELECT * FROM lyrics'
df = pd.read_sql(query, connection, index_col='id')

# Pre-processing
print("Preparing lyrics data...")
data = df.song_lyrics.values.tolist()

# Tokenize each song into list of individual words
data_words = list(sent_to_words(data))
# Remove stop words
data_no_stop = remove_stopwords(data_words)
# Lemmatize words
data_lemmatized = lemmatization(data_no_stop)

# Build LDA Model

# start with creating a dictionary
id2word = corpora.Dictionary(data_lemmatized)

# create corpus
texts = data_lemmatized

# term document frequency
corpus = [id2word.doc2bow(text) for text in texts]

# Baseline model
print("Training Model...")
baseline = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                          id2word=id2word,
                                          num_topics=10,
                                          random_state=100,
                                          chunksize=200,
                                          passes=10,
                                          per_word_topics=True)

pprint(baseline.print_topics())

# some error is occuring here

doc_lda = baseline[corpus]

# How good a given model is shown through topic coherence
coherence_model_lda = CoherenceModel(model=baseline, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherenceScore: ', coherence_lda)