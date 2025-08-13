# app.py

import streamlit as st
import joblib
import random
# Import all our UI functions from the other file
from ui_components import (
    render_header,
    render_hero_section,
    display_recommendations_slider,
    render_footer,
    display_movie_grid,
    render_placeholder_page
)

# --- INITIALIZE SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# --- LOAD PRE-PROCESSED DATA AND STYLES ---
try:
    movies = joblib.load('movies_data.joblib')
    similarity = joblib.load('similarity_matrix.joblib')
except FileNotFoundError:
    st.error("Model files not found. Please run `process_data.py` first.")
    st.stop()

# Load custom CSS from the style.css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- STREAMLIT APP INTERFACE ---
st.set_page_config(layout="wide")

# Render the header. The buttons in the header will update st.session_state.page
render_header()

# --- PAGE ROUTING ---

# HOME PAGE
if st.session_state.page == 'Home':
    hero_movie = movies.sort_values('vote_average', ascending=False).iloc[random.randint(0, 100)]
    render_hero_section(hero_movie)

    st.title('🎬 Movie Recommender')
    st.write("Discover your next favorite film. Get personalized recommendations or explore top movies by genre.")
    st.divider()

    mode = st.radio(
        "Select Recommendation Mode:",
        ('Recommend by Movie Title', 'Discover by Genre'),
        horizontal=True, key='mode_selection'
    )

    if mode == 'Recommend by Movie Title':
        st.header("Find Movies Similar to...")
        movie_title_input = st.text_input("Type a movie title you like:", "Inception", key="movie_input")
        if st.button("Get Recommendations", key="rec_button"):
            with st.spinner('Finding similar movies...'):
                try:
                    movie_index = movies[movies['title'] == movie_title_input].index[0]
                    distances = similarity[movie_index]
                    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
                    rec_titles = [movies.iloc[i[0]].title for i in movies_list]
                    display_recommendations_slider("Similar to your choice:", rec_titles)
                except IndexError:
                    st.error(f"Movie '{movie_title_input}' not found in our dataset.")

    elif mode == 'Discover by Genre':
        st.header("Discover Top-Rated Movies by Genre")
        all_genres = sorted(list(set(sum(movies['genres_list'], []))))
        selected_genres = st.multiselect("Select one or more genres:", all_genres, key="genre_select")
        if st.button("Find Top Movies", key="genre_button"):
            if not selected_genres:
                st.warning("Please select at least one genre.")
            else:
                with st.spinner(f"Searching for top movies..."):
                    genre_movies = movies[movies['genres_list'].apply(lambda x: all(g in x for g in selected_genres))]
                    top_genre_movies = genre_movies.sort_values('vote_average', ascending=False).head(10)
                    rec_titles = top_genre_movies['title'].tolist()
                    display_recommendations_slider(f"Top Rated in {', '.join(selected_genres)}", rec_titles)

# MOVIES PAGE
elif st.session_state.page == 'Movies':
    st.title("Explore All Movies")
    st.write("Browse our extensive collection of films.")
    popular_movies = movies.sort_values('vote_average', ascending=False).head(20)
    display_movie_grid("Top Rated Movies", popular_movies['title'].tolist())

# TV SHOWS PAGE
elif st.session_state.page == 'TV Shows':
    render_placeholder_page("📺 TV Shows", "Our collection of TV shows is coming soon. Stay tuned!")

# MY LIST PAGE
elif st.session_state.page == 'My List':
    render_placeholder_page("❤️ My List", "This feature is coming soon! You'll be able to save your favorite movies here.")

# Render the footer at the bottom of every page
render_footer()
