# -*- coding: utf-8 -*-
"""my_app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ggM2o1ccskT1v_LGJYm1LwSmd29ykx9I
"""

import pandas as pd
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

# Charger le modèle CNN
model_rnn = load_model('./rnn_model3.h5')

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
    return 'Bullish' if pred_prob > 0.5 else 'Bearish'

# Interface Streamlit
st.title('Sentiment Analysis for Stock Tweets')
st.write('Enter a tweet with a stock tag like §AAPL and click on Predict to see the sentiment.')

# Entrée de l'utilisateur
tweet = st.text_area('Enter tweet:')

# Bouton de prédiction
if st.button('Predict'):
    if tweet:
        if len(tweet) > 300:
            st.write('Tweet cannot exceed 300 characters. Please enter a shorter tweet.')
        else:
            sentiment = predict_sentiment(tweet)
            st.write(f'The predicted sentiment is: **{sentiment}**')
    else:
        st.write('Please enter a tweet to predict.')
