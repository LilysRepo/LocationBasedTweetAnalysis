import pandas as pd
from textblob import TextBlob

# Load the CSV file into a DataFrame
data = pd.read_csv('tweets.csv')

# Function to get sentiment polarity using TextBlob
def get_sentiment(text):
    analysis = TextBlob(str(text))
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Apply sentiment analysis to the 'Description' column (assuming this contains the tweet text)
data['Sentiment'] = data['Description'].apply(get_sentiment)

# Save the DataFrame with sentiment analysis results to a new CSV file
data.to_csv('tweets_sentiment_analysis.csv', index=False)

# Group by Profile and Sentiment, then count occurrences
sentiment_counts = data.groupby(['Profile', 'Sentiment']).size().unstack(fill_value=0)

# Save the counts to a new CSV file
sentiment_counts.to_csv('sentiment_counts_per_profile.csv')

# Display the counts
print(sentiment_counts)
