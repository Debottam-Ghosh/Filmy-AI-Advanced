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
            background-image: url("https://raw.githubusercontent.com/Debottam-Ghosh/Filmy-AI-Advanced/main/Movie%20Poster%20Dark.jpg");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


add_bg_image()


st.markdown("""
    <script>
        function toggleMobileWarning() {
            const warningId = "mobile-warning";
            const isMobile = window.innerWidth < 768;
            const existing = document.getElementById(warningId);

            // If mobile and warning not shown
            if (isMobile && !existing && !sessionStorage.getItem('dismissMobileWarning')) {
                const warning = document.createElement('div');
                warning.id = warningId;
                warning.innerHTML = `
                    <div style="background-color: #ff4d4d; color: white; padding: 10px 20px; border-radius: 5px;
                                font-weight: bold; text-align: center; margin-bottom: 20px; position: relative;">
                        ⚠️ This app is best viewed on a desktop device.
                        <br>Please enable 'Desktop Site' on your browser for the best experience.
                        <span style="position:absolute; top:5px; right:10px; cursor:pointer;" onclick="dismissMobileWarning()">❌</span>
                    </div>
                `;
                const mainContainer = window.parent.document.querySelector('.main');
                if (mainContainer) {
                    mainContainer.insertBefore(warning, mainContainer.firstChild);
                }
            } 
            // If not mobile or dismissed
            else if ((!isMobile || sessionStorage.getItem('dismissMobileWarning')) && existing) {
                existing.remove();
            }
        }

        function dismissMobileWarning() {
            sessionStorage.setItem('dismissMobileWarning', 'true');
            const warning = document.getElementById('mobile-warning');
            if (warning) {
                warning.remove();
            }
        }

        window.addEventListener('load', toggleMobileWarning);
        window.addEventListener('resize', toggleMobileWarning);
    </script>
""", unsafe_allow_html=True)



# Load the movie_info DataFrame
movies_info = pickle.load(open('movies_info.pkl', 'rb'))
movies_info = pd.DataFrame(movies_info)

# Load Top_Recommendations and create DataFrame
Top_Recommendations = pickle.load(open('Top_Recommendations.pkl', 'rb'))
Top_Recommendations = pd.DataFrame(Top_Recommendations)

# Download and load the similarity matrix from Google Drive
file_id = '1Jn2XUw592l2RF_wvbRqVFzbq0X1KEit7'
similarity = download_and_load_similarity(file_id)

# Load the genres_info DataFrame
genres_info = pickle.load(open('genres_info.pkl', 'rb'))
genres_info = pd.DataFrame(genres_info)

# Load the cast_info DataFrame
cast_info = pickle.load(open('cast_info.pkl', 'rb'))
cast_info = pd.DataFrame(cast_info)

# My OMDb API Key
OMDB_API_KEY_1 = "ab267713"
OMDB_API_KEY_2 = "e8e2e5fc"


# Function to get poster from OMDb
def get_poster(title):
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


# Function to get some more data from OMDb
def get_awards(title):
    url_1 = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY_1}"
    url_2 = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY_2}"
    response_1 = requests.get(url_1)
    response_2 = requests.get(url_2)

    if response_1.status_code == 200:
        data_1 = response_1.json()
        awards_1 = data_1.get('Awards')
        if awards_1 and awards_1 != "N/A":
            return awards_1
    elif response_2.status_code == 200:
        data_2 = response_2.json()
        awards_2 = data_2.get('Awards')
        if awards_2 and awards_2 != "N/A":
            return awards_2
    return "Got no awards or nominations!"


