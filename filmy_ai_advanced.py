import streamlit as st
import pickle
import pandas as pd
import requests
from utils.file_loader import download_and_load_similarity

# Add background image using raw GitHub URL
def add_bg_image():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://raw.githubusercontent.com/Debottam-Ghosh/Filmy-AI-Advanced/main/Dark%20Background%20Image.jpg");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image()


# Load the movie_info DataFrame
movies_info = pickle.load(open('movies_info.pkl', 'rb'))
movies_info = pd.DataFrame(movies_info)

# Load Top_Recommendations and create DataFrame
Top_Recommendations = pickle.load(open('Top_Recommendations.pkl', 'rb'))
Top_Recommendations = pd.DataFrame(Top_Recommendations)

# Download and load the similarity matrix from Google Drive
file_id = '1yyZFiRDEHimsXP8H_WOBpLpTIfSRrVJ-'
similarity = download_and_load_similarity(file_id)

# My OMDb API Key
OMDB_API_KEY_1 = "ab267713"
OMDB_API_KEY_2 = "e8e2e5fc"

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
    "<p style='color:#808080; font-size:35px; font-weight:bold;'>Choose the movie you like</p>",
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


# Function to get poster from OMDb
def get_poster(title):
    # Correct raw GitHub link (ensure it's raw and publicly accessible)
    default_poster = "https://raw.githubusercontent.com/Debottam-Ghosh/Filmy-AI-Advanced/main/Poster%20Unavailable.png"

    url_1 = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY_1}"
    url_2 = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY_2}"
    response_1 = requests.get(url_1)
    response_2 = requests.get(url_2)

    if response_1.status_code == 200:
        data_1 = response_1.json()
        poster_1 = data_1.get('Poster')
        if poster_1 and poster_1 != "N/A":
            return poster_1
    elif response_2.status_code == 200:
        data_2 = response_2.json()
        poster_2 = data_2.get('Poster')
        if poster_2 and poster_2 != "N/A":
            return poster_2
    return default_poster


