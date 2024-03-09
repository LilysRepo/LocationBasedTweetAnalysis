import pandas as pd
import numpy as np

# Dictionary of keywords for different categories
keywords = {
    'politics': ['government', 'election', 'policy', 'president', 'parliament'],
    'entertainment': ['movie', 'music', 'actor', 'actress', 'performance'],
    'sports': ['football', 'soccer', 'basketball', 'tennis', 'athlete', 'play','cricket','ball']
    # Add more categories and their respective keywords as needed
}

# Function to classify text based on keywords and location
def classify_text_location(row):
    text = row['Description']
    location = row['Location']

    if isinstance(text, str):  # Check if text is a string (not NaN)
        text = text.lower()  # Convert text to lowercase for case-insensitive matching

        for category, category_keywords in keywords.items():
            for keyword in category_keywords:
                if keyword in text:
                    return category, location  # Return the category and location if a keyword is found

    return 'general', location  # Default category if text is NaN or no specific keywords match

# Read data from the CSV files 'Tweets.csv' and 'Twitter_Account_info.csv'
tweets_data = pd.read_csv('Tweets.csv')
account_info = pd.read_csv('Twitter_Account_info_preprocess.csv')

# Merge data based on the 'Profile' column to get location information for tweets
merged_data = pd.merge(tweets_data, account_info[['Profile', 'Location']], on='Profile', how='left')

# Apply classification function to each row and create new columns 'Category' and 'Location_Category'
merged_data[['Category', 'Location_Category']] = merged_data.apply(classify_text_location, axis=1, result_type='expand')

# Save the merged data with 'Description', 'Profile', 'Category', 'Location', and 'Location_Category' columns into 'tweet_location.csv'
columns_to_keep = ['Description', 'Profile', 'Category', 'Location', 'Location_Category']
merged_data[columns_to_keep].to_csv('tweet_location.csv', index=False)
print("Merged data with 'Description', 'Profile', 'Category', 'Location', and 'Location_Category' columns saved to 'tweet_location.csv'")

# Use the 'tweet_location.csv' for the rest of the analysis
data = pd.read_csv('tweet_location.csv')

# Save the counts of each category into 'tweet_count.csv'
category_counts = data['Category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']
category_counts.to_csv('tweet_count.csv', index=False)
print("Category counts saved to 'tweet_count.csv'")

# Save the counts of each location and category into 'tweet_locationwise_count.csv'
location_category_counts = data.groupby(['Location', 'Category']).size().reset_index(name='Count')
location_category_counts.to_csv('tweet_locationwise_count.csv', index=False)
print("Location-wise and Category-wise counts saved to 'tweet_locationwise_count.csv'")