# SAMOSA

<p align="center">
    <img src="logo.png" alt="SAMOSA Logo" width="180">
</p>

SAMOSA stands for Sentiment Analysis Model On Scraped Articles.

SAMOSA is a Streamlit app for analyzing sentiment from text and scraped content. It calculates polarity scores and classifies text into positive, negative, or neutral categories.

## Features

- Analyze direct text input
- Scrape YouTube comments and analyze sentiment
- Upload CSV files and analyze text columns
- Visualize sentiment distribution with charts
- Download processed results as CSV

## Project Structure

- senti.py: main Streamlit application
- requirements.txt: Python dependencies
- logo.png and bg.jpg: UI assets
- Example.py, Twitter bot.py, 0.py, 1.py, 2.py, login.html, style.css: older/experimental files

If you only need the working SAMOSA app, run senti.py.

## Project Requirements

### Software Requirements
- Python 3.9 or newer (recommended)
- Google Chrome installed (required for Selenium)
- Internet connection (needed for scraping, NLTK data download, and ChromeDriver setup)

### Python Dependencies
Install from requirements.txt:
- streamlit
- pandas
- nltk
- textblob
- plotly
- selenium
- webdriver-manager
- pillow
- tweet-preprocessor

## Quick Start (Windows PowerShell)

1. Open PowerShell in the project folder.
2. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the Streamlit app:

```powershell
streamlit run senti.py
```

5. Open the local URL shown in terminal (usually http://localhost:8501).

## How to Use

### 1. Analyze Text
- Expand Analyze Text
- Enter any sentence or paragraph
- View polarity score and sentiment label (positive/negative/neutral)

### 2. Analyze by Scraping YouTube
- Expand Analyze by scraping a youtube video
- Paste a YouTube video URL
- Wait for scraping and processing
- Review sample output table and chart
- Download the analyzed CSV if needed

### 3. Analyze Uploaded CSV
- Expand Analyze an Excel sheet(Upload it in a CSV Format)
- Upload a CSV file containing text data
- The app identifies text-like columns and computes sentiment
- View results and download analyzed CSV

## Notes

- On first run, NLTK resources are downloaded automatically inside the app.
- Selenium uses webdriver-manager to fetch a compatible ChromeDriver.
- Scraping-heavy analysis may take longer depending on page size and internet speed.

## Troubleshooting

### Streamlit command not found
Use:

```powershell
python -m streamlit run senti.py
```

### Selenium/Chrome issues
- Make sure Google Chrome is installed and updated
- Re-run after internet is stable so webdriver-manager can fetch the driver

### NLTK errors
If any tokenizer/corpus error appears, install/download manually:

```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```
