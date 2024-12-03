import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import unicodedata
import re

# Hardcoded App Password (replace this with your actual app password)
APP_PASSWORD = ""  # Replace with your generated Gmail App Password (16 characters)

# Function to clean the email content and ensure it's ASCII-safe
def clean_email_content(content):
    # Normalize text to remove accents and special characters
    content = unicodedata.normalize("NFKD", content)

    # Replace non-breaking spaces and other non-printing characters with regular spaces
    content = content.replace("\xa0", " ")  # Non-breaking space

    # Replace all non-ASCII characters with a question mark or space (depending on preference)
    content = re.sub(r'[^\x00-\x7F]+', '?', content)  # Replace non-ASCII with '?'

    return content

# Function to send email
def send_email(sender_email, recipient_email, subject, body):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Clean the body content before adding to the email
    clean_body = clean_email_content(body)
    print(f"Cleaned email body: {clean_body}")  # Log cleaned content
    
    # Attach the clean body as plain text (force UTF-8 encoding here)
    msg.attach(MIMEText(clean_body, 'plain', _charset='utf-8'))

    try:
        # Connect to Gmail's SMTP server
        print("Connecting to SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        
        # Login to the email account using the App Password
        print("Logging in to SMTP server...")
        server.login(sender_email, APP_PASSWORD)
        
        # Send the email
        print("Sending email...")
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")

# Main function
def main():
    # Get the email details from the user
    sender_email = input("Enter your email address: ")
    recipient_email = input("Enter recipient's email address: ")
    
    # Load the summarized articles from the JSON file
    try:
        with open("summarized_articles.json", "r") as file:
            articles = json.load(file)
    except Exception as e:
        print(f"Error reading summarized articles: {e}")
        return

    # Format the body of the email with the article details
    email_body = "Here are today's summarized articles:\n\n"
    for article in articles:
        title = article.get("title", "No Title")
        url = article.get("url", "No URL")
        summary = article.get("summary", "No Summary")
        
        # Clean each piece of content (title, URL, summary) before adding it to the email body
        title = clean_email_content(title)
        url = clean_email_content(url)
        summary = clean_email_content(summary)
        
        email_body += f"Title: {title}\nURL: {url}\nSummary: {summary}\n\n"

    print(f"Final email body: {email_body}")  # Log final email content

    # Send the email
    send_email(sender_email, recipient_email, "Newsletter Summary", email_body)

if __name__ == "__main__":
    main()
