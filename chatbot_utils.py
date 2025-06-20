# chatbot_utils.py

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Sample knowledge base (can be updated from uploaded PDF chunks)
knowledge_base = [
    "TCS offers placement for B.E, B.Tech, and MCA graduates.",
    "Infosys hires candidates with a degree in Computer Science or IT.",
    "HCL offers opportunities for B.Sc, BCA and Engineering graduates.",
    "Zoho recruits candidates through campus placement for B.E, B.Tech.",
    "Freshers from Tamil Nadu engineering colleges are eligible for Wipro placements."
]

# Chunking & relevant chunk extraction
def get_relevant_chunks(query, top_n=2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([query] + knowledge_base)
    similarity = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    top_indices = similarity.argsort()[-top_n:][::-1]
    return [knowledge_base[i] for i in top_indices]

# Web browsing function
def query_web(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}+site:.in"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        results = []
        for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
            text = g.get_text()
            if len(text.strip()) > 50:
                results.append(text)
        return "\n".join(results[:3])
    except Exception as e:
        return f"Error retrieving data: {e}"

# Generate final response
def generate_response(query, chunks, web_data):
    response = "Here is what I found:\n"
    response += "\n".join(chunks)
    if web_data:
        response += f"\n\nBased on latest data:\n{web_data}"
    return response
