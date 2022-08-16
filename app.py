import streamlit as st
import pickle
import pandas as pd
import requests


# fetching posted url for displaying movies
def fetch_poster(movie_id):
    res = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=ba7902a803993bc4adefee8c35a35fbc&language=en-US".format(
            movie_id))
    data = res.json()
    # st.write(data)
    # st.write(movie_id)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# returns list of recommended movie names and poster urls to show in result
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from movie id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

# similarity holds cosine distance matrix for each movie
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

movies_list = pickle.load(open('movie.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

selected_movie_name = st.selectbox(
    'Select your movie',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5,gap="medium")

    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])
    with col3:
        st.header(names[2])
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])
