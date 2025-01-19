import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from wordcloud import WordCloud, STOPWORDS
from transformers import pipeline
import json
# Importing custom scraper functions
from services.google_scrapper import serp_scrapper
from services.quora_scrapper import extract_quora_data
from services.reddit_scrapper import search_reddit_for_query
from services.youtube_scrapper import get_video_links

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Configure Google Gemini API
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Hugging Face Sentiment Analysis Pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Flask App
app = Flask(__name__)

# Function to generate word cloud image
def generate_word_cloud(text, topic):
    try:
        stopwords = set(STOPWORDS)
        wordcloud = WordCloud(width=800, height=400, background_color="white", stopwords=stopwords).generate(text)
        filename = f"{topic.replace(' ', '_')}_wordcloud.png"
        filepath = os.path.join("static", filename)
        wordcloud.to_file(filepath)
        return filepath
    except Exception as e:
        logging.error(f"Error generating word cloud: {e}")
        return None

# Function to analyze sentiment using Hugging Face
def analyze_sentiment(texts):
    sentiments = {"positive": 0, "negative": 0, "neutral": 0}
    try:
        for text in texts:
            result = sentiment_analyzer(text[:512])[0]  # Limit text to 512 characters
            label = result["label"]
            if label == "POSITIVE":
                sentiments["positive"] += 1
            elif label == "NEGATIVE":
                sentiments["negative"] += 1
            else:
                sentiments["neutral"] += 1
    except Exception as e:
        logging.error(f"Error analyzing sentiment: {e}")
    return sentiments

def analyze_with_gemini(content, topic):
    """
    Analyze content using Gemini with specific prompts for different insight types.
    """
    try:
        # Prepare the structured prompt
        analysis_prompt = f"""
        Analyze the following content about {topic} and provide insights in JSON format:
        just dont add that "```json" at start  and "```" at end
        {{
            "pain_points": [],
            "triggers": [],
            "best_hooks": [],
            "best_ctas": []
        }}
        """
        
        # Call the Gemini API
        response = gemini_model.generate_content(analysis_prompt)
        if not response or not response.text:
            logging.error("No response from Gemini API.")
            return {"pain_points": [], "triggers": [], "best_hooks": [], "best_ctas": []}

        # Parse the response directly as JSON
        raw_text = response.text.strip('`')
        if raw_text.startswith('json'): raw_text = raw_text[4:].strip()
        logging.debug(f"Raw response from Gemini: {raw_text}")

        # Load JSON directly without regex-based extraction
        sections = json.loads(raw_text)
        print("The sections are : \n",sections)
        # Validate and format the response
        return {
            "pain_points": sections.get("pain_points", []),
            "triggers": sections.get("triggers", []),
            "best_hooks": sections.get("best_hooks", []),
            "best_ctas": sections.get("best_ctas", []),
        }

    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {str(e)}")
        logging.error(f"Problematic JSON: {response.text if response else 'No response'}")
        return {"pain_points": [], "triggers": [], "best_hooks": [], "best_ctas": []}
    except Exception as e:
        logging.error(f"Error analyzing content with Gemini: {str(e)}")
        return {"pain_points": [], "triggers": [], "best_hooks": [], "best_ctas": []}


# Function to run scrapers sequentially and collect insights
def run_scrapers_and_summarize(topic):
    # Initialize the structure to store all insights
    combined_insights = {
        "pain_points": [],
        "triggers": [],
        "best_hooks": [],
        "best_ctas": [],
        "YT_LINKS": [],
        "sentiment": {"positive": 0, "negative": 0, "neutral": 0},
        "word_cloud": ""
    }

    try:
        logging.info(f"Running scrapers for topic: {topic}")

        # Define the scrapers to run
        scrapers = [
            ("SERP", serp_scrapper),
            ("Quora", extract_quora_data),
            ("Reddit", search_reddit_for_query),
            ("YouTube Links", get_video_links)
        ]

        # Initialize containers for collected data
        all_text_data = []  # For sentiment analysis and word cloud
        combined_analysis_text = ""  # For Gemini analysis

        # Run each scraper sequentially
        for name, scraper_func in scrapers:
            logging.debug(f"Running {name} scraper...")
            try:
                # Get data from current scraper
                data = scraper_func(topic)
                if not data:
                    continue

                # Process the scraped data
                if isinstance(data, str):
                    all_text_data.append(data)
                    combined_analysis_text += f"\n{name} Data:\n{data}"
                elif isinstance(data, list):
                    all_text_data.extend(data)
                    combined_analysis_text += f"\n{name} Data:\n" + "\n".join(data)

                # Handle YouTube links separately
                if name == "YouTube Links":
                    combined_insights["YT_LINKS"].extend(data)

            except Exception as scraper_error:
                logging.error(f"Error running {name} scraper: {scraper_error}")

        # Process collected data
        if combined_analysis_text:
            # Get insights from Gemini
            analysis_results = analyze_with_gemini(combined_analysis_text, topic)
            # Append Gemini insights to respective fields
            combined_insights["pain_points"].extend(analysis_results.get("pain_points", []))
            combined_insights["triggers"].extend(analysis_results.get("triggers", []))
            combined_insights["best_hooks"].extend(analysis_results.get("best_hooks", []))
            combined_insights["best_ctas"].extend(analysis_results.get("best_ctas", []))


        if all_text_data:
            # Perform sentiment analysis
            combined_insights["sentiment"] = analyze_sentiment(all_text_data)

            # Generate word cloud
            combined_text = " ".join(all_text_data)
            word_cloud_path = generate_word_cloud(combined_text, topic)
            if word_cloud_path:
                combined_insights["word_cloud"] = word_cloud_path

    except Exception as e:
        logging.error(f"Error during scraping or summarizing: {e}")

    return combined_insights

# API Endpoint
@app.route("/generate_insights", methods=["POST"])
def generate_insights():
    try:
        # Get user query from the frontend
        user_request = request.json
        topic = user_request.get("topic", "")
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        # Run scrapers and summarize insights
        insights = run_scrapers_and_summarize(topic)

        # Respond with the generated insights
        return jsonify({"message": "Insights generated successfully", "insights": insights}), 200
    except Exception as e:
        logging.error(f"Error in generating insights: {e}")
        return jsonify({"error": str(e)}), 500

# Run Flask App
if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)  # Ensure static directory exists for word cloud images
    app.run(host="0.0.0.0", port=5001)
