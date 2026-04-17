# Twitter Sentiment Analysis Setup Guide

## Overview
The `scripts/tweet.py` script analyzes sentiment from tweets about the Iran war conflict from Feb 1 - Apr 17, 2026.

## Prerequisites

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `tweepy` - Twitter API client
- `textblob` - Sentiment analysis
- `pandas` - Data processing
- `matplotlib` - Visualization
- `python-dotenv` - Environment variable management

### 2. Get Twitter/X Developer Credentials

1. Visit: https://developer.twitter.com/
2. Create a developer account
3. Create a new app/project
4. Generate a **Bearer Token** from the "Keys and tokens" section
5. You'll need **Elevated access** or **Academic Research** tier to access the search recent tweets endpoint

### 3. Set Up Environment Variables

#### Option A: Using `.env` file (Recommended)
```bash
# Copy the example file
copy .env.example .env

# Edit .env and replace with your actual token
TWITTER_BEARER_TOKEN=your_actual_token_here
```

#### Option B: Export environment variable
```bash
# Windows PowerShell
$env:TWITTER_BEARER_TOKEN="your_actual_token"

# Windows Command Prompt
set TWITTER_BEARER_TOKEN=your_actual_token

# Mac/Linux
export TWITTER_BEARER_TOKEN=your_actual_token
```

## Running the Script

```bash
# From project root
python scripts/tweet.py
```

## What the Script Does

1. **Authenticates** with Twitter/X using Bearer Token
2. **Queries** tweets containing "iran war" from Feb 1 - Apr 17, 2026
3. **Filters** out retweets and keeps only English tweets
4. **Analyzes sentiment** for each tweet (-1.0 = negative, +1.0 = positive)
5. **Groups data** by date to calculate:
   - Tweet volume (daily count)
   - Average sentiment (daily mean)
6. **Visualizes** results with:
   - Bar chart: Tweet volume by date
   - Line chart: Average sentiment trend

## Output

### Console Output:
```
Fetching tweets... (this may take a while depending on rate limits)

--- Daily Twitter Stats ---
        Date  Tweet_Count  Average_Sentiment
0 2026-02-06           45             0.125
1 2026-02-07           67             0.089
...
```

### Visualization:
- X-axis: Date (Feb 1 - Apr 17, 2026)
- Left Y-axis (Blue bars): Tweet count per day
- Right Y-axis (Red line): Average sentiment score

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'tweepy'"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Error: "401 Unauthorized"
```
Causes:
1. Bearer token is placeholder ("YOUR_BEARER_TOKEN_HERE")
2. Token is invalid or expired
3. Account lacks required API access level

Solution:
1. Verify .env file has your real Bearer token
2. Check token in Twitter Developer Portal
3. Ensure account has elevated/academic access
```

### Error: "No tweet data was fetched"
Possible causes:
1. Invalid API credentials
2. Rate limit exceeded (Twitter has limits on requests)
3. Query returned no results for the date range
4. API access level insufficient for search_recent_tweets endpoint

## API Rate Limits

Twitter/X API has rate limits:
- **Search Recent Tweets**: 450 requests per 15 minutes (varies by access level)
- **Max results per request**: 100

The script limits to 1000 tweets for testing. Modify `limit=1000` in the code to adjust.

## Data Privacy

This script:
- ✅ Uses public Twitter data
- ✅ Respects Twitter ToS
- ✅ Does NOT store credentials in code
- ✅ Uses environment variables for security

## Further Analysis Ideas

1. Compare sentiment trends with market data
2. Identify influencers discussing the conflict
3. Track geolocation of tweets
4. Analyze language/keywords used
5. Correlate sentiment with major events

## References

- [Twitter/X Developer Documentation](https://developer.twitter.com/en/docs)
- [Tweepy Documentation](https://docs.tweepy.org/)
- [TextBlob Documentation](https://textblob.readthedocs.io/)

---

**Status**: Requires valid Twitter API credentials  
**Access Level**: Elevated or Academic Research needed  
**Last Updated**: April 17, 2026
