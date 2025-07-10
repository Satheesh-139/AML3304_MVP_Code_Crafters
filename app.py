

import pandas as pd

ratings = pd.read_csv('https://files.grouplens.org/datasets/movielens/ml-100k/u.data',sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
movies = pd.read_csv('https://files.grouplens.org/datasets/movielens/ml-100k/u.item',sep='|', encoding='latin-1', header=None, usecols=[0,1], names=['movie_id', 'title'])

ratings = ratings.merge(movies, on='movie_id')


user_movie_matrix = ratings.pivot_table(index='user_id', columns='title', values='rating')


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

item_similarity = cosine_similarity(user_movie_matrix.T.fillna(0))
sim_df = pd.DataFrame(item_similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)

def recommend(movie_title, num_recommendations):
    sim_scores = sim_df[movie_title].sort_values(ascending=False)[1:num_recommendations+1]
    return sim_scores

# print(recommend('Star Wars (1977)', 5))

from sklearn.metrics import mean_squared_error
from math import sqrt

# Example with mock prediction values
y_true = [4, 5, 3, 4.5]
y_pred = [4.2, 4.8, 2.9, 4.4]
print("RMSE:", sqrt(mean_squared_error(y_true, y_pred)))

import streamlit as st

st.title("🎬 Movie Recommender System")
movie_list = sim_df.columns.tolist()
selected_movie = st.selectbox("Pick a movie to get recommendations", movie_list)
num_recs = st.slider("Number of recommendations", 1, 10, 5)

if st.button("Recommend"):
    recs = recommend(selected_movie, num_recs)
    st.write(recs)



