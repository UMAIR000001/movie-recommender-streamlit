# recommender.py

import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import API_KEY, PLACEHOLDER_IMAGE_URL

@st.cache_resource
def load_data_and_model():
    """Loads the dataset, trains the model, and returns them."""
    # Load data
    df = pd.read_csv('cleaned_movies_with_details.csv')
    
    # Create TF-IDF Matrix
    # We use .astype('U') to ensure all tags are treated as Unicode strings
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['tags'].values.astype('U'))
    
    # Calculate Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    return df, cosine_sim

def get_recommendations(title, cosine_sim_matrix, dataframe, num_recommendations=10):
    """Gets similarity-based movie recommendations."""
    try:
        # Find index of the movie
        idx = dataframe.index[dataframe['title'] == title][0]
        
        # Get scores
        sim_scores = list(enumerate(cosine_sim_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Skip the first one (it is the movie itself)
        sim_scores = sim_scores[1:num_recommendations+1]
        
        # Get indices
        movie_indices = [i[0] for i in sim_scores]
        
        return dataframe.iloc[movie_indices]
    except IndexError:
        return pd.DataFrame() # Return empty if fails

def fetch_poster(movie_id):
    """
    Fetches a movie poster URL from the TMDb API using Movie ID.
    Using ID is much faster and more accurate than Title.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except:
        pass
    return PLACEHOLDER_IMAGE_URL