# App title
st.markdown(
    """
    <div style='text-align: center;'>
        <p style='font-size:75px; font-weight:bold; margin-bottom: 0;'>
            <span style='color:#00fff0;'>Filmy</span> 
            <span style='color:#00fff0;'>AI</span> 
            <span style='color:#00fff0;'>PRO</span>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(" ")

st.markdown("""
    <style>
        div.stButton > button {
            font-size: 35px !important;
            font-weight: bold !important;
            padding: 12px 30px !important;
            border-radius: 12px !important;
            background-color: #013b37;
            color: white;
            border: none;
            margin: 5px;
        }
        div.stButton > button:hover {
            background-color: #00FFF0;
            color: black;
            border: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <h2 style='text-align: center;'>
        Search By Your Favorite</span>
    </h2>
    """,
    unsafe_allow_html=True
)




col1, col2, col3, col4 = st.columns((1.3,4,4,4))

# Initialize mode if not set
if 'mode' not in st.session_state:
    st.session_state.mode = None

with col2:
    if st.button("MOVIE"):
        st.session_state.mode = 'movie'

with col3:
    if st.button("GENRE"):
        st.session_state.mode = 'genre'

with col4:
    if st.button("ACTOR"):
        st.session_state.mode = 'actor'

#st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.mode == 'movie':

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    # Dropdown to select movie
    st.markdown(
        """
        <style>
        /* Target the selectbox text */
        div[data-baseweb="select"] > div {
            background-color: #1f2937; /* background */
            color: #FFFFFF;            /* text color */
            border-radius: 8px;
            padding: 4px 4px;
            font-size: 14px;
        }

        /* Selected option styling */
        div[data-baseweb="select"] span {
            color: #69fff6 !important; /* override Streamlit default */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # The selectbox itself
    selected_movie_name = st.selectbox(
        "",
        ['Select a Movie...'] + list(movies_info['movie_title'].unique())
    )


    # Get the selected movie's details
    movie_info = None
    if selected_movie_name != 'Select a Movie...':
        filtered = movies_info[movies_info['movie_title'] == selected_movie_name]
        if not filtered.empty:
            movie_info = filtered.iloc[0]

    if st.button("Recommend") and movie_info is not None:

        @st.cache_data(show_spinner=False)
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

        st.markdown("# **:rainbow[Movie Info]**")

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
            st.markdown(f"""
            <h3 style='font-weight:bold;'>
                <span style='color:#00FFF0;'>{movie_info['movie_title']}</span> 
                <span style='color:white;'>({movie_info['title_year']})</span>
            </h3>
            """, unsafe_allow_html=True)
            st.markdown(f"**GENRE:**&nbsp;&nbsp; {movie_info['genres']}")
            st.markdown(f"**DIRECTOR:**&nbsp;&nbsp; {movie_info['director_name']}")
            st.markdown(f"**CASTS:**&nbsp;&nbsp; {movie_info['Casts']}")
            st.markdown(f"**IMDb RATING:**&nbsp;&nbsp; {movie_info.get('imdb_score', 'N/A')}")
            st.markdown(f"**RUNTIME:**&nbsp;&nbsp; {movie_info['duration']} min")
            st.markdown(f"**CERTIFICATE:**&nbsp;&nbsp; {movie_info['content_rating']}")
            st.markdown(f"**BOX OFFICE:**&nbsp;&nbsp; $ {movie_info.get('gross', 'N/A')}")
            st.markdown(f"**AWARDS:**&nbsp;&nbsp; {get_awards(movie_info['movie_title'])}")

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

        st.markdown("# **:rainbow[Films You May Like]**")

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
                    st.write(movie['title'])

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")


        @st.cache_data(show_spinner=False)
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

                # Check if index is within bounds
                if dir_idx >= len(Top_Recommendations):
                    continue

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

        if dir_recommendations:
            st.markdown(f"## **:rainbow[Top Recommendations Directed By {movie_info['director_name']}]**")

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
                                border-radius: 10px;
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
                        st.write(movie['title'])

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


        @st.cache_data(show_spinner=False)
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

                # Check if index is within bounds
                if act_idx >= len(Top_Recommendations):
                    continue

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

        if act_recommendations:
            st.markdown(f"## **:rainbow[Top Recommendations From the Cast {act_movie_info['actor_1_name']}]**")

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
                    st.write(movie['title'])


if st.session_state.mode == 'genre':

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    # Flatten all genre lists and get unique genres
    all_genres = sorted(set(genre.strip() for sublist in genres_info['genres'] for genre in sublist))


    # Use in selectbox
    st.markdown(
        """
        <style>
        /* Target the selectbox text */
        div[data-baseweb="select"] > div {
            background-color: #1f2937; /* background */
            color: #FFFFFF;            /* text color */
            border-radius: 8px;
            padding: 4px 4px;
            font-size: 14px;
        }

        /* Selected option styling */
        div[data-baseweb="select"] span {
            color: #69fff6 !important; /* override Streamlit default */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    selected_genre = st.selectbox(
        " ",
        ['Select a Genre...'] + all_genres
    )

    # Lowercase all genre names
    genres_info['normalized_genres'] = genres_info['genres'].apply(
        lambda genre_list: [g.lower().strip() for g in genre_list]
    )


    # Explode the DataFrame so each row has one genre
    exploded_genres = genres_info.explode('normalized_genres').reset_index(drop=True)


    @st.cache_data(show_spinner=False)
    def genres_top_imdb(genre):
        # Normalize input
        genre = genre.strip().lower()

        # Filter the exploded DataFrame for matching genre
        filtered = exploded_genres[exploded_genres['normalized_genres'] == genre]

        if filtered.empty:
            print("No such genre exists!")
            return []

        # Sort by imdb_score descending
        top_movies = filtered.sort_values(by='imdb_score', ascending=False)[0:5]

        recommended = []
        for _, row in top_movies.iterrows():
            movie_title = row['movie_title']
            imdb_link = row['movie_imdb_link']
            imdb_rating = row['imdb_score']
            poster_url = get_poster(movie_title)

            recommended.append({
                "title": movie_title,
                "link": imdb_link,
                "rating": imdb_rating,
                "poster": poster_url
            })

        return recommended


    @st.cache_data(show_spinner=False)
    def genres_popular(genre):
        # Normalize input
        genre = genre.strip().lower()

        # Filter the exploded DataFrame for matching genre
        filtered = exploded_genres[exploded_genres['normalized_genres'] == genre]

        if filtered.empty:
            print("No such genre exists!")
            return []

        # Sort by imdb_score descending
        top_movies = filtered.sort_values(by='popularity', ascending=False)[0:5]

        recommended = []
        for _, row in top_movies.iterrows():
            movie_title = row['movie_title']
            imdb_link = row['movie_imdb_link']
            imdb_rating = row['imdb_score']
            poster_url = get_poster(movie_title)

            recommended.append({
                "title": movie_title,
                "link": imdb_link,
                "rating": imdb_rating,
                "poster": poster_url
            })

        return recommended


    @st.cache_data(show_spinner=False)
    def genres_gross(genre):
        # Normalize input
        genre = genre.strip().lower()

        # Filter the exploded DataFrame for matching genre
        filtered = exploded_genres[exploded_genres['normalized_genres'] == genre]

        if filtered.empty:
            print("No such genre exists!")
            return []

        # Sort by imdb_score descending
        top_movies = filtered.sort_values(by='gross', ascending=False)[0:5]

        recommended = []
        for _, row in top_movies.iterrows():
            movie_title = row['movie_title']
            imdb_link = row['movie_imdb_link']
            imdb_rating = row['imdb_score']
            poster_url = get_poster(movie_title)

            recommended.append({
                "title": movie_title,
                "link": imdb_link,
                "rating": imdb_rating,
                "poster": poster_url
            })

        return recommended


    if st.button("Recommend") and genres_info is not None:
        top_imdb_recommendations = genres_top_imdb(selected_genre)
        top_popularity_recommendations = genres_popular(selected_genre)
        top_gross_recommendations = genres_gross(selected_genre)

        if top_imdb_recommendations:
            st.markdown(f"## **:rainbow[IMDb Top Rated {selected_genre} Movies]**")

            # Create 5 columns
            cols = st.columns(5)

            for col, movie in zip(cols, top_imdb_recommendations):
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
                    st.write(movie['title'])
                    st.write(f"IMDb: :grey[{movie['rating']}/10]")

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")


        if top_popularity_recommendations:
            st.markdown(f"## **:rainbow[Most Popular {selected_genre} Movies]**")

            # Create 5 columns
            cols = st.columns(5)

            for col, movie in zip(cols, top_popularity_recommendations):
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
                    st.write(movie['title'])

        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

        if top_gross_recommendations:
            st.markdown(f"## **:rainbow[Highest Grossing {selected_genre} Movies]**")

            # Create 5 columns
            cols = st.columns(5)

            for col, movie in zip(cols, top_gross_recommendations):
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
                    st.write(movie['title'])


if st.session_state.mode == 'actor':

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    # Flatten all genre lists and get unique genres
    all_cast = sorted(set(cast.strip() for sublist in cast_info['cast'] for cast in sublist))

    # Use in selectbox
    st.markdown(
        """
        <style>
        /* Target the selectbox text */
        div[data-baseweb="select"] > div {
            background-color: #1f2937; /* background */
            color: #FFFFFF;            /* text color */
            border-radius: 8px;
            padding: 4px 4px;
            font-size: 14px;
        }

        /* Selected option styling */
        div[data-baseweb="select"] span {
            color: #69fff6 !important; /* override Streamlit default */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    selected_cast = st.selectbox(
        " ",
        ['Select an Actor...'] + all_cast
    )

    # Lowercase all genre names
    cast_info['normalized_cast'] = cast_info['cast'].apply(
        lambda cast_list: [g.lower().strip() for g in cast_list]
    )


    # Explode the DataFrame so each row has one genre
    exploded_cast = cast_info.explode('normalized_cast').reset_index(drop=True)


    @st.cache_data(show_spinner=False)
    def cast_top(cast):
        # Normalize input
        cast = cast.strip().lower()

        # Filter the exploded DataFrame for matching genre
        filtered = exploded_cast[exploded_cast['normalized_cast'] == cast]

        if filtered.empty:
            print("No such actor exists!")
            return []

        # Sort by imdb_score descending
        top_movies = filtered.sort_values(by='popularity', ascending=False)[0:25]

        recommended = []
        for _, row in top_movies.iterrows():
            movie_title = row['movie_title']
            imdb_link = row['movie_imdb_link']
            imdb_score = row['imdb_score']
            poster_url = get_poster(movie_title)

            recommended.append({
                "title": movie_title,
                "link": imdb_link,
                "rating": imdb_score,
                "poster": poster_url
            })

        return recommended

    if st.button("Recommend") and cast_info is not None:
        top_cast_recommendations = cast_top(selected_cast)

        if top_cast_recommendations:
            st.markdown(f"## **:rainbow[{selected_cast} Top Movies]**")

            # Show movies in chunks of 5 (3 rows max)
            for i in range(0, len(top_cast_recommendations), 5):
                cols = st.columns(5)
                for j in range(5):
                    if i + j < len(top_cast_recommendations):
                        movie = top_cast_recommendations[i + j]
                        with cols[j]:
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
                            st.write(f"{movie['title']}")



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

st.markdown("## 🌟 Rate this App")

rating = st.radio(
    "How many stars would you give?",
    options=["Still exploring", "⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
    index=0,
    horizontal=True
)

if rating != "Still exploring":
    st.success(f"Thank you for your feedback!")

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
    """
    <style>
    .custom-box {
        background: rgba(20, 20, 20, 0.8);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 40px;
    }

    a.custom-button {
        display: inline-block;
        margin-top: 25px;
        padding: 10px 24px;
        font-size: 18px;        
        background-color: #00FFF0;
        color: black !important;
        text-decoration: none !important;  
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        transition: background-color 0.3s ease;
    }

    a.custom-button:hover {
        background-color: #013b37;
        color: white !important;
        text-decoration: none !important;
    }
    </style>

    <div class='custom-box'>
        <p style='color:#01544e; font-size:65px; font-weight:bold; margin-bottom: 20px;'>
            &lt;/&gt;
        </p>
        <p style='color:#7d7d7d; font-size:65px; font-weight:bold; margin-bottom: 5px;'>
            Developed by Debottam Ghosh
        </p>
        <p style='color:#D3D3D3; font-size:20px;'>
            Wanna give any suggestion personally?<br>
            Or have some cool project ideas that we can work on together?<br>
            Or maybe some small talks on Math, Movies or ML?<br>
            I would love to chat on LinkedIn.
        </p>
        <a href="https://www.linkedin.com/in/debottam-ghosh/" class="custom-button" target="_blank">
            Connect
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
