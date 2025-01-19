import praw
import json
import os 
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('REDDIT_CLIENTID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = os.getenv('REDDIT_USERAGENT')

# Authenticate with Reddit API
reddit = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent)

def search_reddit_for_query(query, limit=10):
    """
    Search Reddit for posts related to a user-defined query and return data in JSON format.
    
    Args:
        query (str): Search query provided by the user.
        limit (int): Number of posts to fetch.

    Returns:
        str: JSON string containing search results from Reddit.
    """
    try:
        # Perform search in all subreddits with the provided query
        search_results = reddit.subreddit('all').search(query, limit=limit)
        data = []
        
        # Iterate through search results and gather relevant data
        for submission in search_results:
            data.append({
                'title': submission.title,
                'content': submission.selftext,
                'score': submission.score,
                'comments': [comment.body for comment in submission.comments.list()[:10]]  # Limit comments for performance
            })
        
        # Convert the list of data to a formatted JSON string
        return json.dumps(data, indent=4)
    
    except Exception as e:
        # Handle any exceptions and return an error message
        return json.dumps({"error": str(e)}, indent=4)

# Example usage: Allow user to input a query dynamically
# user_query = input("Enter a search query: ")  # The user can input any query they want
# reddit_data = search_reddit_for_query(user_query, limit=5)

# # # Print the scraped data in JSON format
# print(reddit_data)

# Optionally, save the data to a file
# with open(f'{user_query}_reddit_data.json', 'w') as json_file:
#     json_file.write(reddit_data)
