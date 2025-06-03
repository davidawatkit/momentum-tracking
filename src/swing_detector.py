import pandas as pd
import numpy as np
from typing import List, Dict
from datetime import datetime

def detect_momentum_swings(
    df: pd.DataFrame,
    window: int = 3,
    threshold: float = 0.15
) -> List[Dict]:
    """
    Detect significant momentum swings in win probability data.
    
    Args:
        df: DataFrame with columns ['minute', 'win_prob']
        window: Number of minutes to look ahead for swing detection
        threshold: Minimum win probability change to consider as a swing
        
    Returns:
        List of dictionaries containing swing information:
        {
            'minute': int,
            'win_prob_before': float,
            'win_prob_after': float,
            'delta': float,
            'timestamp': datetime
        }
    """
    if not all(col in df.columns for col in ['minute', 'win_prob']):
        raise ValueError("DataFrame must contain 'minute' and 'win_prob' columns")
    
    swings = []
    
    for i in range(len(df) - window):
        current_prob = df.iloc[i]['win_prob']
        future_prob = df.iloc[i + window]['win_prob']
        delta = future_prob - current_prob
        
        if abs(delta) >= threshold:
            swing = {
                'minute': df.iloc[i]['minute'],
                'win_prob_before': current_prob,
                'win_prob_after': future_prob,
                'delta': delta,
                'timestamp': df.iloc[i].get('timestamp', datetime.now())
            }
            swings.append(swing)
    
    return swings

def calculate_swing_magnitude(swing: Dict) -> float:
    """
    Calculate the magnitude of a momentum swing.
    
    Args:
        swing: Dictionary containing swing information
        
    Returns:
        float: Magnitude of the swing (absolute value of delta)
    """
    return abs(swing['delta'])

def get_swing_direction(swing: Dict) -> str:
    """
    Determine the direction of a momentum swing.
    
    Args:
        swing: Dictionary containing swing information
        
    Returns:
        str: 'positive' or 'negative'
    """
    return 'positive' if swing['delta'] > 0 else 'negative' 