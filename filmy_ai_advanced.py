import streamlit as st
import pickle
import pandas as pd
import requests

# Load the movie_info DataFrame
movies_info = pickle.load(open('movies_info.pkl', 'rb'))
movies_info = pd.DataFrame(movies_info)

# Load Top_Recommendations and create DataFrame
Top_Recommendations = pickle.load(open('Top_Recommendations.pkl', 'rb'))
Top_Recommendations = pd.DataFrame(Top_Recommendations)

# Load Similarity and create DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))
similarity = pd.DataFrame(similarity)

# My OMDb API Key
OMDB_API_KEY = "e8e2e5fc"

# App title
st.title(":red[Filmy] AI")

# Dropdown to select movie
selected_movie_name = st.selectbox("**Choose the movie you like**", movies_info['Series_Title'].unique())

# Get the selected movie's details
movie_info = movies_info[movies_info['Series_Title'] == selected_movie_name].iloc[0]

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
    poster_url = get_poster(selected_movie_name)

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

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    st.title(":red[Top Recommendations For You]")


    def recommend(movie):
        if movie not in Top_Recommendations['Series_Title'].values:
            print("Movie not found in dataset. Please try another one.")
            return []

        movie_index = Top_Recommendations[Top_Recommendations['Series_Title'] == movie].index[0]
        similarity_index = similarity[movie_index]
        recommended_movies_list = sorted(list(enumerate(similarity_index)), reverse=True, key=lambda x: x[1])[1:6]

        recommended = [Top_Recommendations.iloc[i[0]].Series_Title for i in recommended_movies_list]
        return recommended


    recommendations = recommend(selected_movie_name)

    # Create 5 columns
    cols = st.columns(5)

    # Display posters and movie titles
    for i in range(5):
        with cols[i]:
            try:
                poster_url = get_poster(recommendations[i])
                if poster_url and poster_url != "N/A":
                    st.markdown(
                        f"""
                        <div style="border: 2pt solid white; display: inline-block; width: 120px; height: 180px; overflow: hidden;">
                            <img src="{poster_url}" style="width: 100%; height: 100%; object-fit: cover;" />
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.caption(recommendations[i])  
                else:
                    st.warning("Poster not available.")
            except IndexError:
                st.warning("Less than 5 recommendations available.")
