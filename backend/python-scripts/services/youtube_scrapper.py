import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables for Gemini API key
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Utility function to extract video ID from URL
def extract_video_id(link):
    if "youtube.com/watch" in link:
        return link.split("v=")[-1].split("&")[0]
    elif "youtube.com/shorts" in link:
        return link.split("/shorts/")[-1]
    else:
        raise ValueError("Unsupported YouTube URL format")

# Function to scrape YouTube video links and optionally their summaries
def get_video_summaries(query, num_videos=5):
    """
    Fetch YouTube video titles, links, and summaries for the given query.

    Args:
        query (str): The search query provided by the user.
        num_videos (int): The number of videos to fetch (default is 5).

    Returns:
        list: A list of dictionaries containing video titles, links, and summaries.
    """
    # Initialize Selenium WebDriver
    search_query = query.replace(" ", "+")
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    results = []

    try:
        wd.get(youtube_url)
        time.sleep(3)

        videos = wd.find_elements(By.CSS_SELECTOR, 'ytd-video-renderer')[:num_videos]
        for video in videos:
            title_element = video.find_element(By.CSS_SELECTOR, 'a#video-title')
            title = title_element.text.strip()
            link = title_element.get_attribute('href')
            
            try:
                video_id = extract_video_id(link)
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([entry['text'] for entry in transcript])
                summary = genai.generate_text(transcript_text).text
            except Exception as e:
                summary = "Summary not available"

            results.append({"title": title, "link": link, "summary": summary})

    finally:
        wd.quit()

    return results

# Function to scrape only YouTube video links
def get_video_links(query, num_videos=5):
    """
    Fetch only YouTube video links for the given query.

    Args:
        query (str): The search query provided by the user.
        num_videos (int): The number of video links to fetch (default is 5).

    Returns:
        list: A list of YouTube video URLs.
    """
    search_query = query.replace(" ", "+")
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    links = []

    try:
        wd.get(youtube_url)
        time.sleep(3)

        videos = wd.find_elements(By.CSS_SELECTOR, 'ytd-video-renderer')[:num_videos]
        for video in videos:
            title_element = video.find_element(By.CSS_SELECTOR, 'a#video-title')
            link = title_element.get_attribute('href')
            links.append(link)

    finally:
        wd.quit()

    return links

# Example Usage
# if __name__ == "__main__":
#     query = "beauty products"
#     print("Fetching video summaries:\n")
#     print(get_video_summaries(query=query))

#     print("\nFetching video links:\n")
#     print(get_video_links(query=query))
