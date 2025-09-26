import streamlit as st
import pandas as pd
import pickle
import json
import requests

# Load the movies dataset
movies_df = pd.read_csv("movies.csv")

# Load precomputed similarity matrix and movies_data
with open("cosine_sim.pkl", "rb") as f:
    cosine_sim = pickle.load(f)

with open("movies_data.pkl", "rb") as f:
    movies_data = pickle.load(f)

# Load API config
with open("config.json") as f:
    config = json.load(f)
OMDB_API_KEY = config['OMDB_API_KEY']

# Helper function to fetch movie poster
def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Poster") and data["Poster"] != "N/A":
        return data["Poster"]
    else:
        return None

# Recommendation function
def recommend_movies(title, top_n=5):
    if title not in movies_data['title'].values:
        return [], []
    
    idx = movies_data[movies_data['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    
    movie_titles = [movies_data.iloc[i[0]]['title'] for i in sim_scores]
    posters = [fetch_poster(title) for title in movie_titles]
    
    return movie_titles, posters

# Streamlit app
st.set_page_config(page_title="Movie Recommender System", page_icon="🎬")
st.title("🎬 Movie Recommendation System")
st.sidebar.header("About")
st.sidebar.write("""
**Developer:** Mirza Yasir Abdullah Baig  
**LinkedIn:** [link](https://www.linkedin.com/in/mirza-yasir-abdullah-baig/)  
**GitHub:** [link](https://github.com/mirzayasirabdullahbaig07)  
**Kaggle:** [link](https://www.kaggle.com/code/mirzayasirabdullah07)
""")

# Movie selection
movie_list = movies_data['title'].values
selected_movie = st.selectbox("Select a movie you like:", movie_list)

# Recommend button
if st.button("Recommend"):
    recommended_titles, recommended_posters = recommend_movies(selected_movie)
    
    if recommended_titles:
        st.subheader("Recommended Movies:")
        cols = st.columns(len(recommended_titles))
        for i, col in enumerate(cols):
            col.image(recommended_posters[i], use_container_width=True)
            col.caption(recommended_titles[i])
    else:
        st.write("Sorry, movie not found or no recommendations available.")
