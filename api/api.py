from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

app = FastAPI()

# Dictionary to store user interactions
user_interactions = dict()

# Ensure data preprocessing runs before loading the dataset
import data_preprocess  

# Check if the processed dataset exists
filtered_data_path = "filtered_dataset.csv"
if os.path.exists(filtered_data_path):
    films = pd.read_csv(filtered_data_path)
else:
    raise FileNotFoundError("Filtered dataset not found. Please check data preprocessing.")

# Combine genres and keywords into a single string
films["combined"] = films["genres"] + " " + films["keywords"]
corpus = films["combined"].tolist()

# Create TF-IDF matrix
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

# Model to add user interaction to the API
class UserInteraction(BaseModel):
    user_id: str
    movie: str

# Model to get recommendations for the user
class UserRecommendation(BaseModel):
    user_id: str

@app.post("/interact")
def log_interaction(interaction: UserInteraction):
    """ Logs a user's interaction with a movie. """
    if interaction.user_id not in user_interactions:
        user_interactions[interaction.user_id] = []
    
    if interaction.movie not in user_interactions[interaction.user_id]:
        user_interactions[interaction.user_id].append(interaction.movie)

    return {"message": f"Movie {interaction.movie} logged for user {interaction.user_id}."}

@app.post("/recommend")
def recommend_movies(user_data: UserRecommendation):
    """ Recommends movies based on the user's interactions. """
    user_id = user_data.user_id
    if user_id not in user_interactions or len(user_interactions[user_id]) < 5:
        raise HTTPException(status_code=400, detail="Not enough interaction data for this user. At least 5 interactions are required.")

    user_interacted = user_interactions[user_id]

    # Get indices of the movies the user has interacted with
    user_indices = [i for i, film in films.iterrows() if film["title"] in user_interacted]

    if not user_indices:
        raise HTTPException(status_code=400, detail="Interacted movies are not in the dataset.")

    # Create user profile
    user_profile = tfidf_matrix[user_indices].mean(axis=0)
    user_profile_array = np.asarray(user_profile)

    # Calculate similarities
    similarities = cosine_similarity(user_profile_array, tfidf_matrix).flatten()

    # Exclude movies the user has already interacted with from recommendations
    for idx in user_indices:
        similarities[idx] = -1

    # Get top 10 recommendations
    recommended_indices = similarities.argsort()[-10:][::-1]
    recommended_movies = [films.iloc[idx]["title"] for idx in recommended_indices]

    return {"user_id": user_id, "recommended_movies": recommended_movies}
