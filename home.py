import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
import folium
from geopy.geocoders import Nominatim
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from textblob import TextBlob
import os
import mplcursors

def data_extract():
    clear_content()

    # Create a label to display preprocessing status
    status_label = tk.Label(right_frame, text="Data scraping is going on", font=("Arial", 20,"bold"))
    status_label.pack(padx=20, pady=20)

    # Schedule the data extraction after 15 seconds
    left_frame.after(10000, extract_and_display_data)

def extract_and_display_data():  
    clear_content()
    # Update the status label
    status_label = tk.Label(right_frame, text="Extracted Data from Twitter", font=("Arial", 12))
    status_label.pack(padx=20, pady=20)

     # Call the function to load and display CSV data
    data_extract_csv="Twitter_Account_info.csv"
    load_csv_data(data_extract_csv)
    

def display_map():
    # Path to the HTML file containing the map
    map_file = "map_with_bold_location.html"
    # Open the HTML file in the default web browser
    webbrowser.open(map_file)

def load_csv_data(file_path):
    if file_path=='Twitter_Account_info_preprocess.csv':
        clear_content()
        display_buttons()
    # Load CSV data using pandas
    data = pd.read_csv(file_path)

    # Create a new frame within the existing Tkinter window
    tree_frame = ttk.Frame(right_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Create a treeview widget (Data Grid)
    tree = ttk.Treeview(tree_frame, height=15, columns=list(data.columns))

    # Set up columns
    tree["show"] = "headings"

    # Add columns to the treeview
    for col in tree["columns"]:
        tree.heading(col, text=col)

    # Insert data into the treeview
    for i, row in data.iterrows():
        tree.insert("", "end", values=list(row))

    # Set default width for each column in Treeview
    for col in tree["columns"]:
        tree.column(col, width=100)  # Adjust width as needed

    # Add treeview to frame and pack it
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar for the treeview
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.config(yscrollcommand=scrollbar.set)

def location_wise_tweet():
    clear_content()
    
    try:
        # Read CSV file
        file_path = 'Twitter_Account_info.csv'
        df = pd.read_csv(file_path)
        
        # Group by 'Location' and count occurrences
        location_counts = df['Location'].value_counts()

        # Create a new frame within the existing Tkinter window to display the chart
        chart_frame = tk.Frame(right_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True)

        # Plot bar chart
        plt.figure(figsize=(8, 6))
        bars = location_counts.plot(kind='bar', color='skyblue')
        plt.title('Location-wise Tweeting Users Count')
        plt.xlabel('Location')
        plt.ylabel('Tweeting Users Count')
        plt.xticks(rotation=0)  # Rotate x-labels to 0 degrees
        plt.xticks(rotation='vertical')  # Rotate x-labels vertically
        plt.tight_layout()

        # Display chart in the chart frame
        canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Display location names with mouse hover
        mplcursors.cursor(bars, hover=True).connect("add", lambda sel: sel.annotation.set_text(location_counts.index[sel.target.index]))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def data_preprocess():
    clear_content()

    # Create a label to display preprocessing status
    status_label = tk.Label(right_frame, text="Data preprocessing in progess", font=("Arial", 20,"bold"))
    status_label.pack(padx=20, pady=20)

    # Schedule the data extraction after 15 seconds
    left_frame.after(5000, preprocessed_data)


def preprocessed_data():
    clear_content()
    # Update the status label
    status_label = tk.Label(right_frame, text="Data preprocessing completed", font=("Arial", 12))
    status_label.pack(padx=20, pady=20)

    
    if os.path.exists('Twitter_Account_info_preprocess.csv'):
        display_buttons()
    else:
        save_map_and_csv()

def valid_invalid_notshared():
    clear_content()
    display_buttons()
    # Read the Location_Counts.csv file
    counts_data = pd.read_csv('Location_Counts.csv')

    # Extract counts for valid, invalid, and blank locations
    valid_count = counts_data[counts_data['Category'] == 'Valid Locations']['Count'].values[0]
    invalid_count = counts_data[counts_data['Category'] == 'Invalid Locations']['Count'].values[0]
    blank_count = counts_data[counts_data['Category'] == 'Blank Locations']['Count'].values[0]

    counts = [valid_count, blank_count, invalid_count]
    categories = ['Valid', 'Not Shared', 'Invalid']

    # Sort counts and categories in descending order
    counts, categories = zip(*sorted(zip(counts, categories), reverse=True))

    total_count = sum(counts)
    percentages = [count / total_count * 100 for count in counts]

    # Create a bar chart with counts inside the bars
    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, counts, color=['green', 'orange', 'red'])

    for bar, count, percent in zip(bars, counts, percentages):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, f'({percent:.1f}%)', ha='center', va='center')

    plt.title('Location verification')
    plt.xlabel('')
    plt.ylabel('Counts')

    # Create a new frame to embed the chart
    chart_frame = tk.Frame(right_frame)
    chart_frame.pack(fill=tk.BOTH, expand=True)

    # Embed the matplotlib chart in the Tkinter frame
    canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def display_buttons():
    # Create buttons for Chart, Map, and Data
    chart_button = tk.Button(right_frame, text="Geographical Data Integrity Chart", command=valid_invalid_notshared, bg="skyblue", fg="white", font=("Arial", 14, "bold"))
    chart_button.pack(fill=tk.X, padx=10, pady=5)

    map_button = tk.Button(right_frame, text="Tweet Heatmap", command=display_map, bg="salmon", fg="white", font=("Arial", 14, "bold"))
    map_button.pack(fill=tk.X, padx=10, pady=5)

    data_button = tk.Button(right_frame, text="Preprocessed Data", command=lambda: load_csv_data('Twitter_Account_info_preprocess.csv'), bg="lightgreen", fg="black", font=("Arial", 14, "bold"))
    data_button.pack(fill=tk.X, padx=10, pady=5)

