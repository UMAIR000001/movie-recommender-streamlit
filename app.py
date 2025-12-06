# app.py

import streamlit as st
import pandas as pd
from config import ALL_GENRES
from recommender import load_data_and_model, get_recommendations
from ui import set_video_background, display_recommendations_featured

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# --- BACKGROUND ---
set_video_background("bg.mp4")

# Initialize session state
if 'recs_df' not in st.session_state:
    st.session_state.recs_df = pd.DataFrame()

# Load Data
df, cosine_sim = load_data_and_model()

# --- SIDEBAR ---
st.sidebar.header("Find Your Next Movie 🍿")

# 1. Similarity Search
st.sidebar.subheader("Search by Movie")
movie_titles = df['title'].tolist()
selected_movie = st.sidebar.selectbox("Choose a movie you like:", movie_titles)

if st.sidebar.button("Recommend Similar"):
    st.session_state.recs_df = get_recommendations(selected_movie, cosine_sim, df)

st.sidebar.markdown("---")

# 2. Genre Search
st.sidebar.subheader("Search by Genre")
selected_genre = st.sidebar.selectbox("Choose a genre:", ALL_GENRES)

if st.sidebar.button("Find by Genre"):
    # FIX: Convert "Science Fiction" -> "sciencefiction" to match our tags
    clean_genre = selected_genre.replace(" ", "").lower()
    
    # Filter movies that have this tag
    genre_recs = df[df['tags'].str.contains(clean_genre, na=False)]
    
    # Pick 10 random movies from that genre
    if not genre_recs.empty:
        # Use min() to avoid error if genre has less than 10 movies
        sample_size = min(len(genre_recs), 10)
        st.session_state.recs_df = genre_recs.sample(n=sample_size)
    else:
        st.sidebar.error("No movies found for this genre.")

# --- MAIN PAGE ---
st.title("🎬 AI Movie Recommender")

if not st.session_state.recs_df.empty:
    display_recommendations_featured(st.session_state.recs_df)
else:
    st.info("👈 Use the sidebar to find movies!")