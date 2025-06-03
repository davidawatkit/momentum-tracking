import tweepy
import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime

# Load environment variables
load_dotenv()

class TwitterBot:
    def __init__(self):
        """Initialize Twitter bot with API credentials."""
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Missing Twitter API credentials in .env file")
        
        # Initialize API client
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)
        
        # Verify credentials
        try:
            self.api.verify_credentials()
        except Exception as e:
            raise Exception(f"Failed to verify Twitter credentials: {str(e)}")

    def post_momentum_tweet(
        self,
        team: str,
        minute: int,
        win_prob_delta: float,
        sentiment_delta: float,
        direction: str = "lost"
    ) -> Optional[str]:
        """
        Post a tweet about a momentum swing.
        
        Args:
            team: Team name
            minute: Game minute when swing occurred
            win_prob_delta: Change in win probability
            sentiment_delta: Change in sentiment
            direction: "lost" or "gained" momentum
            
        Returns:
            Tweet ID if successful, None if failed
        """
        try:
            message = (
                f"🚨 Momentum Shift Detected!\n\n"
                f"{team} {direction} {abs(win_prob_delta):.1%} win probability "
                f"at minute {minute}.\n"
                f"Fan sentiment {'dropped' if sentiment_delta < 0 else 'increased'} "
                f"{abs(sentiment_delta):.2f} pts.\n"
                f"#MomentumTracker"
            )
            
            tweet = self.api.update_status(message)
            return tweet.id_str
            
        except Exception as e:
            print(f"Failed to post tweet: {str(e)}")
            return None

    def post_error_tweet(self, error_message: str) -> Optional[str]:
        """
        Post a tweet about an error in the system.
        
        Args:
            error_message: Description of the error
            
        Returns:
            Tweet ID if successful, None if failed
        """
        try:
            message = (
                f"⚠️ System Alert\n\n"
                f"Error detected: {error_message}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"#MomentumTracker"
            )
            
            tweet = self.api.update_status(message)
            return tweet.id_str
            
        except Exception as e:
            print(f"Failed to post error tweet: {str(e)}")
            return None 