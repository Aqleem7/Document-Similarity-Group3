import requests
import os
import json
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def fetch_article_links(base_url):
    response = requests.get(base_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a') if link.get('href') and '/news/' in link.get('href')]
    return links

def fetch_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content
    except Exception as e:
        print(f"Failed to fetch article from {url}: {e}")
        return None

def preprocess_text(text):
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def load_articles(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_articles(filename, articles):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)

def get_all_articles(base_url, filename):
    existing_articles = load_articles(filename)
    links = fetch_article_links(base_url)
    new_articles = []
    for link in links:  # No limit on the number of articles fetched
        content = fetch_article_content(link)
        if content:
            preprocessed_content = preprocess_text(content)
            if preprocessed_content not in existing_articles:
                new_articles.append(preprocessed_content)
    all_articles = existing_articles + new_articles
    save_articles(filename, all_articles)
    return all_articles

def check_plagiarism(user_article, articles):
    documents = articles + [user_article]
    tfidf_vectorizer = TfidfVectorizer().fit_transform(documents)
    cosine_matrix = cosine_similarity(tfidf_vectorizer[-1], tfidf_vectorizer[:-1])
    max_similarity = np.max(cosine_matrix)
    return max_similarity

def main():
    base_url = 'https://www.dawn.com/archive/latest-news/2024-06-16'
    articles_file = 'articles.json'
    
    print("Fetching articles from the website...")
    articles = get_all_articles(base_url, articles_file)
    if not articles:
        print("No articles fetched. Exiting...")
        return

    user_article = input("Please enter the article to check for plagiarism: ")
    user_article = preprocess_text(user_article)

    max_similarity = check_plagiarism(user_article, articles)
    threshold = 0.7  # Adjust this threshold as needed

    if max_similarity > threshold:
        print(f"Plagiarism detected! Maximum similarity score: {max_similarity}")
    else:
        print(f"No plagiarism detected. Maximum similarity score: {max_similarity}")

        for i in range(len(articles)):
          print(f"Article {i+1}: {articles[i]}")

if __name__ == "__main__":
    main()
