!pip install streamlit pyngrok nltk requests matplotlib
import nltk
nltk.download('vader_lexicon')
%%writefile app.py
import streamlit as st
import requests
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

API_KEY = "eb72cfd132dd28cc12f52af980864d44"

def get_movie_reviews(movie_name):
    search_url = "https://api.themoviedb.org/3/search/movie"
    search_params = {"api_key": API_KEY, "query": movie_name}
    search_res = requests.get(search_url, params=search_params).json()

    if not search_res.get("results"):
        return []

    movie_id = search_res["results"][0]["id"]
    review_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
    reviews = requests.get(review_url, params={"api_key": API_KEY}).json()

    return [r["content"] for r in reviews.get("results", [])]

def analyze_sentiment(reviews):
    positive = negative = neutral = 0

    for review in reviews:
        score = sia.polarity_scores(review)['compound']
        if score >= 0.05:
            positive += 1
        elif score <= -0.05:
            negative += 1
        else:
            neutral += 1

    return positive, negative, neutral

# ---------------- STREAMLIT UI ---------------- #

st.title("🎬 Movie Review Sentiment Analysis")
st.write("Sentiment analysis using TMDB reviews & NLTK VADER")

movie_name = st.text_input("Enter movie name")

if st.button("Analyze Sentiment"):
    reviews = get_movie_reviews(movie_name)

    if not reviews:
        st.warning("No reviews found for this movie.")
    else:
        pos, neg, neu = analyze_sentiment(reviews)

        st.subheader("Sentiment Summary")
        st.write("Positive:", pos)
        st.write("Negative:", neg)
        st.write("Neutral:", neu)

        # Pie chart
        fig1, ax1 = plt.subplots()
        ax1.pie(
            [pos, neg, neu],
            labels=["Positive", "Negative", "Neutral"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax1.set_title("Sentiment Distribution")
        st.pyplot(fig1)

        # Bar chart
        fig2, ax2 = plt.subplots()
        ax2.bar(["Positive", "Negative", "Neutral"], [pos, neg, neu])
        ax2.set_xlabel("Sentiment Type")
        ax2.set_ylabel("Number of Reviews")
        ax2.set_title("Sentiment Count")
        st.pyplot(fig2)
from pyngrok import ngrok

# Set your ngrok authtoken here. You can get one from https://dashboard.ngrok.com/get-started/your-authtoken
ngrok.set_auth_token("38VtgDwaaxY0qvBLCPqZCOkRKEO_6hRexYBigLKLpdaB3bpqS") # Replace 'YOUR_AUTHTOKEN' with your actual authtoken

# Start Streamlit
!streamlit run app.py &>/content/logs.txt &

# Create public URL
public_url = ngrok.connect(8501)
public_url
