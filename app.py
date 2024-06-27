import json
import os
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_json_from_file(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Failed to load data from file: {e}")
        return []

def check_plagiarism(user_article, articles, threshold=0.7):
    documents = [article['content'] for article in articles] + [user_article]
    tfidf_vectorizer = TfidfVectorizer().fit_transform(documents)
    cosine_matrix = cosine_similarity(tfidf_vectorizer[-1], tfidf_vectorizer[:-1])
    max_similarity = np.max(cosine_matrix)
    return max_similarity, max_similarity > threshold

def main():
    st.title("Plagiarism Detection")

    articles_file_path = 'articles.json'

    st.subheader("Uploaded Articles")
    saved_articles = load_json_from_file(articles_file_path)
    if saved_articles:
        for article in saved_articles:
            st.text_area(f"Article {saved_articles.index(article) + 1}", article['content'], height=200)
    else:
        st.info("No articles found in the saved file.")

    st.subheader("Check for Plagiarism")
    user_article = st.text_area("Enter the article to check for plagiarism:", height=200)

    if st.button("Check"):
        if user_article:
            max_similarity, is_plagiarized = check_plagiarism(user_article, saved_articles)
            if is_plagiarized:
                st.error(f"Plagiarism detected! Maximum similarity score: {max_similarity:.2f}")
            else:
                st.success(f"No plagiarism detected. Maximum similarity score: {max_similarity:.2f}")
        else:
            st.warning("Please enter an article to check.")

'''if _name_ == "_main_":
    main()'''
