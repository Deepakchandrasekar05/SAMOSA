import base64
import os
import time
from PIL import Image
import pandas as pd
import preprocessor as p
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import streamlit as st
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="S.A.M.O.S.A", page_icon=os.path.join(_dir, "logo.png"), layout="wide")

img_logo = Image.open(os.path.join(_dir, "logo.png"))

with st.container():
    image_column, right_column = st.columns((1, 2))

    with image_column:
        st.image(img_logo)
    with right_column:
        st.markdown("<div style='display:flex; align-items:center; height:100%; padding-top:80px;'>"
                    "<div><h1 style='font-size:60px; margin:0;'>S.A.M.O.S.A</h1>"
                    "<h2 style='font-size:24px; margin:0;'>Sentiment Analysis Model On Scraped Articles!</h2></div>"
                    "</div>", unsafe_allow_html=True)


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background(os.path.join(_dir, 'bg.jpg'))


def punctuation_removal(text):
    if not isinstance(text, str):
        text = str(text)
    punc = '!()-[]{};:""\,<>./?@#$%^&*_~'
    for char in punc:
        text = text.replace(char, '')
    return text


def clean_verified(review):
    if review.startswith('Trip Verified | '):
        review = review[16:]
    elif review.startswith("Not Verified | "):
        review = review[15:]
    return review


stop_words = set(stopwords.words('english'))


def filter_words(review):
    filtered = []
    for reviews in review:
        word_tokens = word_tokenize(reviews)
        for w in word_tokens:
            if w not in stop_words and w.isalpha():
                filtered.append(w)
    return filtered


def sentiment_analyzer(review):
    if not isinstance(review, str):
        review = str(review)
    sentiment = TextBlob(review)
    score = sentiment.sentiment.polarity
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"


def score(review):
    if not isinstance(review, str):
        review = str(review)
    sentiment = TextBlob(review)
    return sentiment.sentiment.polarity


def plot(df,chart_selection_counter):
    senti = ['positive', 'negative', 'neutral']
    count = [df['sentiment'].value_counts().get('positive', 0), df['sentiment'].value_counts().get('negative', 0),
             df['sentiment'].value_counts().get('neutral', 0)]

    unique_key = f"chart_option_{chart_selection_counter}"
    chart_selection_counter += 1

    chart = st.radio("Select the chart in which you want to see your analysis: ",
                     ('Pie Chart', 'Bar Chart', 'Line Chart'), key=unique_key)

    plot_val = pd.DataFrame({'sentiment': senti, 'count': count})

    if chart == 'Pie Chart':
        fig = px.pie(plot_val, values='count', names='sentiment')
        st.plotly_chart(fig)
    elif chart == 'Bar Chart':
        fig = px.bar(plot_val, x='sentiment', y='count')
        st.plotly_chart(fig)
    elif chart == 'Line Chart':
        fig = px.line(plot_val, x='sentiment', y='count')
        st.plotly_chart(fig)

def download_data(df,key):
    final1 = df.to_csv().encode('utf-8')
    key+=1
    st.download_button(
        label="Download the Data with scores and sentiment",
        data=final1,
        file_name="sentiment.csv",
        key = key
    )


with st.expander('Analyze Text'):
    text = st.text_input('Enter the Text here:')
    if text:
        st.write('Score(Polarity): ', score(text))
        st.write('Sentiment: ', sentiment_analyzer(text))

with st.expander('Analyze by scraping a youtube video '):
    url = st.text_input('Enter the url of the youtube video here:')
    if url:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(url)

        time.sleep(5)

        scroll_pause_time = 2
        num_scrolls = 20
        for _ in range(num_scrolls):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(scroll_pause_time)
        comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

        comments_list = [comment.text for comment in comments]

        reviews_data = pd.DataFrame(comments_list, columns=['Comment'])

        driver.quit()
        text_columns = [col for col in reviews_data.columns if
                        reviews_data[col].dtype == 'object' and (reviews_data[col].str.len() > 10).any()]

        reviews_data.rename(columns={col: 'Reviews' for col in text_columns}, inplace=True)

        reviews_data['Reviews'] = reviews_data['Reviews'].apply(lambda x: str(x).strip())

        reviews_data['clean_reviews'] = reviews_data['Reviews'].apply(lambda x: p.clean(str(x)))

        reviews_data['clean_reviews'] = reviews_data['clean_reviews'].apply(clean_verified)

        reviews_data['clean_reviews'] = reviews_data['clean_reviews'].apply(punctuation_removal)

        lemmatizer = nltk.stem.WordNetLemmatizer()


        def lemmatize_text(text):
            return [(lemmatizer.lemmatize(w)) for w in word_tokenize(text)]


        reviews_data['tokenized_reviews'] = reviews_data['clean_reviews'].apply(lemmatize_text)
        reviews_data['tokenized_reviews'] = reviews_data['tokenized_reviews'].apply(
            lambda x: [item for item in x if item not in stop_words])
        reviews_data['tokenized_reviews'] = reviews_data['tokenized_reviews'].apply(lambda x: ' '.join(x))

        reviews_data['score'] = reviews_data['clean_reviews'].apply(score)
        reviews_data['sentiment'] = reviews_data['clean_reviews'].apply(sentiment_analyzer)
        st.subheader('The Result of the Analysis is:')
        st.write(reviews_data[['Reviews', 'score', 'sentiment']].head(10))
        plot(reviews_data,0)

        download_data(reviews_data,1)

with st.expander('Analyze an Excel sheet(Upload it in a CSV Format)'):
    upload = st.file_uploader('Upload File')

    if upload:
        df = pd.read_csv(upload, encoding='utf-8')

        text_columns = [col for col in df.columns if df[col].dtype == 'object' and (df[col].str.len() > 10).any()]

        df.rename(columns={col: 'Reviews' for col in text_columns}, inplace=True)

        df['Reviews'] = df['Reviews'].apply(lambda x: str(x).strip())
        df['clean_reviews'] = df['Reviews'].apply(lambda x: p.clean(str(x)))

        df['clean_reviews'] = df['clean_reviews'].apply(clean_verified)

        df['clean_reviews'] = df['clean_reviews'].apply(punctuation_removal)

        lemmatizer = nltk.stem.WordNetLemmatizer()


        def lemmatize_text(text):
            return [(lemmatizer.lemmatize(w)) for w in word_tokenize(text)]


        df['tokenized_reviews'] = df['clean_reviews'].apply(lemmatize_text)
        df['tokenized_reviews'] = df['tokenized_reviews'].apply(
            lambda x: [item for item in x if item not in stop_words])
        df['tokenized_reviews'] = df['tokenized_reviews'].apply(lambda x: ' '.join(x))

        df['score'] = df['clean_reviews'].apply(score)
        df['sentiment'] = df['clean_reviews'].apply(sentiment_analyzer)
        st.subheader('The Result of the Analysis is:')
        st.write(df[['Reviews', 'score', 'sentiment']].head(10))

        plot(df,10)
        download_data(df,11)