def analyze_sentiment(csv_file):
    clear_content()
    display_buttons_textprocess()
    # Check if sentiment_counts_per_profile.csv already exists
    if os.path.exists('total_sentiment_counts.csv'):
        display_total_sentiment_pie_chart()
        return

    # Load the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

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

    # Calculate total counts of positive, negative, and neutral sentiments among all records
    total_counts = sentiment_counts.sum()

    # Create a DataFrame for total counts
    total_sentiments = pd.DataFrame({
        'Sentiment': ['Positive', 'Negative', 'Neutral'],
        'Total Count': total_counts
    })

    # Save the total counts to a new CSV file
    total_sentiments.to_csv('total_sentiment_counts.csv', index=False)
    display_total_sentiment_pie_chart()

def display_total_sentiment_pie_chart():
    try:
        total_sentiments = pd.read_csv('total_sentiment_counts.csv')
        
        # Plot a pie chart for the total sentiment distribution
        plt.figure(figsize=(6, 6))
        total_sentiments.set_index('Sentiment')['Total Count'].plot(kind='pie', autopct='%1.1f%%', startangle=140)
        plt.title('Total Sentiment Analysis')
        plt.axis('equal')

        # Create a new frame to embed the chart
        chart_frame = tk.Frame(right_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True)

        # Embed the matplotlib chart in the Tkinter frame
        canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    except FileNotFoundError:
        messagebox.showerror("Error", "total_sentiment_counts.csv not found")

