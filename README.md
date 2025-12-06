# 🎬 AI Movie Recommender System

A Content-Based Movie Recommendation System built with **Python** and **Streamlit**. 
This application suggests movies based on similarity using the **TMDB 5000 Dataset**. It features a modern, Netflix-style user interface with a video background and real-time movie poster fetching.

## 🚀 Features
* **Content-Based Filtering:** Uses Cosine Similarity and TF-IDF/CountVectorizer to find movies with similar plots, genres, and keywords.
* **Search by Movie:** Select a movie you like, and the AI will recommend 10 similar titles.
* **Discover by Genre:** Filter movies by specific genres (Action, Sci-Fi, Romance, etc.).
* **Interactive UI:** Dynamic video background with a glass-morphism effect.
* **Real-Time Data:** Fetches official movie posters and details using the TMDB API.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **Machine Learning:** Scikit-Learn (Cosine Similarity, TfidfVectorizer)
* **Data Processing:** Pandas, NumPy
* **API:** The Movie Database (TMDB) API

## 📂 Project Structure
```text
├── app.py                   # Main Streamlit application entry point
├── recommender.py           # ML Logic (Vectorization & Similarity)
├── ui.py                    # UI Components (Backgrounds, CSS, Layouts)
├── config.py                # Configuration & API Keys
├── notebooks/               
│   └── data_cleaning.ipynb  # Jupyter Notebook used to preprocess the raw data
├── requirements.txt         # List of dependencies
└── cleaned_movies_with_details.csv # Processed Dataset