import tweepy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve credentials
consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_SECRET")

# Initialize Tweepy Client for OAuth 1.0a User Context
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_secret
)

# Test authentication with get_me()
try:
    response = client.get_me()
    user = response.data
    print(f"Connected as: {user.username}")
except tweepy.errors.Forbidden as e:
    print(f"Error: {e}")

# Proceed with fetching liked tweets (or other operations)
try:
    likes_response = client.get_liked_tweets(id=user.id, max_results=1)
    print(likes_response.data)
except tweepy.errors.Forbidden as e:
    print(f"Error: {e}")
