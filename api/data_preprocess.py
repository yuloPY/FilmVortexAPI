import pandas as pd
import os

# Read the main dataset
main_dataset = pd.read_csv(r"dataset\main_dataset.csv")

add_movie_list = [] # List of movies to be added
drop_movie_list = []  # List of movies to be removed

# Filtering: Select only the movies in add_movie_list
filtered_dataset = main_dataset[main_dataset['title'].isin(add_movie_list)]
filtered_dataset = filtered_dataset[~filtered_dataset['title'].isin(drop_movie_list)]

# Check if the CSV file exists
file_path = "filtered_dataset.csv"
file_exists = os.path.exists(file_path)

# If the CSV file exists, read it, otherwise create an empty DataFrame
if file_exists and os.path.getsize(file_path) > 0:
    existing_filtered = pd.read_csv(file_path)
else:
    existing_filtered = pd.DataFrame(columns=main_dataset.columns)

# If the 'title' column is missing, give a warning and create an empty DataFrame
if 'title' not in existing_filtered.columns:
    print("⚠ Warning: 'title' column not found in filtered_dataset.csv. Creating a new dataset.")
    existing_filtered = pd.DataFrame(columns=main_dataset.columns)

# --- Determine the movies to be added ---
# Select only those in filtered_dataset that are not in the existing file
new_movies_to_add = filtered_dataset[~filtered_dataset['title'].isin(existing_filtered['title'])]

# **If the file does not exist, save with header, otherwise append new data**
if not new_movies_to_add.empty:
    if file_exists and os.path.getsize(file_path) > 0:
        new_movies_to_add.to_csv(file_path, mode="a", index=False, header=False)  # Append
    else:
        new_movies_to_add.to_csv(file_path, mode="w", index=False, header=True)  # Create new
    print(f"✅ {len(new_movies_to_add)} new movies added to {file_path}.")
else:
    print("ℹ No new movies to add.")

# --- Check for titles not found in the main dataset ---
not_found_titles = [title for title in add_movie_list if title not in set(main_dataset['title'])]

if not_found_titles:
    print("⚠ The following titles were not found in the main dataset:")
    for title in not_found_titles:
        print(f"  - {title}")
else:
    print("✅ All titles were found in the main dataset.")
