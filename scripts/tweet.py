# Install required libraries: pip install tweepy textblob pandas matplotlib
import tweepy
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- 1. Twitter API Authentication ---
# You must replace these with your actual X Developer credentials
BEARER_TOKEN = "YOUR_BEARER_TOKEN_HERE"
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# --- 2. Query Setup ---
query = "iran war -is:retweet lang:en"
start_time = "2026-02-01T00:00:00Z" # Start of the conflict per your timeline
end_time = "2026-04-17T00:00:00Z"   # Current date

print("Fetching tweets... (this may take a while depending on rate limits)")

tweet_data = []

# --- 3. Fetch Tweets (Pagination) ---
# Note: Search endpoints and limits depend heavily on your X API tier.
try:
    for tweet in tweepy.Paginator(client.search_recent_tweets, 
                                  query=query,
                                  tweet_fields=['created_at', 'text'],
                                  start_time=start_time,
                                  end_time=end_time,
                                  max_results=100).flatten(limit=1000): # Limit to 1000 for testing
        
        # Calculate Sentiment (-1.0 to 1.0)
        sentiment = TextBlob(tweet.text).sentiment.polarity
        
        tweet_data.append({
            'Date': tweet.created_at.date(),
            'Text': tweet.text,
            'Sentiment': sentiment
        })
except tweepy.TweepyException as e:
    print(f"Twitter API Error: {e}")

# --- 4. Process and Group Data ---
if tweet_data:
    df_tweets = pd.DataFrame(tweet_data)
    
    # Group by date to get the count (volume) and mean sentiment
    daily_stats = df_tweets.groupby('Date').agg(
        Tweet_Count=('Text', 'count'),
        Average_Sentiment=('Sentiment', 'mean')
    ).reset_index()

    print("\n--- Daily Twitter Stats ---")
    print(daily_stats.tail())

    # Plotting Twitter Volume and Sentiment
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Tweet Count', color=color)
    ax1.bar(daily_stats['Date'], daily_stats['Tweet_Count'], color=color, alpha=0.6, label='Volume')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Average Sentiment', color=color)  
    ax2.plot(daily_stats['Date'], daily_stats['Average_Sentiment'], color=color, marker='o', label='Sentiment')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Twitter Volume and Sentiment: "Iran War"')
    fig.tight_layout()  
    plt.show()
else:
    print("No tweet data was fetched. Check your API keys and access levels.")