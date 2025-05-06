import requests
from bs4 import BeautifulSoup
import re

def chunk_text(text, chunk_size=500):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def fetch_web_results(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}+site:naukri.com+OR+site:timesjobs.com"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and "http" in href and "webcache" not in href:
            actual_url = re.search(r"(https?://[^\&]+)", href)
            if actual_url:
                results.append(actual_url.group(1))
        if len(results) >= 3:
            break
    return results

def extract_text_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return ' '.join([p.get_text() for p in paragraphs if len(p.get_text()) > 50])
    except:
        return ""

def get_relevant_chunk(chunks, query):
    query = query.lower()
    scored = []
    for chunk in chunks:
        score = sum(1 for word in query.split() if word in chunk.lower())
        scored.append((score, chunk))
    scored.sort(reverse=True)
    return scored[0][1] if scored else ""

def get_bot_response(query):
    search_results = fetch_web_results(query + " IT placement Tamil Nadu")
    text_data = ""
    for url in search_results:
        text_data += extract_text_from_url(url)
    if not text_data:
        return "Sorry, I couldn't find relevant information right now."
    chunks = chunk_text(text_data)
    relevant = get_relevant_chunk(chunks, query)
    return f"Based on what I found:\n\n{relevant}"
