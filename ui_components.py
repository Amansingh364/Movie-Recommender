# ui_components.py

import streamlit as st
import requests

def fetch_poster(movie_title, quality='high'):
    """Fetches a movie poster from the OMDb API."""
    # ===================================================================
    # !!! IMPORTANT !!!
    # REPLACE "YOUR_API_KEY" WITH THE KEY YOU GOT FROM OMDBAPI.COM
    # The app will not work without a valid API key.
    api_key = "7009884c"
    # ===================================================================
    
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('Response') == 'True':
            poster_url = data.get('Poster', 'https://via.placeholder.com/500x750.png?text=No+Poster')
            if quality == 'high':
                return poster_url.replace('SX300', 'SX700')
            return poster_url
        else:
            return 'https://via.placeholder.com/500x750.png?text=Not+Found'
    except requests.exceptions.RequestException:
        return 'https://via.placeholder.com/500x750.png?text=API+Error'

def render_header():
    """Renders the top navigation header with functional buttons."""
    st.markdown("""
    <div class="header">
        <div class="logo">MovieRecs</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])
    with col2:
        if st.button("Home", key="nav_home", use_container_width=True):
            st.session_state.page = 'Home'
    with col3:
        if st.button("Movies", key="nav_movies", use_container_width=True):
            st.session_state.page = 'Movies'
    with col4:
        if st.button("TV Shows", key="nav_tv", use_container_width=True):
            st.session_state.page = 'TV Shows'
    with col5:
        if st.button("My List", key="nav_list", use_container_width=True):
            st.session_state.page = 'My List'


def render_hero_section(movie):
    """Renders the top hero section with a featured movie."""
    poster_url = fetch_poster(movie['title'], quality='high')
    st.markdown(f"""
    <div class="hero-section" style="background-image: linear-gradient(to right, rgba(3, 7, 18, 0.9) 0%, rgba(3, 7, 18, 0.1) 100%), url('{poster_url}');">
        <div class="hero-text">
            <h1>{movie['title']}</h1>
            <p>Today's Featured Movie</p>
            <div class="hero-buttons">
                <button class="hero-btn-watch">▶ WATCH NOW</button>
                <button class="hero-btn-list">+ PLAYLIST</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_recommendations_slider(subheader_text, titles):
    """Displays a list of movies in a horizontal slider."""
    if not titles:
        st.warning("No recommendations found.")
        return
    
    st.subheader(subheader_text)
    
    movie_cards_html = "".join([
        f"""
        <div class="movie-card">
            <img src="{fetch_poster(title, quality='low')}" class="movie-poster">
            <p class="movie-title">{title}</p>
        </div>
        """ for title in titles
    ])
        
    st.markdown(f'<div class="slider-container"><div class="slider-content">{movie_cards_html}</div></div>', unsafe_allow_html=True)

def display_movie_grid(subheader_text, titles):
    """Displays a grid of movies."""
    st.subheader(subheader_text)
    cols = st.columns(5)
    for i, title in enumerate(titles):
        with cols[i % 5]:
            st.markdown(f"""
            <div class="movie-card-grid">
                <img src="{fetch_poster(title, quality='low')}" class="movie-poster-grid">
                <p class="movie-title-grid">{title}</p>
            </div>
            """, unsafe_allow_html=True)

def render_placeholder_page(title, message):
    """Renders a placeholder page for sections that are not yet built."""
    st.title(title)
    st.markdown(f"<div class='placeholder-text'>{message}</div>", unsafe_allow_html=True)
    st.divider()
    
def render_footer():
    """Renders the footer section at the bottom of the page."""
    st.markdown("""
    <div class="footer">
        <p>Built with ❤️ using Streamlit & Python | Coded by a Gemini User</p>
        <p><a href="#">GitHub</a> | <a href="#">About</a> | <a href="#">Contact</a></p>
    </div>
    """, unsafe_allow_html=True)
