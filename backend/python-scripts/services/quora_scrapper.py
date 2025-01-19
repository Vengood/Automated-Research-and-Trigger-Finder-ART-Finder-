from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

def extract_quora_data(input_query):
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    query = input_query.replace(" ", "-")
    URL = f"https://www.quora.com/{query}"

    wd = webdriver.Chrome(options=options)

    try:
        wd.get(URL)

        # Dynamically scroll to load content
        last_count = 0
        while True:
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            current_count = len(wd.find_elements(By.CSS_SELECTOR, 'div.q-box.qu-mb--tiny'))
            if current_count == last_count:
                break
            last_count = current_count

        # Extract answers
        answer_elements = wd.find_elements(By.CSS_SELECTOR, 'div.q-box.qu-mb--tiny')
        paragraphs = [
            answer.text.strip()
            for answer in answer_elements[:10]  # Limit to 10 answers
            if "Continue Reading" not in answer.text
        ]

        # Prepare the data
        extracted_data = "\n\n".join(paragraphs)
        astra_data = {"query": input_query, "url": URL, "content": extracted_data}

        return json.dumps(astra_data, indent=4)

    finally:
        wd.quit()

# Test the function
# input_query = "beauty products"
# response_json = extract_quora_data(input_query)
# print(response_json)
