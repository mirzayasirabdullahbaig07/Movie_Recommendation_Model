import json
import streamlit as st
from recommend import df, recommend_movies
from omdb_utils import get_movie_details

# ----------------------------
# Load config
# ----------------------------
with open("config.json") as f:
    config = json.load(f)

OMDB_API_KEY = config["OMDB_API_KEY"]

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.title("🎬 About this App")
st.sidebar.info(
    """
This Movie Recommender app suggests similar movies based on your selection.
It uses **TF-IDF vectorization** and **cosine similarity** for recommendations.
"""
)

st.sidebar.title("👤 About Me")
st.sidebar.markdown("""
**Mirza Yasir Abdullah Baig**  
- [LinkedIn](https://www.linkedin.com/in/mirza-yasir-abdullah-baig/)  
- [GitHub](https://github.com/mirzayasirabdullahbaig07)  
- [Kaggle](https://www.kaggle.com/code/mirzayasirabdullah07)  
""")

# ----------------------------
# Main content
# ----------------------------
st.title("🎬 Movie Recommender")

# Movie selection
movie_list = sorted(df['title'].dropna().unique())
selected_movie = st.selectbox("🎬 Select a movie:", movie_list)

if st.button("🚀 Recommend Similar Movies"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        if recommendations is None or recommendations.empty:
            st.warning("Sorry, no recommendations found.")
        else:
            st.success("Top similar movies:")
            for _, row in recommendations.iterrows():
                movie_title = row['title']
                plot, poster = get_movie_details(movie_title, OMDB_API_KEY)

                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A":
                            st.image(poster, width=100)
                        else:
                            st.write("❌ No Poster Found")
                    with col2:
                        st.markdown(f"### {movie_title}")
                        st.markdown(f"*{plot}*" if plot != "N/A" else "_Plot not available_")
