import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from pickle import dump
from pickle import load

st.title('Book Recommendation System')

st.sidebar.header('User Input Parameters')

books = pd.read_csv(r"C:\Users\ds_sa\Desktop\INTERNSHIP\Books.csv")

# Streamlit UI
st.title('User-Based Book Recommendation System')

selected_user = st.selectbox('Select a User:', interactions_df['User'].values)

user_index = interactions_df[interactions_df['User'] == selected_user].index[0]

# Get recommended books based on similar users
similar_users = list(enumerate(cosine_sim[user_index]))
similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)

st.subheader('Recommended Books:')
# Assuming you have a DataFrame named final_ratings
pt = final_ratings.pivot_table(index="bookTitle", columns="userId", values="bookRating")

# Take user ID or book title as input
user_id_or_book_title = input("Enter User ID or Book Title: ")

try:
    # Try converting the input to an integer (assuming it's a user ID)
    user_id_or_book_title = int(user_id_or_book_title)

    # Check if the user ID is valid
    if user_id_or_book_title in pt.columns:
        # Get the user's ratings for all books
        user_ratings = pt[user_id_or_book_title].dropna()

        # Sort books based on the user's ratings
        top_rated_books = user_ratings.sort_values(ascending=False).head(5)

        print(f"Top 5 rated books for User {user_id_or_book_title}:")
        for book_title, rating in top_rated_books.items():
            print(f"{book_title}: {rating}")
    else:
        print("Invalid User ID. Please enter a valid User ID.")
except ValueError:
    # If conversion to int fails, treat the input as a book title
    # Check if the book title is in the DataFrame
    if user_id_or_book_title in pt.index:
        # Get the ratings for the specified book
        ratings_for_book = pt.loc[user_id_or_book_title].dropna()

        print(f"Ratings for book '{user_id_or_book_title}':")
        for user_id, rating in ratings_for_book.items():
            print(f"User {user_id}: {rating}")
    else:
        print(f"Book '{user_id_or_book_title}' not found in the dataset.")


def recommend(book_name):
    # index fetch
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    for i in similar_items:
        print(pt.index[i[0]])


recommend("Into the Wild")

# Assuming you have a DataFrame named final_ratings
pt = final_ratings.pivot_table(index="bookTitle", columns="userId", values="bookRating")

# Take user ID and book title as input
user_id_to_check = input("Enter User ID: ")
book_title_to_check = input("Enter Book Title: ")

# Convert the input to integers (assuming user IDs are integers)
user_id_to_check = int(user_id_to_check)

# Check if the user ID is valid
if user_id_to_check in pt.columns:
    # Check if the book title is in the DataFrame
    if book_title_to_check in pt.index:
        # Get the rating given by the user for the specified book
        rating = pt.loc[book_title_to_check, user_id_to_check]

        if pd.notna(rating):
            print(f"Rating given by User {user_id_to_check} for '{book_title_to_check}': {rating}")
        else:
            print(f"User {user_id_to_check} has not rated '{book_title_to_check}'.")
    else:
        print(f"Book '{book_title_to_check}' not found in the dataset.")
else:
    print("Invalid User ID. Please enter a valid User ID.")


