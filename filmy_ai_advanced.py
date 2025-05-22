import streamlit as st
import pickle
import pandas as pd
import requests

# Load the movie info DataFrame
movies_info = pickle.load(open('movies_info.pkl', 'rb'))
movies_info = pd.DataFrame(movies_info)

# Your OMDb API Key
OMDB_API_KEY = "e8e2e5fc"  # 🔐 Replace this with your actual API key

# App title
st.title("🎬 Movie Info Explorer")

# Dropdown to select movie
selected_movie = st.selectbox("**Choose the movie you like**", movies_info['Series_Title'].unique())

# Get the selected movie's details
movie_info = movies_info[movies_info['Series_Title'] == selected_movie].iloc[0]

# Function to get poster from OMDb
def get_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('Poster')  # Returns None if poster not available
    return None

if st.button("Recommend"):
    # Get poster from OMDb
    poster_url = get_poster(selected_movie)

    # Create two columns: left for poster, right for details
    col1, col2 = st.columns([1, 2])

    with col1:
        if poster_url and poster_url != "N/A":
            st.markdown(
                f"""
                <div style="border: 2pt solid white; display: inline-block;">
                    <img src="{poster_url}" width="200" />
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Poster not available.")

    with col2:
        st.markdown(f"## :red[**{movie_info['Series_Title']}**]")
        st.markdown(f"**GENRE:**&nbsp;&nbsp; {movie_info['Genre']}")
        st.markdown(f"**DIRECTOR:**&nbsp;&nbsp; {movie_info['Director']}")
        st.markdown(f"**CASTS:**&nbsp;&nbsp; {movie_info['Casts']}")
        st.markdown(f"**IMDB RATING:**&nbsp;&nbsp; {movie_info.get('IMDB_Rating', 'N/A')}")
        st.markdown(f"**RUNTIME:**&nbsp;&nbsp; {movie_info['Runtime']}")
        st.markdown(f"**RELEASED YEAR:**&nbsp;&nbsp; {movie_info.get('Released_Year', 'N/A')}")
