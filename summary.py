import json
import openai
import unicodedata

# Hardcoded API key (replace this with your actual API key)
openai.api_key = ""  # Replace with your actual OpenAI API key

# Function to clean the article data and ensure it's ASCII-safe
def clean_text(content):
    # Normalize text to remove accents and special characters
    content = unicodedata.normalize("NFKD", content)

    # Replace non-breaking spaces with regular spaces
    content = content.replace("\xa0", " ")

    # Remove any non-ASCII characters explicitly
    content = content.encode('ascii', 'ignore').decode('ascii')  # Remove non-ASCII characters
    
    return content

# Function to summarize articles using OpenAI's newer API
def summarize_article(article):
    try:
        title = article.get("title", "")
        url = article.get("url", "")
        
        # Creating the prompt for GPT-4 (or GPT-3.5) using the new format
        prompt = f"Summarize the article titled '{title}' from {url}"

        # Using the correct API method for chat-based models (openai.ChatCompletion.create)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you want the GPT-4 model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # Limit the summary length
        )

        # Extract the summary from the response
        summary = response['choices'][0]['message']['content'].strip()  # Extract from 'message' field
        return clean_text(summary)  # Clean the summary text
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return "Error: Unable to summarize article"

# Main function to summarize articles and save them to a JSON file
def main():
    try:
        with open("articles.json", "r") as file:
            articles = json.load(file)
    except Exception as e:
        print(f"Error reading articles: {e}")
        return

    summarized_articles = []
    for article in articles:
        print(f"Summarizing: {article['title']}")
        summary = summarize_article(article)
        summarized_articles.append({
            "title": article["title"],
            "url": article["url"],
            "summary": summary
        })

    try:
        with open("summarized_articles.json", "w") as file:
            json.dump(summarized_articles, file, indent=4)
        print("Summarized articles saved successfully!")
    except Exception as e:
        print(f"Error saving summarized articles: {e}")

if __name__ == "__main__":
    main()
