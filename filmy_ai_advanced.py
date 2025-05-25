import streamlit as st
import pickle
import pandas as pd
import requests
from utils.file_loader import download_and_load_similarity

# Load the movie_info DataFrame with cached poster URLs
movies_info = pickle.load(open('movies_info_with_posters.pkl', 'rb'))
movies_info = pd.DataFrame(movies_info)

# Load Top_Recommendations and create DataFrame
Top_Recommendations = pickle.load(open('Top_Recommendations.pkl', 'rb'))
Top_Recommendations = pd.DataFrame(Top_Recommendations)

# Download and load the similarity matrix from Google Drive
file_id = '1yyZFiRDEHimsXP8H_WOBpLpTIfSRrVJ-'
similarity = download_and_load_similarity(file_id)

# Default poster URL for fallback
DEFAULT_POSTER = "https://raw.githubusercontent.com/Debottam-Ghosh/Filmy-AI-Advanced/main/Poster%20Unavailable.png"

# App title
st.markdown(
    """
    <p style='font-size:75px; font-weight:bold;'>
        <span style='color:#FF0000;'>Filmy</span> <span style='color:#FFFFFF;'>AI</span> <span style='color:#282828;'>PRO</span>
    </p>
    """,
    unsafe_allow_html=True
)

st.write(" ")

st.markdown(
    "<p style='color:#696969; font-size:35px; font-weight:bold;'>Choose the movie you like</p>",
    unsafe_allow_html=True
)

# Dropdown to select movie
selected_movie_name = st.selectbox(
    "",
    ['Select a movie...'] + list(movies_info['movie_title'].unique())
)

# Get the selected movie's details
movie_info = None
if selected_movie_name != 'Select a movie...':
    filtered = movies_info[movies_info['movie_title'] == selected_movie_name]
    if not filtered.empty:
        movie_info = filtered.iloc[0]

# Function to get cached poster URL from movies_info DataFrame
def get_cached_poster(title):
    filtered = movies_info[movies_info['movie_title'] == title]
    if not filtered.empty:
        poster_url = filtered.iloc[0].get('poster_url', DEFAULT_POSTER)
        if poster_url and poster_url != 'N/A':
            return poster_url
    return DEFAULT_POSTER

