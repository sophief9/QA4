# QA4 
Fetch Articles:

Uses the News API to fetch articles based on the chosen topic.
Saves titles and URLs in articles.json.
Summarize Articles:

Reads articles.json.
Uses OpenAI API to generate summaries for each article.
Outputs summarized_articles.json with titles, URLs, and summaries.
Send Email:

Reads summarized_articles.json.
Formats the summaries into a clear, bulleted email.
Sends the email to the specified recipient.
Notes for Future Users
The .json files (articles.json and summarized_articles.json) are not included in the repository to avoid sharing sensitive information.
To execute the project, ensure you have valid API keys and credentials:
News API key.
OpenAI API key.
Gmail app password.
The code is modular, allowing you to modify each step without affecting the others.