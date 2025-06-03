# 🧠 Momentum Shift Tracker

A real-time sports analytics tool that detects psychological momentum swings in games using win probability data and Twitter sentiment analysis.

## 🌟 Features

- Real-time win probability swing detection
- Twitter sentiment analysis around key moments
- Automated momentum shift alerts via Twitter
- Future ML model for team resilience prediction

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/momentum-tracking.git
cd momentum-tracking
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your Twitter API credentials:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

## 🚀 Usage

Run the main script:
```bash
python src/main.py
```

## 📁 Project Structure

```
momentum_tracker_bot/
├── data/                  # Game data (CSV, JSON, etc.)
├── models/                # ML model scripts and saved models
├── src/                   # Core app logic
│   ├── main.py           # Main execution script
│   ├── swing_detector.py # Win probability swing detection
│   ├── sentiment.py      # Twitter sentiment analysis
│   ├── twitter_bot.py    # Twitter bot integration
│   └── utils.py          # Helper functions
├── requirements.txt
├── .env
└── README.md
```

## 🔧 Configuration

- Adjust swing detection parameters in `swing_detector.py`
- Modify sentiment analysis settings in `sentiment.py`
- Configure Twitter bot settings in `twitter_bot.py`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 