from flask import Flask, request, jsonify, render_template
import pandas as pd
import re
import os

app = Flask(__name__)

# Load the CSV data
data_file = "Turkuler_data.csv"  # Ensure this file is in the same directory as app.py
form_data = pd.read_csv(data_file)

# Turkish to English character mapping
turkish_to_english = str.maketrans(
    "çğıöşüÇĞİÖŞÜ",
    "cgiosuCGIOSU"
)

def normalize_text(text):
    """Normalize text for Turkish-English compatibility."""
    if not isinstance(text, str):
        return text
    return text.translate(turkish_to_english).lower()

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML file in the templates folder

@app.route('/search', methods=['POST'])
def search():
    # Parse request JSON
    filters = request.json
    style = filters.get('style', "Hepsi")
    artist = filters.get('artist', "Hepsi")
    technique = filters.get('technique', "Hepsi")
    keyword = filters.get('keyword', "").strip()  # Default to empty string
    popularity = filters.get('popularity', "Hepsi")

    # Ensure column names are correct
    column_map = {
        "style": "Tarz",  # Replace with the correct column name for style
        "artist": "Ozan",  # Replace with the correct column name for artist
        "technique": "Teknik",  # Replace with the correct column name for technique
        "popularity": "Populerlik",  # Replace with the correct column name for popularity
        "lyrics": "Sozler (tum kitalar tek hucre icinde)",  # Replace with the correct column name for lyrics
        "name": "Turku Adi"  # Replace with the correct column name for song name
    }

    # Debugging: Print dataset column names
    print("Dataset columns:", form_data.columns)

    # Define relevant columns
    relevant_columns = [
        column_map["name"], column_map["style"], column_map["artist"],
        column_map["technique"], column_map["popularity"], column_map["lyrics"]
    ]

    # Drop extraneous columns and ensure only relevant columns are selected
    form_data_clean = form_data[relevant_columns].dropna(how="all")

    # Check if all filters are "Hepsi" and keyword is empty
    if all([
        style == "Hepsi",
        artist == "Hepsi",
        technique == "Hepsi",
        popularity == "Hepsi",
        not keyword
    ]):
        # If true, return the full dataset without filtering
        results = form_data_clean.copy()
    else:
        # Make a copy of the clean data
        results = form_data_clean.copy()

        # Apply filters only if the value is not "Hepsi"
        if style != "Hepsi":
            results = results[results[column_map["style"]] == style]
        if artist != "Hepsi":
            results = results[results[column_map["artist"]] == artist]
        if technique != "Hepsi":
            results = results[results[column_map["technique"]] == technique]
        if popularity != "Hepsi":
            results = results[results[column_map["popularity"]] == popularity]

        # Debugging: Print intermediate results
        print("After filtering by style:", results.head())
        print("After filtering by artist:", results.head())
        print("After filtering by technique:", results.head())
        print("After filtering by popularity:", results.head())

        # Apply keyword search only if keyword is not empty
        if keyword:
            keyword_normalized = normalize_text(keyword)

            def search_lyrics(row):
                if not isinstance(row, str):  # Ensure row is a string
                    return False
                row_normalized = normalize_text(row)
                return re.search(keyword_normalized, row_normalized) is not None

            # Apply the search to the lyrics column
            results = results[results[column_map["lyrics"]].apply(search_lyrics)]

        # Debugging: Print results after keyword search
        print("After filtering by keyword:", results.head())

    # Convert results to JSON
    if not results.empty:
        results_json = results.to_dict(orient='records')
    else:
        results_json = []  # Return an empty list if no results found

    return jsonify(results_json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

