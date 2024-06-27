import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st

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
    st.title("Plagiarism Checker")

    articles_file_path = 'articles.json'

    st.subheader("Saved Articles")
    saved_articles = load_json_from_file(articles_file_path)
    if saved_articles:
        for article in saved_articles:
            st.text_area("Article", article['content'], height=150, key=article['content'])

    st.subheader("Check for Plagiarism")
    user_article = st.text_area("Enter the article to check for plagiarism:", height=200)
    if st.button("Check"):
        if user_article.strip():
            max_similarity, is_plagiarized = check_plagiarism(user_article, saved_articles)
            if is_plagiarized:
                st.warning(f"Plagiarism detected! Maximum similarity score: {max_similarity}")
            else:
                st.success(f"No plagiarism detected. Maximum similarity score: {max_similarity}")
        else:
            st.error("Please enter an article to check.")

if __name__ == "__main__":
    main()
