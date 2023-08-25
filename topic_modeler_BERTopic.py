# Data processing
import pandas as pd
import numpy as np

# text processing
import nltk
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('wordnet')
wn = nltk.WordNetLemmatizer()

# dimension reduction
from umap import UMAP

# modeling
from bertopic import BERTopic

# Helper functions
from helper_functions import create_connection, remove_stopwords


# Import data
connection = create_connection('lyrics_nlp.sqlite')
query = 'SELECT * FROM lyrics'
df = pd.read_sql(query, connection, index_col='id')


# Text preprocessing

# Remove stopwords
df['lyrics_no_stopwords'] = df['song_lyrics'].apply(remove_stopwords)


# Lemmatize
df['lyrics_lemmatized'] = df['lyrics_no_stop'].apply(lambda x: ' '.join([wn.lemmatize(w) for w in x.split()]))


# Model Building

# Initiate UMAP
umap_model = UMAP(n_neighbors=15,
                  n_components=5,
                  min_dist=0.0,
                  metric='cosine',
                  random_state=100)

# initiate BERTopic
topic_model = BERTopic(umap_model=umap_model,
                       language='english',
                       calculate_probabilities=True)

topics, probabilities = topic_model.fit_transform(df['lyrics_lemmatized'])

# extract topics
topic_model.get_topic_info()