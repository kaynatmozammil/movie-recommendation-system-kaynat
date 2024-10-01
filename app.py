import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch the poster for a movie using TMDB API
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7f28078657cb5b626069772944e5e88f'
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Function to recommend similar movies
def recommend(movie):
    # Fetch the index of the selected movie
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Use 'movie_id' from the DataFrame
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load the movie dataset and similarity matrix
with open('movies.pkl', 'rb') as file:
    data = pickle.load(file)

# Ensure 'movies' is a DataFrame
if isinstance(data, pd.DataFrame):
    movies = data
else:
    movies = pd.DataFrame(data)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title
st.title('Movie Recommender System')

# Create a dropdown box to select a movie title
selected_movie_name = st.selectbox(
    'Choose a movie to get recommendations:',
    movies['title'].values
)

# When 'Recommend' button is clicked
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display recommended movies and posters in columns
    # cols_row1 = st.columns(5)
    #
    # # Manually assign each movie name and poster to its respective column in the first row
    # with cols_row1[0]:
    #     st.text(names[0])
    #     st.image(posters[0])
    #
    # with cols_row1[1]:
    #     st.text(names[1])
    #     st.image(posters[1])
    #
    # with cols_row1[2]:
    #     st.text(names[2])
    #     st.image(posters[2])
    #
    # with cols_row1[3]:
    #     st.text(names[3])
    #     st.image(posters[3])
    #
    # with cols_row1[4]:
    #     st.text(names[4])
    #     st.image(posters[4])
    #
    # # Create the second row with 5 columns
    # cols_row2 = st.columns(5)
    #
    # # Manually assign each movie name and poster to its respective column in the second row
    # with cols_row2[0]:
    #     st.text(names[5])
    #     st.image(posters[5])
    #
    # with cols_row2[1]:
    #     st.text(names[6])
    #     st.image(posters[6])
    #
    # with cols_row2[2]:
    #     st.text(names[7])
    #     st.image(posters[7])
    #
    # with cols_row2[3]:
    #     st.text(names[8])
    #     st.image(posters[8])
    #
    # with cols_row2[4]:
    #     st.text(names[9])
    #     st.image(posters[9])

    # Create a list of rows (two rows, 5 columns each)
    rows = [st.columns(5), st.columns(5)]

    # Loop over the movie names and posters to display them
    for i in range(10):
        col = rows[i // 5][i % 5]  # Selects the appropriate row and column
        with col:
            st.text(names[i])
            st.image(posters[i])
