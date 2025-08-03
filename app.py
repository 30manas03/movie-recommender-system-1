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
        background: linear-gradient(135deg, #FF4B4B 0%, #FF4B4B 100%);
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
        border-bottom: 2px solid #FF4B4B;
        padding-bottom: 0.5rem;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF4B4B 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
    }
    
    /* Selectbox Styles */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #FF4B4B;
        box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.1);
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
        border-left: 4px solid #FF4B4B;
    }
    
    /* About Section Styles */
    .about-content {
        line-height: 1.6;
        color: #555;
        margin-bottom: 1.5rem;
    }
    
    .feature-item {
        margin-bottom: 0.8rem;
        padding: 1rem 0;
        border-bottom: 1px solid #eee;
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        display: inline-block;
        width: 2rem;
    }
    
    .feature-title {
        color: #FF4B4B;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }
    
    .feature-description {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    .team-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border-left: 4px solid #FF4B4B;
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
        border-top: 4px solid #FF4B4B;
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
        return "https://via.placeholder.com/300x450/FF4B4B/white?text=Error"
    
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the poster: {e}")
        return "https://via.placeholder.com/300x450/FF4B4B/white?text=Error"

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
    st.markdown('<div class="section-title">💬 Feedback & Support</div>', unsafe_allow_html=True)
    
    # Create tabs for different feedback types
    tab1, tab2, tab3 = st.tabs(["📝 General Feedback", "🐛 Bug Report", "💡 Feature Request"])
    
    with tab1:
        st.markdown("### Share Your Experience")
        with st.form("general_feedback_form"):
            col1, col2 = st.columns(2)
            with col1:
                rating = st.select_slider(
                    "Rate your experience:",
                    options=[1, 2, 3, 4, 5],
                    value=5,
                    format_func=lambda x: "⭐" * x
                )
            with col2:
                usage_frequency = st.selectbox(
                    "How often do you use CineMatch?",
                    ["First time", "Occasionally", "Regularly", "Daily"]
                )
            
            feedback_text = st.text_area(
                "Tell us about your experience:",
                placeholder="What did you like? What could be improved? Any suggestions?",
                height=120
            )
            
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input(
                    "Email (optional):",
                    placeholder="your.email@example.com"
                )
            with col2:
                age_group = st.selectbox(
                    "Age Group (optional):",
                    ["", "Under 18", "18-25", "26-35", "36-50", "Over 50"]
                )
            
            submitted = st.form_submit_button("📤 Submit Feedback", use_container_width=True)
            
            if submitted:
                if feedback_text:
                    st.success("🎉 Thank you for your feedback! We'll use it to improve CineMatch.")
                    st.balloons()
                else:
                    st.warning("Please provide some feedback before submitting.")
    
    with tab2:
        st.markdown("### Report a Bug")
        with st.form("bug_report_form"):
            bug_type = st.selectbox(
                "Type of Issue:",
                ["App not loading", "Recommendations not working", "Poster images not showing", 
                 "Navigation problems", "Performance issues", "Other"]
            )
            
            severity = st.selectbox(
                "Severity:",
                ["Low - Minor inconvenience", "Medium - Affects functionality", "High - App unusable"]
            )
            
            bug_description = st.text_area(
                "Describe the issue:",
                placeholder="Please provide detailed steps to reproduce the bug...",
                height=120
            )
            
            browser_info = st.text_input(
                "Browser & Device (optional):",
                placeholder="e.g., Chrome on Windows 10, Safari on iPhone"
            )
            
            submitted = st.form_submit_button("🐛 Report Bug", use_container_width=True)
            
            if submitted:
                if bug_description:
                    st.success("🐛 Bug report submitted! We'll investigate and fix it soon.")
                else:
                    st.warning("Please describe the bug before submitting.")
    
    with tab3:
        st.markdown("### Suggest New Features")
        with st.form("feature_request_form"):
            feature_category = st.selectbox(
                "Feature Category:",
                ["UI/UX Improvements", "New Recommendation Features", "Movie Database", 
                 "User Account Features", "Social Features", "Other"]
            )
            
            feature_title = st.text_input(
                "Feature Title:",
                placeholder="Brief title for your feature request"
            )
            
            feature_description = st.text_area(
                "Feature Description:",
                placeholder="Describe the feature you'd like to see...",
                height=120
            )
            
            impact = st.selectbox(
                "How important is this feature?",
                ["Nice to have", "Would be useful", "Very important", "Essential"]
            )
            
            submitted = st.form_submit_button("💡 Submit Feature Request", use_container_width=True)
            
            if submitted:
                if feature_title and feature_description:
                    st.success("💡 Feature request submitted! We'll consider it for future updates.")
                else:
                    st.warning("Please provide both title and description.")
    
    # Contact Information
    st.markdown("---")
    st.markdown("### 📧 Contact Us")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Email:** support@cinematch.com")
    with col2:
        st.markdown("**Twitter:** @CineMatchApp")
    with col3:
        st.markdown("**GitHub:** github.com/cinematch")

def render_about_section():
    st.markdown('<div class="section-title">ℹ️ About CineMatch</div>', unsafe_allow_html=True)
    
    # Mission Statement
    st.markdown("### 🎯 Our Mission")
    st.markdown("""
    **CineMatch** is an intelligent movie recommendation system designed to revolutionize how you discover films. 
    We believe everyone deserves to find their perfect movie match, and our AI-powered platform makes that possible 
    through advanced machine learning and comprehensive movie analysis.
    """)
    
    # Key Features
    st.markdown("### 🚀 Key Features")
    features = [
        ("🎯", "Personalized Recommendations", "Get movie suggestions tailored to your unique preferences and viewing history using advanced content-based filtering"),
        ("🤖", "AI-Powered Algorithm", "Advanced machine learning algorithms analyze thousands of movie attributes including genre, cast, plot, and themes for accurate predictions"),
        ("🎬", "Extensive Movie Database", "Access to over 4,800 movies across all genres, from timeless classics to the latest blockbuster releases"),
        ("⚡", "Lightning Fast Performance", "Get personalized recommendations in under 2 seconds with our optimized recommendation engine"),
        ("🎨", "Beautiful Modern Interface", "Clean, intuitive design with smooth animations and responsive layout that works seamlessly across all devices"),
        ("📱", "Mobile-First Design", "Responsive design optimized for mobile devices while maintaining full functionality on desktop and tablet"),
        ("🔍", "Smart Search & Filter", "Advanced search capabilities with intelligent autocomplete and filtering options"),
        ("💬", "Interactive Feedback", "Built-in feedback system to help us improve recommendations and user experience"),
        ("🔄", "Real-time Updates", "Live updates and continuous improvement of our recommendation algorithms"),
        ("🛡️", "Privacy Focused", "No personal data collection - recommendations based purely on movie selection")
    ]
    
    # Display features in a clean list format
    for icon, title, description in features:
        st.markdown(f"""
        <div class="feature-item">
            <span class="feature-icon">{icon}</span>
            <div class="feature-title">{title}</div>
            <div class="feature-description">{description}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.markdown("### 🔬 How It Works")
    st.markdown("""
    Our recommendation engine uses sophisticated **content-based filtering** to analyze multiple movie characteristics:
    
    - **Genre Analysis:** Identifies similar genres and sub-genres
    - **Cast & Crew:** Considers actors, directors, and production teams
    - **Plot Keywords:** Analyzes story themes and plot elements
    - **Release Era:** Considers the time period and cultural context
    
    When you select a movie you enjoyed, our algorithm calculates similarity scores with all other movies in our database and presents you with the top 5 most similar recommendations.
    """)
    
    # Technology Stack
    st.markdown("### 🛠️ Technology Stack")
    tech_col1, tech_col2 = st.columns(2)
    with tech_col1:
        st.markdown("""
        **Frontend & UI:**
        - Streamlit (Python web framework)
        - Custom CSS styling
        - Responsive design
        
        **Data Processing:**
        - Pandas (Data manipulation)
        - NumPy (Numerical computing)
        """)
    with tech_col2:
        st.markdown("""
        **Machine Learning:**
        - Scikit-learn (ML algorithms)
        - Content-based filtering
        - Cosine similarity
        
        **APIs & Data:**
        - OMDB API (Movie posters)
        - TMDb dataset (Movie information)
        """)
    
    # Data Source
    st.markdown("### 📊 Data Sources")
    st.markdown("""
    Our recommendations are powered by comprehensive movie data from:
    
    - **The Movie Database (TMDb):** Primary source for movie metadata, including genres, cast, crew, and plot information
    - **OMDB API:** High-quality movie posters and additional movie details
    - **Curated Dataset:** Carefully processed and cleaned dataset of over 4,800 movies
    """)
    
    # Statistics
    st.markdown("### 📈 Platform Statistics")
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        st.metric("Movies in Database", "4,800+")
    with stats_col2:
        st.metric("Genres Covered", "20+")
    with stats_col3:
        st.metric("Recommendation Speed", "< 2 seconds")
    
    # Team Section
    st.markdown("### 👥 Our Team")
    st.markdown("""
    CineMatch is developed by a passionate team of data scientists, machine learning engineers, and movie enthusiasts dedicated to revolutionizing the way people discover films.
    
    **🌟 Meet Our Core Team:**
    
    - **Data Science Lead:** Specializes in recommendation algorithms and machine learning
    - **Frontend Developer:** Creates intuitive and beautiful user interfaces
    - **Backend Engineer:** Ensures robust and scalable system architecture
    - **UI/UX Designer:** Crafts seamless user experiences across all devices
    
    We believe in the power of personalized recommendations to enhance your movie-watching experience and help you discover hidden gems you might otherwise miss. Our mission is to make movie discovery effortless, enjoyable, and accurate through the power of artificial intelligence and comprehensive data analysis.
    """)
    
    # Future Plans
    st.markdown("### 🔮 Future Plans")
    st.markdown("""
    We're constantly working to enhance CineMatch and bring you the best movie discovery experience. Here's what we have planned:
    
    **🎯 Short-term Goals (Next 3-6 months):**
    - **Enhanced Personalization:** User accounts with watch history and preference learning
    - **Advanced Filtering:** Filter recommendations by genre, year, rating, and cast
    - **Mobile App:** Native iOS and Android applications for on-the-go recommendations
    - **Social Features:** Share recommendations with friends and create watchlists
    
    **🚀 Medium-term Goals (6-12 months):**
    - **AI Chat Assistant:** Interactive movie recommendation chatbot
    - **Voice Search:** Voice-activated movie search and recommendations
    - **Multi-language Support:** Expand to support multiple languages and regional content
    - **Advanced Analytics:** Detailed insights into your movie preferences and trends
    
    **🌟 Long-term Vision (1+ years):**
    - **Predictive Recommendations:** AI that predicts what you'll want to watch before you know it
    - **Virtual Reality Integration:** Immersive movie discovery experiences
    - **Global Content:** Access to international films and regional cinema
    - **Community Features:** Movie clubs, discussion forums, and user-generated content
    - **Integration Partnerships:** Connect with streaming platforms for seamless watching
    
    **🔬 Research & Development:**
    - **Advanced ML Models:** Implementing state-of-the-art recommendation algorithms
    - **Sentiment Analysis:** Understanding emotional responses to movies
    - **Cross-platform Sync:** Seamless experience across all your devices
    - **Accessibility Features:** Making CineMatch accessible to users with disabilities
    
    We're excited to bring these features to life and continue revolutionizing how people discover and enjoy movies!
    """)

def main():
    # Load CSS
    load_css()
    
    # Initialize session state for theme
    if 'dark_theme' not in st.session_state:
        st.session_state.dark_theme = False
    
    # Apply dark theme if selected
    if st.session_state.dark_theme:
        st.markdown('<div class="dark-theme">', unsafe_allow_html=True)
    
    # Render header
    render_header()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        selected = option_menu(
            menu_title=None,
            options=["Movie Recommender", "Feedback", "About Us"],
            icons=["film", "chat-dots", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#FF4B4B", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px 15px",
                    "border-radius": "10px",
                    "margin-bottom": "5px"
                },
                "nav-link-selected": {"background-color": "#FF4B4B"},
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
