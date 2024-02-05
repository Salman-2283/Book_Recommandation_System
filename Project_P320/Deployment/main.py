import pandas as pd
import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load data
final_ratings = pd.read_csv(r"C:\Users\ds_sa\Desktop\INTERNSHIP\final_ratings.csv")
pt = final_ratings.pivot_table(index="bookTitle", columns="userId", values="bookRating")
pt.fillna(0, inplace=True)



# Function to recommend similar books
def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similarity_scores = cosine_similarity(pt)
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    recommended_books = [pt.index[i[0]] for i in similar_items]
    return recommended_books


# Function to get top 5 rated books for a user
def top_rated_books(user_id):
    user_ratings = pt[user_id].dropna()
    top_rated_books = user_ratings.sort_values(ascending=False).head(5)
    return top_rated_books


# Streamlit app
st.title("Book Recommendation and Rating Checker")

option = st.sidebar.selectbox('Select an Option', ['Book Recommendation', 'Book Rating Checker', 'Top 5 Rated Books'])

if option == 'Book Recommendation':
    st.header("Book Recommendation System")
    book_input = st.text_input("Enter Book Name:")

    if st.button("Recommend"):
        if book_input in pt.index:
            recommended_books = recommend(book_input)
            st.write(f"Books similar to '{book_input}':")
            st.write(recommended_books)
        else:
            st.write(f"Book '{book_input}' not found in the dataset.")

elif option == 'Book Rating Checker':
    st.header("Book Rating Checker")
    user_id_to_check = st.text_input("Enter User ID:")
    book_title_to_check = st.text_input("Enter Book Title:")

    try:
        user_id_to_check = int(user_id_to_check)
    except ValueError:
        pass  # Handle non-integer inputs

    if user_id_to_check in pt.columns:
        if book_title_to_check in pt.index:
            rating = pt.loc[book_title_to_check, user_id_to_check]

            if pd.notna(rating):
                st.write(f"Rating given by User {user_id_to_check} for '{book_title_to_check}': {rating}")
            else:
                st.write(f"User {user_id_to_check} has not rated '{book_title_to_check}'.")
        else:
            st.write(f"Book '{book_title_to_check}' not found in the dataset.")
    else:
        st.write("Invalid User ID. Please enter a valid User ID.")

elif option == 'Top 5 Rated Books':
    st.header("Top 5 Rated Books for a User")
    user_id_for_top_books = st.text_input("Enter User ID:")

    try:
        user_id_for_top_books = int(user_id_for_top_books)
    except ValueError:
        pass  # Handle non-integer inputs

    if user_id_for_top_books in pt.columns:
        top_books = top_rated_books(user_id_for_top_books)
        st.write(f"Top 5 rated books for User {user_id_for_top_books}:")
        st.write(top_books)
    else:
        st.write("Invalid User ID. Please enter a valid User ID.")
