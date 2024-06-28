#Deployed Project on Streamlit
https://document-similarity-group3.streamlit.app/

#The code used to create the `Articles.json` file, which serves as our database, was generated through web scraping.
'''import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time
import os
import json

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def fetch_article_links(base_url):
    try:
        response = requests.get(base_url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', href=True) if '/news/' in link['href']]
        return links
    except Exception as e:
        print(f"Failed to fetch links from {base_url}: {e}")
        return []

def fetch_article_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join(para.get_text().strip() for para in paragraphs)
        content = ' '.join(content.split())  
        return content
    except Exception as e:
        print(f"Failed to fetch article from {url}: {e}")
        return None

def save_json_to_file(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Failed to save data to file: {e}")

def load_json_from_file(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load data from file: {e}")
        return []

def get_all_articles(base_url, month, year, processed_urls, delay_seconds=2):
    articles = []

    for day in range(1, 32):  
        date_str = f"{year}-{month:02d}-{day:02d}"
        url = f"{base_url}/{date_str}"
        print(f"Fetching articles for {date_str}...")

        links = fetch_article_links(url)
        for link in links:
            if link in processed_urls:
                print(f"Skipping already processed URL: {link}")
                continue

            content = fetch_article_content(link)
            if content:
                articles.append({'date': date_str, 'url': link, 'content': content})
                processed_urls.add(link)
            time.sleep(delay_seconds)  # Delay between requests

    return articles

def main():
    base_url = 'https://www.dawn.com/archive/latest-news'
    year = 2024
    month = 6
    articles_file_path = 'articles.json'
    processed_urls_file_path = 'processed_urls.json'
    delay_seconds = 5

    print("Loading processed URLs...")
    processed_urls = set(load_json_from_file(processed_urls_file_path))

    print("Fetching articles from the website...")
    articles = get_all_articles(base_url, month, year, processed_urls, delay_seconds)

    if articles:
        existing_articles = load_json_from_file(articles_file_path)
        existing_articles.extend(articles)
        save_json_to_file(existing_articles, articles_file_path)
        save_json_to_file(list(processed_urls), processed_urls_file_path)
    else:
        print("No new articles fetched.")

    print("Reading and displaying all articles from the saved file...")
    saved_articles = load_json_from_file(articles_file_path)

    #for idx, article in enumerate(saved_articles, 1):
        #print(f"Article {idx}:\nDate: {article['date']}\nURL: {article['url']}\nContent: {article['content']}\n{'-'*80}\n")

if __name__ == "__main__":
    main()'''

___________________________________________________________________________________________________________________________

#The code to display all the articles from the `Articles.json` file
'''import json

def read_articles_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            articles = json.load(file)
        return articles
    except Exception as e:
        print(f"Failed to read articles from file: {e}")
        return []

def display_articles(articles):
    for idx, article in enumerate(articles, 1):
        print(f"Article {idx}:\nDate: {article['date']}\nURL: {article['url']}\nContent: {article['content']}\n{'-'*80}\n")

def main():
    articles_file_path = 'articles.json'

    print("Reading and displaying all articles from the saved file...")
    saved_articles = read_articles_from_file(articles_file_path)
    display_articles(saved_articles)

if __name__ == "__main__":
    main()'''

______________________________________________________________________________________________________________________________


#The final code checks for plagiarism of the user-given articles against our `Articles.json` database file
import json
import os
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
        print(f"Failed to load data from file: {e}")
        return []

def check_plagiarism(user_article, articles, threshold=0.7):
    documents = [article['content'] for article in articles] + [user_article]
    tfidf_vectorizer = TfidfVectorizer().fit_transform(documents)
    cosine_matrix = cosine_similarity(tfidf_vectorizer[-1], tfidf_vectorizer[:-1])
    max_similarity = np.max(cosine_matrix)
    return max_similarity, max_similarity > threshold

def main():
    articles_file_path = 'articles.json'

    print("Reading and displaying all articles from the saved file...")
    saved_articles = load_json_from_file(articles_file_path)

    user_article = input("Please enter the article to check for plagiarism: ").strip()
    max_similarity, is_plagiarized = check_plagiarism(user_article, saved_articles)

    if is_plagiarized:
        print(f"Plagiarism detected! Maximum similarity score: {max_similarity}")
    else:
        print(f"No plagiarism detected. Maximum similarity score: {max_similarity}")

if __name__ == "__main__":
    main()





