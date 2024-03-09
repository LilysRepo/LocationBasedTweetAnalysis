from transformers import pipeline
import pandas as pd

# Load the text classification pipeline using a pre-trained model (e.g., 'distilbert-base-uncased')
classifier = pipeline('text-classification', model='distilbert-base-uncased')

# Load data from 'Tweets.csv' assuming it contains a column 'Description'
data = pd.read_csv('Tweets.csv')

# Classify each Description in the data
categories = []
for description in data['Description']:
    description_str = str(description)  # Ensure description is in string format
    result = classifier(description_str)  # Pass the description as a string
    category = result[0]['label']
    categories.append(category)

# Add the 'Category' column to the original DataFrame
data['Category'] = categories

# Save the categorized data with 'Description' and 'Category' columns into 'categoryoftweets.csv'
columns_to_keep = ['Description', 'Category']
data[columns_to_keep].to_csv('categoryoftweets.csv', index=False)
print("Categorized data with 'Description' column saved to 'categoryoftweets.csv'")

# Calculate the count of each category
category_counts = data['Category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']

# Save the counts of each category into 'categoryoftweets_count.csv'
category_counts.to_csv('categoryoftweets_count.csv', index=False)
print("Category counts saved to 'categoryoftweets_count.csv'")