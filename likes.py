import tweepy
from keybert import KeyBERT
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_SECRET")

# Create a Client object for v2 API
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret
)

# Get the authenticated user's ID
response = client.get_me()
user = response.data
user_id = user.id

# Initialize KeyBERT model for key phrase extraction
kw_model = KeyBERT()

# Set output directory for markdown files
output_dir = "tweets"
os.makedirs(output_dir, exist_ok=True)

# Fetch your liked tweets (limit to 1 for testing)
likes_response = client.get_liked_tweets(
    id=user_id,
    max_results=1,  # Adjust this value as needed (max 100 per request)
    tweet_fields=["created_at", "author_id"],  # Include additional tweet fields
    expansions=["author_id"]  # Include author details
)

likes = likes_response.data
includes = likes_response.includes
users = {u.id: u for u in includes['users']}  # Map author_id to user object

# Process each tweet
for tweet in likes:
    text = tweet.text
    author = users[tweet.author_id]
    username = author.username
    created_at = tweet.created_at
    
    # Extract key phrases (top 3, n-gram range 1-3)
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words='english',
        top_n=3
    )
    if keywords:
        # Use the top key phrase as the theme (title case)
        theme = keywords[0][0].title()
        # Generate tags from all extracted key phrases
        tags = " ".join([f"#{kw[0].replace(' ', '')}" for kw in keywords])
    else:
        # Fallback if no key phrases are extracted
        theme = "Uncategorized"
        tags = "#Uncategorized"
    
    # Generate title: theme + truncated tweet text
    title = f"{theme} - {text[:50]}..." if len(text) > 50 else f"{theme} - {text}"
    
    # Create markdown content
    markdown_content = f"""
# {title}

**Date:** {created_at.strftime("%Y-%m-%d")}

**Author:** @{username}

**Tweet ID:** {tweet.id}

**Link:** [Original Tweet](https://x.com/{username}/status/{tweet.id})

---

{text}

---

**Tags:** {tags}
"""
    # Save to file
    file_name = f"tweet_{tweet.id}.md"
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(markdown_content)

print(f"Processed {len(likes)} tweets and saved them as markdown files in '{output_dir}' folder.")
