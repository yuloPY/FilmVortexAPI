# FilmVortexAPI
 ## Table of Contents
 - [Introduction](#introduction)
 - [Dataset](#dataset)
 - [Preprocess](#preprocess)
 - [API Endpoints](#apiendpoints)
 - [Requirements](requirements)
 - [Contributing](contributing)
 - [Licence](licence)


 # Introduction
 - FilmVortexAPI is built to improve the user experience on movie websites.
 - API learns from user interactions and recommends movies that may be of interest to the user.
 - **Completely open source.**

 # Dataset
 - I used the **[main_dataset.csv](dataset/main_dataset.csv)** dataset to develop and test the content based filtering algorithm.
 - **[main_dataset.csv](dataset/main_dataset.csv)** consists of 'title','genres','keywords' columns and 8660 rows.
 - **[main_dataset.csv](dataset/main_dataset.csv)** file derived from [Full TMDB Movies Dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)

 # Preprocess
 The first step to integrate the API into your website is to edit the **[data_preprocess.py](api/data_preprocess.py)** file.
 - Reads the main dataset from dataset/main_dataset.csv
 - Filters movies based on predefined lists (`add_movie_list` and `drop_movie_list`).
 - Ensures that only valid movies exist in filtered_dataset.csv
 - Warns if any movie titles are not found in the main dataset.

 # API Endpoints
 **1. Log User Interactions**
 - Endpoint: `/interact`
 - Method: `POST`
 - Request Body:
    `{
        "user_id":str,
        "movie":str   
    }`
 - Response:
    `{"message":"Movie {movie} logged for user {user_id}"}`

 **2. Get Movie Recommendations**
 - Endpoint: `/recommend`
 - Method: `POST`
 - Request Body: `{"user_id":str}`
 - Response: `{"user_id":str,"recommended_movies":[...]}`

 # Requirements
  - Python 3.8+
  - [requirements.txt](requirements.txt)

 # Contributing
  Contributions are welcome! Please create a pull request or open an issue to discuss any changes.

 # Licence
  This project is licensed under the **[MIT License](LICENSE)**.