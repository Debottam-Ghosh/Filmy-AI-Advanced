# Filmy AI Pro – Personalized Movie Recommendations with AI

[![Streamlit App](https://img.shields.io/badge/Launch%20App-Click%20Here-brightgreen?style=for-the-badge)](https://filmy-ai-pro.streamlit.app/)

Welcome to **Filmy AI Pro**, a smart and interactive movie recommendation app powered by content-based filtering and AI. Whether you're a film enthusiast or a casual viewer, Filmy AI Pro helps you discover movies similar to your favorites — by genre, cast, plot, and even director.

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
