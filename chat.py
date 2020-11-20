from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import pickle
import numpy as np
import re

def load_replies():
    f = open("replies.txt", "r")
    replies = f.read().splitlines()
    f.close()
    return replies

def load_vectorized_inputs():
    return sparse.load_npz("vectorized_inputs.npz")

def clean_text(text):
    text = text[1:-1]
    pattern = r'\\'
    return re.sub(pattern, '', text, re.I)

def preprocess(text):
    pattern = r'[Ii]saac:|[Bb]ot [Rr]eply:'
    return re.sub(pattern, '', text, re.I).strip()

def predict_response(text):
    tfidf_vectorizer = pickle.load(open("vectorizer.pk", "rb"))
    vector = tfidf_vectorizer.transform([preprocess(text)])
    X = load_vectorized_inputs()
    index = np.argmax(cosine_similarity(vector, X))
    replies = load_replies()
    reply = replies[index]
    reply = clean_text(reply)
    return reply