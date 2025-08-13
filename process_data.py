# process_data.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import sys
import ast # To safely evaluate the string representation of lists/dicts

print("Starting advanced data processing...")

def parse_literal_string(data):
    """Safely parse a string that looks like a Python literal."""
    try:
        return ast.literal_eval(data)
    except (ValueError, SyntaxError):
        return []

# --- 1. DATA LOADING AND PREPROCESSING ---
try:
    movies = pd.read_csv('tmdb_5000_movies.csv')
except FileNotFoundError:
    print("ERROR: The movie dataset file ('tmdb_5000_movies.csv') was not found.")
    print("Please make sure it's in the same folder as this script.")
    sys.exit(1) # Exit the script if file not found

print("Dataset loaded successfully.")

# Parse the 'genres' and 'keywords' columns from string to list
movies['genres'] = movies['genres'].apply(parse_literal_string)
movies['keywords'] = movies['keywords'].apply(parse_literal_string)

# Create a new column with just the genre names
movies['genres_list'] = movies['genres'].apply(lambda x: [i['name'] for i in x])
movies['keywords_list'] = movies['keywords'].apply(lambda x: [i['name'] for i in x])

# Combine overview, genre names, and keyword names into a single 'tags' column
movies['tags'] = movies['overview'].fillna('') + ' ' + \
                 movies['genres_list'].apply(lambda x: ' '.join(x)) + ' ' + \
                 movies['keywords_list'].apply(lambda x: ' '.join(x))

# Create a new, clean dataframe with the columns we need for the app
new_data = movies[['id', 'title', 'tags', 'genres_list', 'vote_average']].copy()
print("Data cleaned and 'tags' and 'genres_list' columns created.")

# --- 2. MODEL BUILDING (TF-IDF & COSINE SIMILARITY) ---
print("Building TF-IDF model for content similarity...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
vectors = vectorizer.fit_transform(new_data['tags']).toarray()

print("Calculating cosine similarity matrix...")
similarity = cosine_similarity(vectors)

# --- 3. SAVING THE PROCESSED DATA ---
# This is much faster than recalculating it every time the app starts.
joblib.dump(new_data, 'movies_data.joblib')
joblib.dump(similarity, 'similarity_matrix.joblib')

print("\nProcessing complete!")
print("Two files were created: 'movies_data.joblib' and 'similarity_matrix.joblib'")
