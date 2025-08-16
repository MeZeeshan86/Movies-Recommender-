import pickle
import streamlit as st
import requests

# Custom CSS styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #141E30, #243B55);
        color: white;
    }
    .title {
        font-size: 30px !important;
        color: #FFDD57 !important;
        text-align: center;
        margin-bottom: 15px !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.6);
    }
    .subtitle {
        font-size: 30px !important;
        color: #E0E0E0 !important;
        text-align: center;
        margin-bottom: 35px !important;
    }
    .selectbox {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px;
        color: white !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF512F, #DD2476) !important;
        color: white !important;
        border: none;
        padding: 14px 28px;
        border-radius: 10px;
        font-size: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        display: block;
        margin: 25px auto;
    }
    .stButton>button:hover {
        transform: scale(1.08);
        box-shadow: 0 6px 20px rgba(255,75,75,0.5);
    }
    .movie-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 12px;
        margin: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        text-align: center;
    }
    .movie-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 25px rgba(255,255,255,0.15);
    }
    .movie-title {
        font-size: 25px !important;
        font-weight: bold !important;
        color: white !important;
        margin: 10px 0 !important;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bae1e49fea504a1bf1ffd2537aa4cebd&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=Poster+Not+Found"
    except requests.RequestException:
        return "https://via.placeholder.com/500x750?text=Poster+Not+Found"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies = []
    for i in distances[1:6]:  # Top 5 recommendations excluding the movie itself
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_id)
        recommended_movies.append({
            'title': title,
            'poster': poster_url
        })
    return recommended_movies

# App Header
st.markdown('<h1 class="title">🎬 Movie Recommender</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Discover Your Next Favorite Movie ✨</p>', unsafe_allow_html=True)

# Load data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Movie selection dropdown
selected_movie = st.selectbox(
    "🔍 Search for your favorite movie...",
    movies['title'].values,
    key="selectbox"
)

# Recommendation button and display
if st.button('🎥 Get Recommendations'):
    with st.spinner('🔮 Finding the best movies for you...'):
        recommendations = recommend(selected_movie)

        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f'<div class="movie-card">', unsafe_allow_html=True)
                st.image(recommendations[idx]['poster'], use_container_width=True)
                st.markdown(f'<p class="movie-title">{recommendations[idx]["title"]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        st.success('🎉 Recommendations are ready! Enjoy your movie night!')