# Filmy AI Pro – Personalized Movie Recommendations with AI

[![Streamlit App](https://img.shields.io/badge/Launch%20App-Click%20Here-brightgreen?style=for-the-badge)](https://filmy-ai-pro.streamlit.app/)

<br>
Welcome to **Filmy AI Pro**, a smart and interactive movie recommendation app powered by content-based filtering and AI. Whether you're a film enthusiast or a casual viewer, Filmy AI Pro helps you discover movies similar to your favorites — by genre, cast, plot, and even director.
<br>
<br>
If you want to know starting to ending coding and my thought process, you may refer to the notebook file [Filmy AI Pro.ipynb](https://github.com/Debottam-Ghosh/Filmy-AI-Advanced/blob/4cee3bd7962b174a589fbf81464d94328a3e9ba8/Filmy%20AI%20Pro.ipynb)
---

## Features

- **Search by Movie Title** – Get recommendations based on any movie in the dataset.
- **AI-Powered Recommendations** – Uses similarity scores based on metadata (genre, cast, plot keywords).
- **Director-Based Suggestions** – Find other movies by the same director if available.
- **Poster Previews** – Instant poster display via OMDb API integration.
- **IMDb Links** – Jump directly to IMDb pages for more details.
- **Fallback Handling** – Gracefully handles missing data and API limits.

---

## Live Demo

[Click here to try the app](https://filmy-ai-pro.streamlit.app/)

---

## Tech Stack

- Python
- Pandas / NumPy – Data handling and preprocessing
- Scikit-learn – Similarity computation (TF-IDF, cosine similarity)
- Streamlit – App interface
- OMDb API – Fetching posters and metadata
- HTML / CSS – Styled components in Streamlit for custom UI

---

## Dataset

The app uses a movie metadata dataset containing:
- Title, genre, plot keywords
- Cast and crew (actors, director)
- IMDb links
- Budget, gross revenue
- Facebook likes (social metrics)

---

## How to Run Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/filmy-ai-pro.git
   cd filmy-ai-pro

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
3. **Add your OMDb API Key**
   ```bash
   OMDB_API_KEY = "your_api_key_here"
4. **Run the app**
   ```bash
   streamlit run app.py
---

## Features Coming Soon
- TMDb/IMDb rating filters
- Collaborative filtering integration
- Language and country filters
- Mobile-responsive UI

---

## Developer
#### Debottam Ghosh
M.Sc. in Mathematics from IIT Hyderabad
Connect on LinkedIn

---

## Acknowledgments
- OMDb API for poster and metadata
- Streamlit for rapid web app development
- The original IMDb dataset contributors
