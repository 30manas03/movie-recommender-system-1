import pickle
import streamlit as st  # type: ignore
import requests # type: ignore
import pandas as pd # type: ignore

def fetch_poster(movie_title):
    # url1 = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    # url2 = "https://api.themoviedb.org/3/movie/{}?api_key=e03ddf1f52c850781fd30c24d5428eec&language=en-US".format(movie_id)
    url="https://www.omdbapi.com/?t={}&apikey=e4cf043f".format(movie_title)

    try:
        data = requests.get(url, timeout=10)
        data.raise_for_status()
        data = data.json()
        
        # st.text(data)
        # st.text("https://api.themoviedb.org/3/movie/{}?api_key=e03ddf1f52c850781fd30c24d5428eec&language=en-US".format(movie_id))

        # poster_path = data['poster_path']
        poster_path = data['Poster']
        # full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        # full_path1 = "https://image.tmdb.org/t/p/original/" + poster_path
        # return full_path
        return poster_path
    
    except requests.exceptions.Timeout:
        st.error("Connection to the movie database timed out. Please check your internet connection and try again.")
        return None
    
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the poster: {e}")
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances=similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movie_list[1:6]:
        # movie_id = movies.iloc[i[0]].movie_id
        # fetch the movie poster
        # recommended_movie_posters.append(fetch_poster(movie_id))

        recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].title))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
# movies = pickle.load(open('movie_list.pkl','rb'))
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


movies = pd.DataFrame(movies_dict)
selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

if st.button('Show Recommendation'):
    st.subheader(f"Top 5 Recommendations for {selected_movie}")
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    # for i in range(1, 51, 5):  # 10 rows
    #     cols = st.columns(5)   # 5 columns per row
    #     for j in range(5):
    #         idx = i + j
    #         if idx < len(recommended_movie_names):
    #             with cols[j]:
    #                 st.text(recommended_movie_names[idx])
    #                 if recommended_movie_posters[idx]:
    #                     st.image(recommended_movie_posters[idx], width=150)
    #                 else:
    #                     st.text("Poster not available")


    # recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    # for i in range(0, 50, 5):  # 10 rows
    #     cols = st.columns(5)
    #     for j in range(5):
    #         idx = i + j
    #         if idx < len(recommended_movie_names):
    #             with cols[j]:
    #                 st.text(recommended_movie_names[idx])
    #                 st.image(recommended_movie_posters[idx], width=150)



    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

