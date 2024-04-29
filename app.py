import streamlit as st
import pickle
import pandas as pd
import requests as req # to hit API library

def poster_fetch(movie_id):
    response = req.get('https://api.themoviedb.org/3/movie/{}?api_key=009d1afabc99ba51a0e23a88bb3ef2c7&language=en-US'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # print(i[0]) # as returning tuple i.e (1216, 0.28676966733820225)
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)  # need title from index
        # fetch poster from API
        recommended_movies_posters.append(poster_fetch(movie_id))
    return recommended_movies,recommended_movies_posters

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Movie name',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<span style="font-size: 14px;">{names[0]}</span>', unsafe_allow_html=True)
        st.image(posters[0])

    with col2:
        st.markdown(f'<span style="font-size: 14px;">{names[1]}</span>', unsafe_allow_html=True)
        st.image(posters[1])

    with col3:
        st.markdown(f'<span style="font-size: 14px;">{names[2]}</span>', unsafe_allow_html=True)
        st.image(posters[2])

    with col4:
        st.markdown(f'<span style="font-size: 14px;">{names[3]}</span>', unsafe_allow_html=True)
        st.image(posters[3])

    with col5:
        st.markdown(f'<span style="font-size: 14px;">{names[4]}</span>', unsafe_allow_html=True)
        st.image(posters[4])

