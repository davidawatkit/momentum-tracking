import pandas as pd
from datetime import datetime
import json
import os
from typing import Dict, List
import requests
import time

from swing_detector import detect_momentum_swings

class MomentumTracker:
    def __init__(self, team: str, game_id: str = None):
        """
        Initialize the momentum tracker.
        
        Args:
            team: Team name to track
            game_id: ESPN game ID (optional)
        """
        self.team = team
        self.game_id = game_id
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary"
        
    def calculate_win_probability(self, home_score: int, away_score: int, time_remaining: int) -> float:
        """
        Calculate win probability based on score and time remaining.
        This is a simplified model - in practice, you'd want a more sophisticated model.
        
        Args:
            home_score: Home team score
            away_score: Away team score
            time_remaining: Seconds remaining in the game
            
        Returns:
            float: Win probability for the home team
        """
        # Base probability on score difference and time remaining
        score_diff = home_score - away_score
        time_factor = time_remaining / (48 * 60)  # Convert to proportion of game remaining
        
        # Simple model: score difference is more important early in the game
        # and less important as time runs out
        if time_remaining <= 0:
            return 1.0 if score_diff > 0 else 0.0
            
        # Convert score difference to probability using a sigmoid function
        # and adjust for time remaining
        prob = 1 / (1 + 2.71828 ** (-score_diff * time_factor))
        return prob
        
    def get_espn_game_data(self) -> pd.DataFrame:
        """
        Get live game data from ESPN API.
        
        Returns:
            DataFrame with game data
        """
        if not self.game_id:
            raise ValueError("Game ID is required for ESPN data")
            
        try:
            # Get the game data from ESPN API
            url = f"{self.base_url}?event={self.game_id}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse the JSON response
            game_data = response.json()
            
            # Extract game information
            boxscore = game_data.get('boxscore', {})
            home_team = boxscore.get('teams', [{}])[0]
            away_team = boxscore.get('teams', [{}])[1]
            
            # Get current score and time
            home_score = int(home_team.get('teamStats', [{}])[0].get('value', 0))
            away_score = int(away_team.get('teamStats', [{}])[0].get('value', 0))
            time_remaining = int(game_data.get('gameInfo', {}).get('timeRemaining', 0))
            
            # Calculate win probability
            win_prob = self.calculate_win_probability(home_score, away_score, time_remaining)
            
            # Create DataFrame with current game state
            current_minute = 48 - (time_remaining / 60)
            return pd.DataFrame({
                'minute': [current_minute],
                'win_prob': [win_prob],
                'timestamp': [datetime.now()]
            })
            
        except Exception as e:
            print(f"Error fetching ESPN data: {str(e)}")
            return None
    
    def load_game_data(self) -> pd.DataFrame:
        """
        Load game data from ESPN or generate sample data.
        
        Returns:
            DataFrame with game data
        """
        if self.game_id:
            return self.get_espn_game_data()
        else:
            # Generate sample data for testing
            minutes = range(0, 48)
            win_probs = [0.5 + 0.1 * (i % 10) / 10 for i in minutes]
            return pd.DataFrame({
                'minute': minutes,
                'win_prob': win_probs,
                'timestamp': [datetime.now() for _ in minutes]
            })
    
    def process_game(self) -> List[Dict]:
        """
        Process a game and detect momentum swings.
        
        Returns:
            List of detected momentum swings
        """
        # Load game data
        game_data = self.load_game_data()
        
        if game_data is None:
            raise ValueError("Failed to load game data")
        
        # Detect momentum swings
        swings = detect_momentum_swings(game_data)
        
        # Print swing information
        for swing in swings:
            direction = "gained" if swing['delta'] > 0 else "lost"
            print(f"\nMomentum Shift Detected!")
            print(f"{self.team} {direction} {abs(swing['delta']):.1%} win probability at minute {swing['minute']}")
        
        return swings
    
    def save_swings(self, swings: List[Dict], output_path: str):
        """
        Save detected swings to a JSON file.
        
        Args:
            swings: List of swing dictionaries
            output_path: Path to save the data
        """
        with open(output_path, 'w') as f:
            json.dump(swings, f, indent=2, default=str)

def main():
    # Example usage
    tracker = MomentumTracker(
        team="Lakers",
        game_id="401585401"  # Example ESPN game ID
    )
    
    try:
        # Process the game
        swings = tracker.process_game()
        
        # Save results
        tracker.save_swings(swings, "data/swings.json")
        
        print(f"\nDetected {len(swings)} momentum swings")
        print("Results saved to data/swings.json")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 