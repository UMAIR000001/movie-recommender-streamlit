# ui.py

import streamlit as st
import pandas as pd
import ast
import base64
from recommender import fetch_poster

def set_video_background(video_file):
    """Sets a local video as the background."""
    try:
        with open(video_file, "rb") as f:
            video_bytes = f.read()
        
        video_b64 = base64.b64encode(video_bytes).decode()
        
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: transparent;
            }}
            #my-video {{
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%; 
                min-height: 100%;
                z-index: -1;
            }}
            .content-overlay {{
                background-color: rgba(0,0,0,0.7);
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                z-index: -1;
            }}
            /* Make text on cards readable */
            .stCaption {{
                color: #e0e0e0 !important;
                font-size: 14px;
            }}
            </style>
            
            <video autoplay loop muted id="my-video">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            <div class="content-overlay"></div>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"Video file '{video_file}' not found.")

def display_recommendations_featured(recs_df):
    """Displays recommendations with one featured movie and a detailed grid."""
    if recs_df.empty:
        st.warning("No recommendations found.")
        return

    # --- FEATURED RECOMMENDATION (Top 1) ---
    featured = recs_df.iloc[0]
    poster_url = fetch_poster(featured['movie_id'])

    st.markdown("### 🔥 Top Recommendation")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(poster_url, use_container_width=True)
    with col2:
        st.markdown(f"## {featured['title']}")
        
        # Parse Genres safely
        try:
            if isinstance(featured['genres'], str):
                genres_list = ast.literal_eval(featured['genres'])
            else:
                genres_list = featured['genres']
            st.markdown(f"**Genres:** *{', '.join(genres_list)}*")
        except:
            pass
            
        # Full Overview for the top movie
        st.write(featured['overview'])

    # --- GRID OF OTHER RECOMMENDATIONS (Next 9) ---
    other_recs = recs_df.iloc[1:]
    if not other_recs.empty:
        st.markdown("---")
        st.subheader("More Suggestions")
        
        num_columns = 4
        cols = st.columns(num_columns)
        
        for i, (index, row) in enumerate(other_recs.iterrows()):
            with cols[i % num_columns]:
                st.image(fetch_poster(row['movie_id']), use_container_width=True)
                st.markdown(f"**{row['title']}**")
                
                # --- NEW CODE STARTS HERE ---
                # Check if overview exists
                if pd.notna(row['overview']):
                    text = row['overview']
                    # Truncate if it's too long (over 100 chars) to keep the grid neat
                    if len(text) > 100:
                        text = text[:100] + "..."
                    
                    # Display it in small gray text
                    st.caption(text)
                # --- NEW CODE ENDS HERE ---