def tweet_category_preprocess():
    # Dictionary of keywords for different categories
    keywords = {
        'politics': ['government', 'vote', 'election', 'policy', 'Prime Minister', 'president', 'parliament','economic','public affairs','activism','Republicans','Democrats','war','legislation', 'justice'],
        'entertainment': ['Happy','fashion','movie', 'author', 'paparazzi','red carpet','music', 'actor', 'actress', 'celebrity', 'performance', 'ceremony', 'award', 'glad','festival','Netflix','streaming', 'television', 'band'],
        'sports': ['football', 'soccer', 'basketball', 'tennis', 'athlete','cricket', 'play', 'game', 'team','champion','competition','tournament','World Cup', 'league','sports', 'fitness']
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
    display_buttons_textprocess()

def tweet_locationwise_category_chart(file_path):
    clear_content()
    display_buttons_textprocess()
    # Read the data from the CSV file
    data = pd.read_csv(file_path)

    # Get unique locations and categories
    unique_locations = data['Location'].unique()
    unique_categories = data['Category'].unique()

    # Set up color map for categories
    category_colors = plt.get_cmap('tab10')(range(len(unique_categories)))

    # Create a dictionary to map categories to colors
    category_color_dict = dict(zip(unique_categories, category_colors))

    plt.figure(figsize=(12, 8))

    # Iterate through each location
    for idx, location in enumerate(unique_locations):
        location_data = data[data['Location'] == location]

        # Create a bar for each category within the location bar
        category_percentages = []
        for category in unique_categories:
            count = location_data[location_data['Category'] == category]['Count'].sum()
            category_percentages.append(count)

        # Calculate percentage for each category within the location
        total_count = sum(category_percentages)
        category_percentages = [count * 100 / total_count if total_count > 0 else 0 for count in category_percentages]

        # Plotting each category within the location bar
        bar_start = 0
        for i, (count, category) in enumerate(zip(category_percentages, unique_categories)):
            plt.barh(location, count, left=bar_start, color=category_color_dict[category], label=category if idx == 0 else "", edgecolor='grey')
            plt.text(bar_start + count / 2, idx, f'{count:.1f}%', color='white', va='center', ha='center', fontsize=8)
            bar_start += count

    plt.xlabel('Percentage of Tweets')
    plt.ylabel('Location')
    plt.title('Tweet Category Percentage for Different Locations')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    # Create a new frame to embed the chart
    chart_frame = tk.Frame(right_frame)
    chart_frame.pack(fill=tk.BOTH, expand=True)

    # Embed the matplotlib chart in the Tkinter frame
    canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def tweet_category_chart(file_path):
    clear_content()
    display_buttons_textprocess()
    # Read the data from the CSV file
    data = pd.read_csv(file_path)

    # Calculate total count for percentage calculation
    total_count = data['Count'].sum()

    # Plotting
    plt.figure(figsize=(10, 6))
    bars = plt.bar(data['Category'], data['Count'], color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Count of Tweets')
    plt.title('Tweet Count per Category')
    plt.xticks(rotation=45, ha='right')  # Rotating x labels for better readability

    # Display percentages on top of bars
    for bar in bars:
        height = bar.get_height()
        percentage = (height / total_count) * 100
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{percentage:.1f}%', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()

    # Create a new frame to embed the chart
    chart_frame = tk.Frame(right_frame)
    chart_frame.pack(fill=tk.BOTH, expand=True)

    # Embed the matplotlib chart in the Tkinter frame
    canvas = FigureCanvasTkAgg(plt.gcf(), master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def display_buttons_textprocess():
    sentiment_analysis_button = tk.Button(right_frame, text="Sentiment Analysis", command=lambda: analyze_sentiment('Tweets.csv'), bg="lightblue", fg="black", font=("Arial", 12, "bold"))
    sentiment_analysis_button.pack(fill=tk.X, padx=10, pady=5)

    category_chart_button = tk.Button(right_frame, text="Tweet Trends by Category", command=lambda: tweet_category_chart('tweet_count.csv'), bg="lightgreen", fg="black", font=("Arial", 12, "bold"))
    category_chart_button.pack(fill=tk.X, padx=10, pady=5)
    
    locationwise_chart_button = tk.Button(right_frame, text="User Preferences by Location", command=lambda: tweet_locationwise_category_chart('tweet_locationwise_count.csv'), bg="lightcoral", fg="black", font=("Arial", 12, "bold"))
    locationwise_chart_button.pack(fill=tk.X, padx=10, pady=5)

def save_map_and_csv():
    # Load your CSV file into a DataFrame using pandas
    account_data  = pd.read_csv('Twitter_Account_info.csv')
    tweet_data = pd.read_csv('Tweets.csv')

    # Initialize a geolocator from Geopy
    geolocator = Nominatim(user_agent="geoapiEx")

    # Create a label to display preprocessing status
    preprocess_label = tk.Label(right_frame, text="Preprocessing in progress...", font=("Arial", 12))
    preprocess_label.pack(padx=20, pady=20)

    # Refresh the window to display the label
    root.update_idletasks()

    # Create a map centered at a specific location (e.g., coordinates of a city)
    map_center = [40.7128, -74.0060]  # Example: New York City
    mymap = folium.Map(location=map_center, zoom_start=2)

    # Group tweet data by 'Profile' (Location) and get the first tweet for each location
    unique_tweets = tweet_data.groupby('Profile')['Description'].first().reset_index()

    # Initialize counters for valid, invalid, and blank locations
    valid_count = 0
    invalid_count = 0
    blank_count = 0

    valid_rows = []
    latitudes = []
    longitudes = []

    # Create a dictionary to store one tweet per location from Twitter_Account_info.csv
    location_tweets = {}
    for index, row in tweet_data.iterrows():
        profile = row['Profile']
        description = row['Description']
        if profile not in location_tweets:
            location_tweets[profile] = description

    # Iterate through the DataFrame, geocode locations, and add markers for each location
    for index, row in account_data.iterrows():
        location = row['Location']
        profilename=row['Profile']

        # Check if location data is not empty or NaN
        if pd.notnull(location) and location.strip() != '':
            try:
                # Geocode the location using the geolocator
                if location == 'Bangladesh':
                    latitude = 23.6850
                    longitude = -90.3563
                else:
                    geocode = geolocator.geocode(location)
                    if geocode:
                        latitude = geocode.latitude
                        longitude = geocode.longitude
                    else:
                        invalid_count += 1  # Increment invalid count
                        continue

                latitudes.append(latitude)
                longitudes.append(longitude)

                # Get the profile information for the location
                profile_info = row  # This contains the profile data

                # Get the tweet for that location from Twitter_Account_info.csv
                tweet_for_location = location_tweets.get(profilename, '')

                # Modify the popup text to include profile info and the tweet
                popup_text = f"Location: {location} |User: {profilename} | Tweet: {tweet_for_location}"
                popup = folium.Popup(popup_text, parse_html=True)
                marker = folium.Marker(location=[latitude, longitude], popup=popup)
                marker.add_to(mymap)

                valid_count += 1  # Increment valid count
                valid_rows.append(row)
            except Exception as e:
                print(f"Error geocoding '{location}': {e}")
        else:
            blank_count += 1  # Increment blank count

    # Create a DataFrame with valid rows for the new CSV file
    valid_data = pd.DataFrame(valid_rows)
    
    if not os.path.exists('Twitter_Account_info_preprocess.csv'):
        # Save processed data to a new CSV file with the same format as Twitter_Account_info.csv
        valid_data.to_csv('Twitter_Account_info_preprocess.csv', index=False)
    
    if not os.path.exists('map_with_bold_location.html'):
        # Save the map to an HTML file
        mymap.save('map_with_bold_location.html')

    # Create a DataFrame with counts of valid, invalid, and blank locations
    counts_data = pd.DataFrame({
        'Category': ['Valid Locations', 'Invalid Locations', 'Blank Locations'],
        'Count': [valid_count, invalid_count, blank_count]
    })

    # Save counts data to a new CSV file
    counts_data.to_csv('Location_Counts.csv', index=False)

    # Once preprocessing is complete:
    preprocess_label.config(text="Preprocessing complete!")

    # Display buttons or perform any further actions as needed
    display_buttons()

   
def text_process():
    clear_content()

    # Create a label to display preprocessing status
    status_label = tk.Label(right_frame, text="Tweet Analysis in progess", font=("Arial", 20,"bold"))
    status_label.pack(padx=20, pady=20)

    # Schedule the data extraction after 15 seconds
    left_frame.after(5000, Tweet_Analysis)

def Tweet_Analysis():
    clear_content()
    status_label = tk.Label(right_frame, text="Tweet Analysis completed", fg="green", font=("Arial", 14, "bold"))
    status_label.pack(padx=20, pady=20)

    if os.path.exists('tweet_location.csv'):
        display_buttons_textprocess()
    else:
        tweet_category_preprocess()

def close_window():
    root.destroy()

def display_boxes():
    # Display boxes below the status label
    box1 = tk.Label(right_frame, text="Sentiment Analysis", bg="skyblue", fg="white", width=60, height=5, font=("Arial", 25, "bold"))
    box1.pack(side=tk.TOP, padx=5, pady=5)

    box2 = tk.Label(right_frame, text="Entity Recognition", bg="salmon", fg="white", width=60, height=5, font=("Arial", 25, "bold"))
    box2.pack(side=tk.TOP, padx=5, pady=5)

    box3 = tk.Label(right_frame, text="Keyword Extraction", bg="darkseagreen", fg="white", width=60, height=5, font=("Arial", 25, "bold"))
    box3.pack(side=tk.TOP, padx=5, pady=5)

def clear_content():
    # Destroy all widgets in the right frame
    for widget in right_frame.winfo_children():
        widget.destroy()
root = tk.Tk()

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def on_escape(event=None):
    root.attributes("-fullscreen", False)

# Set the initial size of the window
initial_width = 1000
initial_height = 800
root.geometry(f"{initial_width}x{initial_height}")

# Bind the F11 key to toggle fullscreen
root.bind("<F11>", toggle_fullscreen)
# Bind the Escape key to exit fullscreen
root.bind("<Escape>", on_escape)

root.title("Course Project : Immersive Analytics Apps")

# Header
header = tk.Frame(root, bg='green', height=50)
header.pack(fill=tk.X)

# Create a label inside the frame
header_label = tk.Label(header, text="Analyzing location-based tweets towards soft biometrics", fg='white', font=('Arial', 14, 'bold'), bg="green")
header_label.pack(pady=10)

# close_button = tk.Button(header, text="X", command=close_window, font=("Arial", 10))
# close_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Left division for menu buttons
left_frame = tk.Frame(root, width=200, bg="lightgrey")
left_frame.pack_propagate(False)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

data_extract_button = tk.Button(left_frame, text="Data Extraction", command=data_extract, font=("Arial", 12, ""))
data_extract_button.pack(fill=tk.X, padx=10, pady=5)

data_preprocess_button = tk.Button(left_frame, text="Preprocessing", command=data_preprocess, font=("Arial", 12, ""))
data_preprocess_button.pack(fill=tk.X, padx=10, pady=5)

text_process_button = tk.Button(left_frame, text="Text Analysis", command=text_process, font=("Arial", 12, ""))
text_process_button.pack(fill=tk.X, padx=10, pady=5)

location_wise_tweet_button = tk.Button(left_frame, text="Tweeting Users", command=location_wise_tweet, font=("Arial", 12, ""))
location_wise_tweet_button.pack(fill=tk.X, padx=10, pady=5)

#display_map_button = tk.Button(left_frame, text="Map", command=display_map, bg="blue", fg="white", font=("Arial", 12, "bold"))
#display_map_button.pack(fill=tk.X, padx=10, pady=5)

# Right division for content/message
right_frame = tk.Frame(root, bg="white")
right_frame.pack(fill=tk.BOTH, expand=True)

status_label = tk.Label(right_frame, text="", font=("Arial", 12))
status_label.pack(padx=5, pady=5)

# Footer
footer = tk.Frame(root, bg='gray', height=30)
footer.pack(fill=tk.X)

root.mainloop()