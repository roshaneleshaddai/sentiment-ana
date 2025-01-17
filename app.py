from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Define piracy-related keywords
PIRACY_KEYWORDS = ["torrent", "pirated", "illegal download", "crack", "warez", "bootleg","piracy","movierulz","tamilrockers","torrentz2","1337x","yts","yify","eztv","limetorrents","thepiratebay","rarbg","kickass","extratorrent","torrentdownloads","torrentfunk","torrentproject","torrentbit","torrentreactor","torrentz","torrents","torrentz2","torrentday","torrenting"]
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_youtube_comments(video_url):
    """Scrape comments dynamically rendered on a YouTube video."""
    driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
    driver.get(video_url)

    # Wait for comments section to load
    time.sleep(5)  # Adjust the sleep time as needed

    # Scroll to load more comments
    for _ in range(5):  # Adjust the range for more comments
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

    # Extract comments
    comment_elements = driver.find_elements(
        By.CSS_SELECTOR, 
        "span.yt-core-attributed-string.yt-core-attributed-string--white-space-pre-wrap"
    )
    comments = [comment.text for comment in comment_elements]
    print(f"Scraped {len(comments)} comments from the YouTube video.")
    driver.quit()
    return comments



def analyze_sentiment(reviews):
    """Classify sentiment as positive, neutral, or negative."""
    try:
        analyzer = SentimentIntensityAnalyzer()
        results = []

        for review in reviews:
            sentiment_score = analyzer.polarity_scores(review)
            print(f"Sentiment score for review: {sentiment_score}")

            if sentiment_score['compound'] >= 0.05:
                sentiment = 'Positive'
            elif sentiment_score['compound'] <= -0.05:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'

            # Check for piracy mentions
            piracy_flag = any(keyword in review.lower() for keyword in PIRACY_KEYWORDS)

            results.append({
                'Review': review,
                'Sentiment': sentiment,
                'Piracy Mention': piracy_flag
            })

        print(f"Sentiment analysis completed for {len(reviews)} reviews.")
        return results

    except Exception as e:
        print(f"Error in analyze_sentiment: {str(e)}")
        raise


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No data received in the request body.")

        url = data.get("url")
        if not url:
            raise ValueError("URL is required in the request.")
        # url is not valid
        if "youtube.com" not in url:
            raise ValueError("Invalid URL. Only YouTube URLs are supported.")
        print(f"Processing URL: {url}")

        # Scrape reviews from the given URL
        print("Scraping reviews...")
        reviews = scrape_youtube_comments(url)

        # Analyze sentiment of the scraped reviews
        print("Analyzing sentiment...")
        results = analyze_sentiment(reviews)

        # Return the analysis results as JSON
        return jsonify(results)

    except ValueError as ve:
        print(f"ValueError: {str(ve)}")
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(debug=True)
