# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import re
import nltk
import string

# Ensure necessary NLTK data packages are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Function to fetch and parse article text from URL
def fetch_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    
    # Get text and remove leading/trailing whitespace
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Function to preprocess text
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    tokens = nltk.word_tokenize(text)
    
    # Remove stopwords
    stopwords = set(nltk.corpus.stopwords.words('english'))
    tokens = [token for token in tokens if token not in stopwords]
    
    
    # Reconstruct text from tokens
    processed_text = ' '.join(tokens)
    
    return processed_text

# URLs of the articles to compare
url1 = 'https://www.example.com/article1'
url2 = 'https://www.example.com/article2'

# Fetch and preprocess articles
article1 = preprocess_text(fetch_article(url1))
article2 = preprocess_text(fetch_article(url2))

# Combine the articles into a list
documents = [article1, article2]


    
