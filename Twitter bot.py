import base64
import requests
from bs4 import BeautifulSoup
import pandas as pd
import preprocessor as p
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import matplotlib.pyplot as plt
from textblob import TextBlob
import seaborn as sns
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="S.A.M.O.S.A", layout="wide")

with st.container():
    st.header('S.A.M.O.S.A')
    st.write("Sentiment Analysis Model On Scraped Articles!")


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


set_background('./bg.jpg')

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

def plot(df):
    senti = ['positive', 'negative', 'neutral']
    count = [df['sentiment'].value_counts().get('positive', 0), df['sentiment'].value_counts().get('negative', 0),
             df['sentiment'].value_counts().get('neutral', 0)]

    chart_selection_counter = 0
    chart = st.radio("Select the chart in which you want to see your analysis: ",
                     ('Line Chart', 'Bar Chart', 'Pie Chart'), key=f"chart_option_{chart_selection_counter}")

    plot_val = pd.Series(data=count, index=senti)

    if chart == 'Line Chart':
        fig = px.line(plot_val, x=plot_val.index, y=count)
        st.plotly_chart(fig)

    elif chart == 'Bar Chart':
        fig = px.bar(plot_val, x=plot_val.index, y=count)
        st.plotly_chart(fig)

    elif chart == 'Pie Chart':
        fig = px.pie(values=count, names=senti)
        st.plotly_chart(fig)


with st.expander('Analyze Text'):
    text = st.text_input('Enter the Text here:')
    if text:
        st.write('Score(Polarity): ', score(text))
        st.write('Sentiment: ', sentiment_analyzer(text))

with st.expander('Analyze by scraping a website '):
    url = st.text_input('Enter the url of the website here:')
    if url:
        pages = 5
        page_size = 1000

        reviews = []

        for i in range(1, pages + 1):
            # st.write(f"Scraping page {i}")

            page_url = f"{url}/page/{i}/?sortby=post_date%3ADesc&pagesize={page_size}"

            response = requests.get(page_url)

            content = response.content
            parsed_content = BeautifulSoup(content, 'html.parser')
            for para in parsed_content.find_all("div", {"class": "text_content"}):
                reviews.append(para.get_text())

        st.write(f"   ---> {len(reviews)} total reviews")

        review_data = pd.DataFrame(data=reviews, columns=['Reviews'])
        review_data['clean_reviews'] = review_data['Reviews'].apply(lambda x: p.clean(str(x)))

        review_data['clean_reviews'] = review_data['clean_reviews'].apply(clean_verified)

        review_data['clean_reviews'] = review_data['clean_reviews'].apply(punctuation_removal)

        lemmatizer = nltk.stem.WordNetLemmatizer()

        def lemmatize_text(text):
            return [(lemmatizer.lemmatize(w)) for w in word_tokenize(text)]

        review_data['tokenized_reviews'] = review_data['clean_reviews'].apply(lemmatize_text)
        review_data['tokenized_reviews'] = review_data['tokenized_reviews'].apply(
            lambda x: [item for item in x if item not in stop_words])
        review_data['tokenized_reviews'] = review_data['tokenized_reviews'].apply(lambda x: ' '.join(x))

        review_data['score'] = review_data['clean_reviews'].apply(score)
        review_data['sentiment'] = review_data['clean_reviews'].apply(sentiment_analyzer)
        st.subheader('The Result of the Analysis is:')
        st.write(review_data[['Reviews', 'score', 'sentiment']].head(10))
        plot(review_data)


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

        plot(df)
