import tweepy
from textblob import TextBlob
from typing import Dict, List
from datetime import datetime, timedelta
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_twitter_api():
    """Initialize and return Twitter API client."""
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise ValueError("Missing Twitter API credentials in .env file")
    
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def get_tweets_around_time(
    query: str,
    timestamp: datetime,
    minutes_range: int = 3
) -> List[Dict]:
    """
    Scrape tweets around a specific timestamp using Twitter API.
    
    Args:
        query: Search query (e.g., team name, hashtag)
        timestamp: Center point for tweet collection
        minutes_range: Minutes before and after timestamp to collect tweets
        
    Returns:
        List of dictionaries containing tweet information
    """
    api = get_twitter_api()
    tweets = []
    
    try:
        # Search tweets
        search_results = api.search_tweets(
            q=query,
            count=100,  # Maximum allowed by Twitter API
            tweet_mode='extended'
        )
        
        # Filter tweets by time
        for tweet in search_results:
            tweet_time = tweet.created_at
            if abs((tweet_time - timestamp).total_seconds()) <= minutes_range * 60:
                tweets.append({
                    'text': tweet.full_text,
                    'timestamp': tweet_time,
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count
                })
    
    except tweepy.TweepyException as e:
        print(f"Error fetching tweets: {str(e)}")
    
    return tweets

def analyze_sentiment(tweets: List[Dict]) -> Dict[str, float]:
    """
    Analyze sentiment of a list of tweets.
    
    Args:
        tweets: List of tweet dictionaries
        
    Returns:
        Dictionary containing sentiment metrics
    """
    if not tweets:
        return {
            'average_sentiment': 0.0,
            'positive_ratio': 0.0,
            'negative_ratio': 0.0,
            'neutral_ratio': 0.0
        }
    
    sentiments = []
    for tweet in tweets:
        analysis = TextBlob(tweet['text'])
        sentiments.append(analysis.sentiment.polarity)
    
    sentiments = pd.Series(sentiments)
    
    return {
        'average_sentiment': sentiments.mean(),
        'positive_ratio': (sentiments > 0).mean(),
        'negative_ratio': (sentiments < 0).mean(),
        'neutral_ratio': (sentiments == 0).mean()
    }

def get_sentiment_around_time(
    team: str,
    timestamp: datetime,
    minutes_range: int = 3
) -> Dict[str, float]:
    """
    Get sentiment analysis for tweets around a specific time.
    
    Args:
        team: Team name or hashtag to search for
        timestamp: Time to analyze sentiment around
        minutes_range: Minutes before and after timestamp to analyze
        
    Returns:
        Dictionary containing sentiment metrics
    """
    tweets = get_tweets_around_time(team, timestamp, minutes_range)
    return analyze_sentiment(tweets)

def calculate_sentiment_delta(
    before_sentiment: Dict[str, float],
    after_sentiment: Dict[str, float]
) -> float:
    """
    Calculate the change in sentiment between two time periods.
    
    Args:
        before_sentiment: Sentiment metrics before the event
        after_sentiment: Sentiment metrics after the event
        
    Returns:
        float: Change in average sentiment
    """
    return after_sentiment['average_sentiment'] - before_sentiment['average_sentiment'] 