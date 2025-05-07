import json
import os
import requests

# Dummy chunks (extend with real placement data)
chunks = {
    "btech": "Companies like TCS, Infosys, and Wipro hire B.Tech graduates through campus and off-campus.",
    "mca": "Zoho, HCL, and Accenture hire MCA graduates. Online assessments and interviews are common.",
    "diploma": "HCL and CTS occasionally hire diploma holders. Look for TechBee or off-campus drives."
}

def get_relevant_chunk(query):
    query = query.lower()
    for key in chunks:
        if key in query:
            return chunks[key]
    return "Sorry, I don't have information on that qualification."

def ask_bot(query, chunk):
    return f"Based on your qualification, here's what I found: {chunk}"

def save_chat(username, question, response):
    path = "data/chat_history.json"
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({}, f)

    with open(path, "r+") as f:
        data = json.load(f)
        data.setdefault(username, []).append({"q": question, "a": response})
        f.seek(0)
        json.dump(data, f, indent=4)