if st.button("Recommend") and movie_info is not None:

    def recommend(movie):
        if movie not in Top_Recommendations['movie_title'].values:
            st.warning("Movie not found in dataset. Please try another one.")
            return []

        movie_index = Top_Recommendations[Top_Recommendations['movie_title'] == movie].index[0]
        similarity_index = similarity[movie_index]
        recommended_movies_list = sorted(list(enumerate(similarity_index)), reverse=True, key=lambda x: x[1])

        # Filter for movies with unique titles
        top_list = []
        seen_titles = set()

        for i in recommended_movies_list:
            idx = i[0]
            movie_title = Top_Recommendations.iloc[idx]['movie_title']

            if idx != movie_index and movie_title != movie_info['movie_title'] and movie_title not in seen_titles:
                top_list.append(idx)
                seen_titles.add(movie_title)

            if len(top_list) >= 6:
                break

        recommended = []
        for i in top_list:
            movie_title = Top_Recommendations.iloc[i].movie_title
            imdb_link = Top_Recommendations.iloc[i].movie_imdb_link
            poster_url = get_cached_poster(movie_title)
            recommended.append({
                "title": movie_title,
                "link": imdb_link,
                "poster": poster_url
            })
        return recommended

    # Get poster from cached data
    poster_url = get_cached_poster(selected_movie_name)

    # Create two columns: left for poster, right for details
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write(" ")
        if poster_url and poster_url != "N/A":
            st.markdown(
                f"""
                <style>
                    .hover-large {{
                        transition: transform 0.3s ease;
                        width: 250px;
                        height: 375px;
                        object-fit: cover;
                    }}
                    .hover-large:hover {{
                        transform: scale(1.05);
                    }}
                </style>

                <a href="{movie_info['movie_imdb_link']}" target="_blank">
                    <img src="{poster_url}" class="hover-large" />
                </a>
                """,
                unsafe_allow_html=True
            )

    with col2:
        st.markdown(f"### **:red[{movie_info['movie_title']}] ({movie_info['title_year']})**")
        st.markdown(f"**GENRE:**&nbsp;&nbsp; {movie_info['genres']}")
        st.markdown(f"**DIRECTOR:**&nbsp;&nbsp; {movie_info['director_name']}")
        st.markdown(f"**CASTS:**&nbsp;&nbsp; {movie_info['Casts']}")
        st.markdown(f"**IMDB RATING:**&nbsp;&nbsp; {movie_info.get('imdb_score', 'N/A')}")
        st.markdown(f"**RUNTIME:**&nbsp;&nbsp; {movie_info['duration']} min")
        st.markdown(f"**CERTIFICATE:**&nbsp;&nbsp; {movie_info['content_rating']}")
        st.markdown(f"**BOX OFFICE:**&nbsp;&nbsp; $ {movie_info.get('gross', 'N/A')}")

    st.write("\n" * 6)

    st.markdown("# **:red[Top Recommendations For You]**")

    recommendations = recommend(selected_movie_name)

    # Create 5 columns
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            movie = recommendations[idx]
            if movie['poster'] and movie['poster'] != "N/A":
                st.markdown(
                    f"""
                    <style>
                    .hover-img {{
                        transition: transform 0.3s ease;
                        width: 120px;
                        height: 180px;
                        object-fit: cover;
                        display: block;
                    }}
                    .hover-img:hover {{
                        transform: scale(1.05);
                    }}
                    </style>

                    <a href="{movie['link']}" target="_blank">
                        <div class="img-container">
                            <img src="{movie['poster']}" class="hover-img" />
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
                st.caption(movie['title'])

    st.write("\n" * 4)

    st.markdown(f"## **:red[Top Recommendations Directed By {movie_info['director_name']}]**")

    def dir_recommend(movie):
        if movie not in Top_Recommendations['movie_title'].values:
            st.warning("Movie not found in dataset. Please try another one.")
            return []

        movie_index = Top_Recommendations[Top_Recommendations['movie_title'] == movie].index[0]
        dir_movie_info = Top_Recommendations.loc[movie_index]
        similarity_index = similarity[movie_index]
        recommended_movies_list = sorted(list(enumerate(similarity_index)), reverse=True, key=lambda x: x[1])

        dir_top_list = []
        seen_titles = set()

        for i in recommended_movies_list:
            dir_idx = i[0]
            movie_title = Top_Recommendations.iloc[dir_idx]['movie_title']

            if (dir_idx != movie_index and
                Top_Recommendations.iloc[dir_idx]['director_name'] == dir_movie_info['director_name'] and
                movie_title != dir_movie_info['movie_title'] and
                movie_title not in seen_titles):
                dir_top_list.append(dir_idx)
                seen_titles.add(movie_title)

            if len(dir_top_list) >= 6:
                break

        dir_recommended = []
        for i in dir_top_list:
            movie_title = Top_Recommendations.iloc[i].movie_title
            imdb_link = Top_Recommendations.iloc[i].movie_imdb_link
            poster_url = get_cached_poster(movie_title)
            dir_recommended.append({
                "title": movie_title,
                "link": imdb_link,
                "poster": poster_url
            })
        return dir_recommended

    dir_recommendations = dir_recommend(selected_movie_name)

    cols = st.columns(5)

    for col, movie in zip(cols, dir_recommendations):
        with col:
            if movie['poster'] and movie['poster'] != "N/A":
                st.markdown(
                    f"""
                    <style>
                    .hover-img {{
                        transition: transform 0.3s ease;
                        width: 120px;
                        height: 180px;
                        object-fit: cover;
                        display: block;
                    }}
                    .hover-img:hover {{
                        transform: scale(1.05);
                    }}
                    </style>

                    <a href="{movie['link']}" target="_blank">
                        <div class="img-container">
                            <img src="{movie['poster']}" class="hover-img" />
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
            st.caption(movie['title'])
    st.write("\n" * 4)

    # Actor-based recommendations (similar to above)
    act_movie_info = None
    if selected_movie_name != 'Select a movie...':
        act_filtered = Top_Recommendations[Top_Recommendations['movie_title'] == selected_movie_name]
        if not act_filtered.empty:
            act_movie_info = act_filtered.iloc[0]
            act_movie_info = act_movie_info.apply(lambda x: x.replace('_', ' ') if isinstance(x, str) else x)

    if act_movie_info is not None:
        st.markdown(f"## **:red[Top Recommendations From the Actor {act_movie_info['actor_1_name']}]**")

        def act_recommend(movie):
            if movie not in Top_Recommendations['movie_title'].values:
                st.warning("Movie not found in dataset. Please try another one.")
                return []

            movie_index = Top_Recommendations[Top_Recommendations['movie_title'] == movie].index[0]
            act_movie_info = Top_Recommendations.loc[movie_index]
            similarity_index = similarity[movie_index]
            recommended_movies_list = sorted(list(enumerate(similarity_index)), reverse=True, key=lambda x: x[1])

            act_top_list = []
            seen_titles = set()

            for i in recommended_movies_list:
                act_idx = i[0]
                movie_title = Top_Recommendations.iloc[act_idx]['movie_title']

                if (act_idx != movie_index and
                    Top_Recommendations.iloc[act_idx]['actor_1_name'] == act_movie_info['actor_1_name'] and
                    movie_title != act_movie_info['movie_title'] and
                    movie_title not in seen_titles):
                    act_top_list.append(act_idx)
                    seen_titles.add(movie_title)

                if len(act_top_list) >= 6:
                    break

            act_recommended = []
            for i in act_top_list:
                movie_title = Top_Recommendations.iloc[i].movie_title
                imdb_link = Top_Recommendations.iloc[i].movie_imdb_link
                poster_url = get_cached_poster(movie_title)
                act_recommended.append({
                    "title": movie_title,
                    "link": imdb_link,
                    "poster": poster_url
                })
            return act_recommended

        act_recommendations = act_recommend(selected_movie_name)

        cols = st.columns(5)

        for col, movie in zip(cols, act_recommendations):
            with col:
                if movie['poster'] and movie['poster'] != "N/A":
                    st.markdown(
                        f"""
                        <style>
                        .hover-img {{
                            transition: transform 0.3s ease;
                            width: 120px;
                            height: 180px;
                            object-fit: cover;
                            display: block;
                        }}
                        .hover-img:hover {{
                            transform: scale(1.05);
                        }}
                        </style>

                        <a href="{movie['link']}" target="_blank">
                            <div class="img-container">
                                <img src="{movie['poster']}" class="hover-img" />
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
                st.caption(movie['title'])
