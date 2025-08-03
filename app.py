import pickle
import streamlit as st
import requests
import pandas as pd
# This is CORRECT
from streamlit_option_menu import option_menu
import base64

# Page configuration
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header Styles */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 300;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Movie Card Styles */
    .movie-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    .movie-title {
        font-weight: 600;
        font-size: 0.9rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    .movie-poster {
        border-radius: 10px;
        width: 100%;
        height: auto;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar Styles */
    .sidebar-section {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .section-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Selectbox Styles */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Theme Toggle */
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        background: white;
        border-radius: 50px;
        padding: 0.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Dark Theme Styles */
    .dark-theme {
        background-color: #1a1a1a;
        color: white;
    }
    
    .dark-theme .movie-card {
        background: #2d2d2d;
        border: 1px solid #404040;
    }
    
    .dark-theme .sidebar-section {
        background: #2d2d2d;
        border: 1px solid #404040;
    }
    
    .dark-theme .section-title {
        color: white;
    }
    
    .dark-theme .movie-title {
        color: white;
    }
    
    /* Feedback Form Styles */
    .feedback-form {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
    }
    
    /* About Section Styles */
    .about-content {
        line-height: 1.6;
        color: #555;
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 8px;
    }
    
    .feature-icon {
        margin-right: 0.8rem;
        font-size: 1.2rem;
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .header-container {
            padding: 1rem;
        }
        
        .movie-card {
            margin-bottom: 0.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def fetch_poster(movie_title):
    url = "https://www.omdbapi.com/?t={}&apikey=e4cf043f".format(movie_title)
    
    try:
        data = requests.get(url, timeout=10)
        data.raise_for_status()
        data = data.json()
        
        poster_path = data.get('Poster', '')
        if poster_path and poster_path != 'N/A':
            return poster_path
        else:
            return "https://via.placeholder.com/300x450/667eea/white?text=No+Poster"
    
    except requests.exceptions.Timeout:
        st.error("Connection to the movie database timed out. Please check your internet connection and try again.")
        return "https://via.placeholder.com/300x450/667eea/white?text=Error"
    
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the poster: {e}")
        return "https://via.placeholder.com/300x450/667eea/white?text=Error"

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = similarity[index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
        
        recommended_movie_names = []
        recommended_movie_posters = []
        
        for i in movie_list[1:6]:
            movie_title = movies.iloc[i[0]].title
            recommended_movie_names.append(movie_title)
            recommended_movie_posters.append(fetch_poster(movie_title))
        
        return recommended_movie_names, recommended_movie_posters
    
    except Exception as e:
        st.error(f"An error occurred while generating recommendations: {e}")
        return [], []

def render_header():
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🎬 CineMatch</h1>
        <p class="header-subtitle">Discover your next favorite movie with AI-powered recommendations</p>
    </div>
    """, unsafe_allow_html=True)

def render_movie_recommender():
    st.markdown('<div class="section-title">🎯 Movie Recommender</div>', unsafe_allow_html=True)
    
    # Movie selection
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movies['title'].values,
        help="Choose a movie you enjoyed to get similar recommendations"
    )
    
    # Recommendation button
    if st.button('🚀 Get Recommendations', key='recommend_btn'):
        with st.spinner('Finding perfect matches for you...'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            
            if recommended_movie_names:
                st.markdown(f'<div class="section-title">🌟 Top 5 Recommendations for "{selected_movie}"</div>', unsafe_allow_html=True)
                
                # Display recommendations in a grid
                cols = st.columns(5)
                for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="movie-card">
                            <div class="movie-title">{name}</div>
                            <img src="{poster}" class="movie-poster" alt="{name}">
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Sorry, we couldn't generate recommendations. Please try another movie.")

def render_feedback_section():
    st.markdown('<div class="section-title">💬 Feedback</div>', unsafe_allow_html=True)
    
    with st.form("feedback_form"):
        st.markdown('<div class="feedback-form">', unsafe_allow_html=True)
        
        # Rating
        rating = st.select_slider(
            "Rate your experience:",
            options=[1, 2, 3, 4, 5],
            value=5,
            format_func=lambda x: "⭐" * x
        )
        
        # Feedback type
        feedback_type = st.selectbox(
            "Feedback Type:",
            ["General Feedback", "Bug Report", "Feature Request", "Recommendation Quality"]
        )
        
        # Feedback text
        feedback_text = st.text_area(
            "Your feedback:",
            placeholder="Tell us about your experience with CineMatch...",
            height=100
        )
        
        # Contact info (optional)
        email = st.text_input(
            "Email (optional):",
            placeholder="your.email@example.com"
        )
        
        submitted = st.form_submit_button("📤 Submit Feedback")
        
        if submitted:
            if feedback_text:
                st.success("🎉 Thank you for your feedback! We appreciate your input.")
                st.balloons()
            else:
                st.warning("Please provide some feedback before submitting.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_about_section():
    st.markdown('<div class="section-title">ℹ️ About CineMatch</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="about-content">
        <p><strong>CineMatch</strong> is an intelligent movie recommendation system that helps you discover new films based on your preferences. Using advanced machine learning algorithms, we analyze movie features to find the perfect matches for your taste.</p>
        
        <h4>🚀 Key Features:</h4>
    </div>
    """, unsafe_allow_html=True)
    
    features = [
        ("🎯", "Personalized Recommendations", "Get movie suggestions tailored to your preferences"),
        ("🤖", "AI-Powered Algorithm", "Advanced machine learning for accurate predictions"),
        ("🎬", "Extensive Movie Database", "Access to thousands of movies across all genres"),
        ("⚡", "Fast & Responsive", "Get recommendations in seconds"),
        ("🎨", "Beautiful Interface", "Clean, modern design for the best user experience")
    ]
    
    for icon, title, description in features:
        st.markdown(f"""
        <div class="feature-item">
            <span class="feature-icon">{icon}</span>
            <div>
                <strong>{title}</strong><br>
                <small>{description}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="about-content">
        <h4>🔬 How It Works:</h4>
        <p>Our recommendation engine uses content-based filtering to analyze movie characteristics such as genres, cast, crew, and plot keywords. When you select a movie you enjoyed, the system finds other movies with similar attributes and presents you with the top 5 matches.</p>
        
        <h4>📊 Data Source:</h4>
        <p>Our recommendations are powered by The Movie Database (TMDb), ensuring up-to-date and comprehensive movie information.</p>
        
        <h4>👥 Team:</h4>
        <p>CineMatch is developed by a passionate team of data scientists and movie enthusiasts who believe in the power of personalized recommendations to enhance your movie-watching experience.</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Load CSS
    load_css()
    
    # Initialize session state for theme
    if 'dark_theme' not in st.session_state:
        st.session_state.dark_theme = False
    
    # Theme toggle in sidebar
    with st.sidebar:
        st.markdown("### 🎨 Theme")
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            if st.button("☀️ Light"):
                st.session_state.dark_theme = False
        with theme_col2:
            if st.button("🌙 Dark"):
                st.session_state.dark_theme = True
    
    # Apply dark theme if selected
    if st.session_state.dark_theme:
        st.markdown('<div class="dark-theme">', unsafe_allow_html=True)
    
    # Render header
    render_header()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        selected = streamlit_option_menu(
            menu_title=None,
            options=["Movie Recommender", "Feedback", "About Us"],
            icons=["film", "chat-dots", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#667eea", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px 15px",
                    "border-radius": "10px",
                    "margin-bottom": "5px"
                },
                "nav-link-selected": {"background-color": "#667eea"},
            }
        )
    
    # Main content area
    if selected == "Movie Recommender":
        render_movie_recommender()
    elif selected == "Feedback":
        render_feedback_section()
    elif selected == "About Us":
        render_about_section()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Made with ❤️ by the CineMatch Team | © 2024 CineMatch. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
    return pd.DataFrame(movies_dict), similarity_matrix

# Load the data
movies, similarity = load_data()

if __name__ == "__main__":
    main()
