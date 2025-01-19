from serpapi import GoogleSearch
import json
import os
from dotenv import load_dotenv

load_dotenv()

SERP_API = os.getenv('SERP_API')

def serp_scrapper(input1):
    params = {
        "engine": "google",
        "q": input1,
        "api_key": SERP_API
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    
    # Extract relevant keys
    filtered_results = []
    for result in organic_results:
        filtered_result = {
            "position": result.get("position"),
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet"),
        }
        filtered_results.append(filtered_result)

    # Convert the filtered results to JSON format
    filtered_results_json = json.dumps(filtered_results, indent=4)
    return filtered_results_json

# Test the function
# input1 = "beauty products"
# res = serp_scrapper(input1)
# print(res)
