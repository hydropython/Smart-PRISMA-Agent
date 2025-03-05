import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Your API key for the Scraper API (if using Scraper API service)
API_KEY = 'your_api_key_here'
BASE_URL = "https://api.scraperapi.com"

# Function to fetch IEEE Xplore results based on a query
def fetch_ieee_xplore_data(query, start_year, end_year, max_results=10):
    search_url = f"https://ieeexplore.ieee.org/rest/search?queryText={query}&minYear={start_year}&maxYear={end_year}&count={max_results}"
    
    params = {
        'api_key': API_KEY,
        'url': search_url
    }
    
    # Make request to Scraper API to fetch IEEE Xplore content
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()  # This returns the JSON response, which you can parse
    else:
        print("Request failed with status code:", response.status_code)
        return None

# Parse IEEE Xplore search results
def parse_ieee_results(results):
    papers = []
    for result in results.get('records', []):
        paper = {
            'title': result.get('article_title', ''),
            'authors': result.get('authors', ''),
            'abstract': result.get('abstract', ''),
            'doi': result.get('doi', ''),
            'publication_year': result.get('publication_year', ''),
            'journal': result.get('publication_name', ''),
            'url': f"https://ieeexplore.ieee.org/document/{result.get('document_id', '')}"
        }
        papers.append(paper)
    return papers

# Main function to handle the scraping
def scrape_ieee_xplore(query, start_year, end_year, max_results=10):
    ieee_results = fetch_ieee_xplore_data(query, start_year, end_year, max_results)
    if ieee_results:
        papers = parse_ieee_results(ieee_results)
        # Convert the list of papers to a DataFrame for better display/analysis
        df = pd.DataFrame(papers)
        return df
    else:
        return pd.DataFrame()

# Example query: "machine learning evapotranspiration"
queries = [
    ('"machine learning" AND "potential evapotranspiration"', '2015', '2024'),
    ('"machine learning" AND "PE" AND "evapotranspiration"', '2015', '2024'),
    ('"deep learning" AND "evapotranspiration" AND "climate" AND "water resources"', '2015', '2024'),
    ('"neural networks" AND "potential evapotranspiration"', '2015', '2024'),
    ('"decision trees" AND "evapotranspiration predictions"', '2015', '2024'),
    ('"support vector machine" AND "evapotranspiration forecasting"', '2015', '2024'),
    ('"Potential Evapotranspiration" AND "Machine Learning"', '2015', '2024'),
    ('"Lake Evapotranspiration" AND "Machine Learning"', '2015', '2024'),
    ('"Reference Evapotranspiration" AND "Machine Learning"', '2015', '2024'),
    ('"machine learning" AND "evaporation"', '2015', '2024'),
    ('"machine learning" AND "evaporation" AND "prediction"', '2015', '2024'),
    ('"machine learning" AND "evaporation" AND "modeling"', '2015', '2024'),
    ('"machine learning" AND "evaporation" AND "forecasting"', '2015', '2024'),
    ('"neural networks" AND "evaporation"', '2015', '2024'),
    ('"neural networks" AND "evaporation" AND "prediction"', '2015', '2024'),
    ('"deep learning" AND "evaporation"', '2015', '2024'),
    ('"deep learning" AND "evaporation" AND "prediction"', '2015', '2024'),
    ('"deep learning" AND "machine learning" AND "evaporation"', '2015', '2024')
]
start_year = 2015
end_year = 2024

# Scrape IEEE Xplore data
papers_df = scrape_ieee_xplore(query, start_year, end_year)

# Save the results to a CSV file
if not papers_df.empty:
    papers_df.to_csv('ieee_xplore_results.csv', index=False)
    print("Results successfully saved to ieee_xplore_results.csv")
else:
    print("No results found.")