if st.button("Recommend") and movie_info is not None:
    def recommend(movie):
        if movie not in Top_Recommendations['movie_title'].values:
            print("Movie not found in dataset. Please try another one.")
            return []

        movie_index = Top_Recommendations[Top_Recommendations['movie_title'] == movie].index[0]
        similarity_index = similarity[movie_index]
        recommended_movies_list = sorted(list(enumerate(similarity_index)), reverse=True, key=lambda x: x[1])

        # Filter for movies with the same actor and unique titles
        top_list = []
        seen_titles = set()

        for i in recommended_movies_list:
            idx = i[0]
            movie_title = Top_Recommendations.iloc[idx]['movie_title']

            if (
                idx != movie_index and
                movie_title != movie_info['movie_title'] and
                movie_title not in seen_titles
                ):
                top_list.append(idx)
                seen_titles.add(movie_title)

            if len(top_list) >= 6:
                break

        recommended = []
        for i in top_list:
            movie_title = Top_Recommendations.iloc[i].movie_title
            imdb_link = Top_Recommendations.iloc[i].movie_imdb_link
            poster_url = get_poster(movie_title)
            recommended.append({
                "title": movie_title,
                "link": imdb_link,
                "poster": poster_url
            })
        return recommended


    # Get poster from OMDb
    poster_url = get_poster(selected_movie_name)

    st.markdown("## **:rainbow[Movie Info]**")

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
        st.markdown(f"#### **:red[{movie_info['movie_title']}] ({movie_info['title_year']})**")
        st.markdown(f"**GENRE:**&nbsp;&nbsp; {movie_info['genres']}")
        st.markdown(f"**DIRECTOR:**&nbsp;&nbsp; {movie_info['director_name']}")
        st.markdown(f"**CASTS:**&nbsp;&nbsp; {movie_info['Casts']}")
        st.markdown(f"**IMDB RATING:**&nbsp;&nbsp; {movie_info.get('imdb_score', 'N/A')}")
        st.markdown(f"**RUNTIME:**&nbsp;&nbsp; {movie_info['duration']} min")
        st.markdown(f"**CERTIFICATE:**&nbsp;&nbsp; {movie_info['content_rating']}")
        st.markdown(f"**BOX OFFICE:**&nbsp;&nbsp; $ {movie_info.get('gross', 'N/A')}")

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    st.markdown("# **:rainbow[Top Recommendations For You]**")

    recommendations = recommend(selected_movie_name)

    # Create 5 columns
    cols = st.columns(5)

    # Loop through columns and display each recommended movie
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
                # Add movie title as caption
                st.caption(movie['title'])


    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")


    st.markdown(f"## **:rainbow[Top Recommendations Directed By {movie_info['director_name']}]**")

    def dir_recommend(movie):
        if movie not in Top_Recommendations['movie_title'].values:
            print("Movie not found in dataset. Please try another one.")
            return []

        movie_index = Top_Recommendations[Top_Recommendations['movie_title'] == movie].index[0]

        # Get the selected movie's details
        dir_movie_info = Top_Recommendations.loc[movie_index]

        similarity_index = similarity[movie_index]

        recommended_movies_list = sorted(list(enumerate(similarity_index)), reverse=True, key=lambda x: x[1])

        # Filter for movies with the same director
        dir_top_list = []
        seen_titles = set()

        for i in recommended_movies_list:
            dir_idx = i[0]
            movie_title = Top_Recommendations.iloc[dir_idx]['movie_title']

            if (
                    dir_idx != movie_index and
                    Top_Recommendations.iloc[dir_idx]['director_name'] == dir_movie_info['director_name'] and
                    movie_title != dir_movie_info['movie_title'] and
                    movie_title not in seen_titles
            ):
                dir_top_list.append(dir_idx)
                seen_titles.add(movie_title)
                
            if len(dir_top_list) >= 6:
                break
                
        dir_recommended = []
        for i in dir_top_list:
            movie_title = Top_Recommendations.iloc[i].movie_title
            imdb_link = Top_Recommendations.iloc[i].movie_imdb_link
            poster_url = get_poster(movie_title)
            dir_recommended.append({
                "title": movie_title,
                "link": imdb_link,
                "poster": poster_url
            })
        return dir_recommended


    dir_recommendations = dir_recommend(selected_movie_name)
    
    if not dir_recommendations:
        st.markdown(
            "<p style='color:#A9A9A9; font-size:45px; font-weight:bold;'>No Recommendations From This Director!</p>",
            unsafe_allow_html=True
        )


    # Create 5 columns
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
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    # Get the selected movie's details
    act_movie_info = None
    if selected_movie_name != 'Select a movie...':
        act_filtered = Top_Recommendations[Top_Recommendations['movie_title'] == selected_movie_name]
        if not act_filtered.empty:
            act_movie_info = act_filtered.iloc[0]

            # Replace underscores with spaces in all string values
            act_movie_info = act_movie_info.apply(lambda x: x.replace('_', ' ') if isinstance(x, str) else x)


    st.markdown(f"## **:rainbow[Top Recommendations From the Cast {act_movie_info['actor_1_name']}]**")

    def act_recommend(movie):
        if movie not in Top_Recommendations['movie_title'].values:
            print("Movie not found in dataset. Please try another one.")
            return []

        movie_index = Top_Recommendations[Top_Recommendations['movie_title'] == movie].index[0]

        # Get the selected movie's details
        act_movie_info = Top_Recommendations.loc[movie_index]

        similarity_index = similarity[movie_index]

        recommended_movies_list = sorted(list(enumerate(similarity_index)), reverse=True, key=lambda x: x[1])

        # Filter for movies with the same director
        act_top_list = []
        seen_titles = set()

        for i in recommended_movies_list:
            act_idx = i[0]
            movie_title = Top_Recommendations.iloc[act_idx]['movie_title']

            if (
                    act_idx != movie_index and
                    Top_Recommendations.iloc[act_idx]['actor_1_name'] == act_movie_info['actor_1_name'] and
                    movie_title != act_movie_info['movie_title'] and
                    movie_title not in seen_titles
            ):
                act_top_list.append(act_idx)
                seen_titles.add(movie_title)

            if len(act_top_list) >= 6:
                break

        act_recommended = []
        for i in act_top_list:
            movie_title = Top_Recommendations.iloc[i].movie_title
            imdb_link = Top_Recommendations.iloc[i].movie_imdb_link
            poster_url = get_poster(movie_title)
            act_recommended.append({
                "title": movie_title,
                "link": imdb_link,
                "poster": poster_url
            })
        return act_recommended


    act_recommendations = act_recommend(selected_movie_name)
    
    if not act_recommendations:
        st.markdown(
            "<p style='color:#A9A9A9; font-size:45px; font-weight:bold;'>No Recommendations From This Cast!</p>",
            unsafe_allow_html=True
        )

    # Create 5 columns
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


st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")

st.markdown(
    "<p style='color:#808080; font-size:45px; font-weight:bold;'>Developed by Debottam Ghosh</p>",
    unsafe_allow_html=True
)


