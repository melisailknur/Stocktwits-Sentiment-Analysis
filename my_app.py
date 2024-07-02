# -*- coding: utf-8 -*-
"""my_app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ggM2o1ccskT1v_LGJYm1LwSmd29ykx9I
"""

import pandas as pd
import re
import nltk
import emoji
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import roc_auc_score, roc_curve, auc
import tensorflow as tf
import tensorflow_text as text
# import tensorflow_hub as hub
#from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import streamlit as st
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import numpy as np
import joblib

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

# Initialize the WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

custom_stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
'from', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
's', 't', 'can', 'will', 'just', 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y'])

# Function to add spaces around emojis
def extract_emojis(s):
    return ''.join((' ' + c + ' ') if c in emoji.EMOJI_DATA else c for c in s)

# Pre-processing function
def preprocess_text(text, custom_stopwords):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'\$\w+', '', text)
    text = re.sub(r'rt\s+', '', text)
    text = extract_emojis(text)
    text = emoji.demojize(text)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    words = word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags if word not in custom_stopwords]
    return ' '.join(lemmatized_words)

# Charger le modèle RNN
model_rnn = load_model('./rnn_model_3_1.h5')

# Définir les paramètres de tokenisation
maxlen = 150
tokenizer = joblib.load('./rnn3_tokenizer.pickle')

# Fonction pour prédire le sentiment
def predict_sentiment(tweet):
    # Prétraiter le tweet
    tweet_seq = tokenizer.texts_to_sequences([tweet])
    tweet_pad = pad_sequences(tweet_seq, maxlen=maxlen)
    # Prédire le sentiment
    pred_prob = model_rnn.predict(tweet_pad).ravel()[0]
    return 'Bullish' if pred_prob > 0.6 else 'Bearish'

# Interface Streamlit
st.title('Sentiment Analysis for Stock Tweets')
st.write('Enter a tweet with a stock tag like §AAPL and click on Predict to see the sentiment.')

# Entrée de l'utilisateur
tweet = st.text_area('Enter tweet:')

# Bouton de prédiction
if st.button('Predict'):
    if tweet:
        if len(tweet) > 300:
            st.write('Please enter a shorter tweet.')
        else:
            tweet = preprocess_text(tweet, custom_stopwords)
            sentiment = predict_sentiment(tweet)
            st.write(f'The predicted sentiment is: **{sentiment}**')
    else:
        st.write('Please enter a tweet to predict.')
