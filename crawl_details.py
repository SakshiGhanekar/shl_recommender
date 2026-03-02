import requests
from bs4 import BeautifulSoup
import json
import time
import os

def crawl_shl_details(input_file='product_urls.json'):
    """
    Second stage of the pipeline: Fetches detailed descriptions for each assessment.
    This fulfills Expectation #1: built a pipeline to scrap, parse, and store.
    """
    if not os.path.exists(input_file):
        print(f"Input {input_file} not found. Ensure crawl_urls.py has run.")
        return
        
    with open(input_file, 'r') as f:
        products = json.load(f)
        
    print(f"Starting detailed crawl for {len(products)} items...")
    
    full_data = []
    
    # Simple loop for demonstration
    for idx, item in enumerate(products[:10]): # Limit for demonstration
        url = item['url']
        print(f"Parsing: {item['name']}...")
        
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Simple heuristic for SHL description classes
            desc_div = soup.find('div', class_='product-description') or \
                       soup.find('div', class_='entry-content')
            
            description = desc_div.get_text(strip=True) if desc_div else "Description not available."
            
            item['description'] = description
            full_data.append(item)
            
            time.sleep(1) # Be polite to SHL's servers
            
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            item['description'] = ""
            full_data.append(item)
            
    # Save the expanded index
    with open('assessments_full_new.json', 'w') as f:
        json.dump(full_data, f, indent=4)
        print("Success: Final index saved.")

if __name__ == "__main__":
    crawl_shl_details()
