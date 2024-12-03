import requests
import json
import unicodedata
import os

# Hardcode the API Key for testing
API_KEY="" #Insert NEWS API key here (not openai one)
API_URL = "https://newsapi.org/v2/everything" #change this url if you are using a different news site

# Debug: Print the API key
print(f"Using API Key: {API_KEY}")

# Function to clean the article data and ensure it's ASCII-safe
def clean_text(content):
    # Normalize text to remove accents and special characters
    content = unicodedata.normalize("NFKD", content)

    # Replace non-breaking spaces with regular spaces
    content = content.replace("\xa0", " ")

    # Remove any non-ASCII characters explicitly
    content = content.encode('ascii', 'ignore').decode('ascii')  # Remove non-ASCII characters
    
    return content

# Function to fetch articles based on topic
def fetch_articles(topic):
    params = {
        'q': topic,
        'apiKey': API_KEY,
        'pageSize': 5  # Limit the number of articles
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        if data.get("status") == "ok":
            articles = []
            for article in data.get("articles", []):
                title = clean_text(article.get("title", "No Title"))
                url = article.get("url", "No URL")

                if title and url:
                    articles.append({
                        "title": title,
                        "url": url
                    })
            return articles
        else:
            print("No articles found or all articles were removed.")
            return []
    else:
        print(f"Failed to fetch articles. HTTP status code: {response.status_code}")
        return []

def main():
    print("Select a topic to fetch articles:")
    print("1. Education")
    print("2. Health")
    print("3. Travel")
    print("4. Entertainment")
    print("5. Business")
    choice = input("Enter the number corresponding to your choice: ")

    topics = {
        "1": "Education",
        "2": "Health",
        "3": "Travel",
        "4": "Entertainment",
        "5": "Business"
    }

    topic = topics.get(choice)
    if topic:
        print(f"Fetching articles for {topic}...")
        articles = fetch_articles(topic)
        if articles:
            with open("articles.json", "w") as file:
                json.dump(articles, file, indent=4)
            print("Articles fetched and saved successfully!")
        else:
            print("No articles to save.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
