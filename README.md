# SAMOSA

![SAMOSA Logo](logo.png)

SAMOSA stands for Sentiment Analysis Model On Scraped Articles.

This project is a Streamlit-based sentiment analysis tool that can:
- Analyze a single text input
- Scrape comments from a YouTube video URL and classify sentiment
- Analyze uploaded CSV data and classify sentiment row by row
- Show sentiment distribution using charts
- Export analyzed results as a CSV file

## Main App

The primary app entry point is:
- senti.py

## Project Requirements

### Software Requirements
- Python 3.9+ recommended
- Google Chrome installed (required for Selenium scraping)
- Internet connection (for scraping, NLTK data download, and ChromeDriver download)

### Python Dependencies
Install dependencies from requirements.txt:
- streamlit
- pandas
- nltk
- textblob
- plotly
- selenium
- webdriver-manager
- pillow
- tweet-preprocessor

## Setup Instructions (Windows PowerShell)

1. Open PowerShell in the project folder.
2. (Optional but recommended) Create and activate a virtual environment:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

3. Install dependencies:

    pip install -r requirements.txt

4. Run the Streamlit app:

    streamlit run senti.py

5. Open the local URL shown in terminal (usually http://localhost:8501).

## How to Use

### 1) Analyze Text
- Expand Analyze Text
- Enter any sentence or paragraph
- View polarity score and sentiment label (positive/negative/neutral)

### 2) Analyze by Scraping YouTube
- Expand Analyze by scraping a youtube video
- Paste a YouTube video URL
- Wait for scraping and sentiment processing
- Review sample output table and chart
- Download full analyzed CSV if needed

### 3) Analyze Uploaded CSV
- Expand Analyze an Excel sheet(Upload it in a CSV Format)
- Upload a CSV file containing text data
- The app identifies text-like columns and computes sentiment
- View results and download analyzed CSV

## Notes

- On first run, NLTK resources are downloaded automatically inside the app.
- Selenium uses webdriver-manager to fetch a compatible ChromeDriver.
- Scraping-heavy analysis may take longer depending on page size and internet speed.

## Other Files in Repository

Some files appear to be experiments:
- Example.py
- 0.py

If you only want the SAMOSA sentiment app, use senti.py.

## Troubleshooting

### Streamlit command not found
Use:

    python -m streamlit run senti.py

### Selenium/Chrome issues
- Make sure Google Chrome is installed and updated
- Re-run after internet is stable so webdriver-manager can fetch the driver

### NLTK errors
If any tokenizer/corpus error appears, install/download manually:

    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
