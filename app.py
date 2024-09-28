import streamlit as st # type: ignore
import numpy as np
import pandas as pd


def fetch_poster(movies_info, movie_names):
    # Initialize an empty list to store poster URLs
    posters = []
    
    # Loop through each movie in movie_names
    for movie in movie_names:
        # Find the corresponding poster for the movie
        poster_url = movies_info[movies_info['Title'] == movie]['Poster'].values[0]
        # Append the poster URL to the list
        posters.append(poster_url)
    return posters

def recommend(titles, movie_name, cosine_mat, count):
    pos = np.where(titles == movie_name)[0][0]
    neighbors = cosine_mat[pos]
    nearest_neighbors = neighbors[-count-1:-1]
    nearest_neighbors = nearest_neighbors[::-1]
    nearest_neighbors_names = titles[nearest_neighbors]
    return(nearest_neighbors_names)

def truncate_title(title, max_length = 14):
    if len(title) > max_length:
        return title[:max_length] + '...'  # Add ellipsis
    return title


st.markdown("""
    <style>
    /* Add a hover effect to images */
    img:hover {
        transform: scale(1.05); /* Scale image on hover */
        transition: 0.3s; /* Smooth transition */
    }
    
    /* Hover effect for text color change */
    div:hover span {
        color: #FFA500; /* Change text color on hover */
        transition: 0.2s; /* Smooth transition */
    }

    /* Center align movie posters and titles */
    .movie-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Optional: Add some padding between titles and posters */
    .movie-title {
        margin-bottom: 5px;
    }
    
    /* Background image settings */
    .stApp {
        background-image: url('your_background_image_url');
        background-size: cover;
        background-blend-mode: darken;
        background-color: rgba(0, 0, 0, 0.4);
    }

    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center; color: #FFA500;'>Movie Recommendation</h1>", unsafe_allow_html = True)
st.markdown("<style>.css-123abc {margin-bottom: 20px;}</style>", unsafe_allow_html = True)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://wallpapercave.com/wp/wp8492327.jpg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)


cosine_matrix = np.load('CosineMatrix50.npy')
movies_info = pd.read_csv('Info.csv').reset_index(drop = True)

movies_title = movies_info.Title.values
selected_movie = st.selectbox(
    'Select movie to get recommendation',
    movies_title
)

if st.button('Show recommendation'):
    with st.spinner('Fetching recommendations...'):
        recommended_movies_name = recommend(movies_title, selected_movie, cosine_matrix, 10)
        posters = fetch_poster(movies_info, recommended_movies_name)

    with st.container():
        st.subheader("Top Recommendations")
        cols1 = st.columns(5)
        for i, col in enumerate(cols1):
            with col:
                st.markdown(
                    f"""
                    <div style='display: flex; flex-direction: column; align-items: center;'>
                        <!-- Title Container with Fixed Height -->
                        <div style='white-space: nowrap; overflow: auto; width: 120px; padding: 5px; text-align: center; height: 40px;'>
                            <span title='{recommended_movies_name[i]}'>{recommended_movies_name[i]}</span>
                        </div>
                        <!-- Image -->
                        <img src='{posters[i]}' style='width: 120px; margin-top: 5px;' />
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Second Row
        st.subheader("More Recommendations")
        cols2 = st.columns(5)
        for i, col in enumerate(cols2):
            with col:
                st.markdown(
                    f"""
                    <div style='display: flex; flex-direction: column; align-items: center;'>
                        <!-- Title Container with Fixed Height -->
                        <div style='white-space: nowrap; overflow: auto; width: 120px; padding: 5px; text-align: center; height: 40px;'>
                            <span title='{recommended_movies_name[i+5]}'>{recommended_movies_name[i+5]}</span>
                        </div>
                        <!-- Image -->
                        <img src='{posters[i+5]}' style='width: 120px; margin-top: 5px;' />
                    </div>
                    """,
                    unsafe_allow_html=True
                )
