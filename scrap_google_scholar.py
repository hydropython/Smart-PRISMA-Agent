import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import time
import random

# ✅ Set up your ScraperAPI key (replace with your actual API key)
SCRAPERAPI_KEY = "########"  # Get from https://www.scraperapi.com/

# Function to scrape Google Scholar using ScraperAPI
def scrape_google_scholar(query):
    """Scrape Google Scholar search results using ScraperAPI"""
    
    # Convert query into a Google Scholar URL
    search_url = f"https://scholar.google.com/scholar?q={query}"
    
    # ✅ Use ScraperAPI (no proxy needed)
    api_url = f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url={search_url}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # ✅ Implement retries in case of failures
    for attempt in range(3):
        try:
            # ✅ Send request through ScraperAPI
            response = requests.get(api_url, headers=headers, timeout=50) 
            
            if response.status_code == 200:
                break  # Success, exit retry loop
            else:
                print(f"Attempt {attempt+1}: Failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1}: Request error - {e}")
        
        time.sleep(random.uniform(2, 5))  # Wait before retrying
    
    # ✅ Parse the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    # ✅ Extract paper details
    for item in soup.find_all('div', class_='gs_ri'):
        title = item.find('h3').text if item.find('h3') else "N/A"
        link = item.find('a')['href'] if item.find('a') else "N/A"
        abstract = item.find('div', class_='gs_rs').text if item.find('div', class_='gs_rs') else "N/A"
        citation_count = "0"

        # ✅ Try extracting citation count safely
        citation_div = item.find('div', class_='gs_fl')
        if citation_div:
            links = citation_div.find_all('a')
            if len(links) > 2 and "Cited" in links[2].text:
                citation_count = links[2].text.split()[-1]  # Extract number

        authors, year, journal, publisher = "N/A", "N/A", "N/A", "N/A"
        if item.find('div', class_='gs_a'):
            gs_a_text = item.find('div', class_='gs_a').text.strip()
            split_text = gs_a_text.split('-')

            if len(split_text) > 2:
                try:
                    publisher_year = split_text[-2].strip()
                    year = publisher_year.split(' ')[-1].strip()
                    journal = publisher_year.replace(year, '').strip()
                    publisher = split_text[-3].strip()
                except IndexError:
                    pass

        results.append({
            'title': title,
            'link': link,
            'abstract': abstract,
            'citation_count': citation_count,
            'authors': authors,
            'year': year,
            'journal': journal,
            'publisher': publisher
        })

    return results

# Function to save results to CSV
def save_results_to_csv(results, filename="scholar_results.csv"):
    if not results:
        print("No data to save!")
        return
    
    keys = results[0].keys()
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Results successfully saved to {filename}")

# Function to save results to SQLite Database
def save_results_to_db(results, db_name="scholar_results.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS papers (
        title TEXT,
        link TEXT,
        abstract TEXT,
        citation_count TEXT,
        authors TEXT,
        year TEXT,
        journal TEXT,
        publisher TEXT
    )''')

    for row in results:
        cursor.execute('''INSERT INTO papers (title, link, abstract, citation_count, authors, year, journal, publisher)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (row['title'], row['link'], row['abstract'], row['citation_count'],
                                                  row['authors'], row['year'], row['journal'], row['publisher']))

    conn.commit()
    conn.close()
    print(f"Results successfully saved to {db_name}")

# ✅ Define queries
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

# ✅ Scrape and save results
all_results = []
for query in queries:
    print(f"Scraping for query: {query}")
    results = scrape_google_scholar(query)
    all_results.extend(results)
    time.sleep(random.uniform(3, 7))  # Avoid rapid requests

# ✅ Choose save option
save_option = input("Choose save option (1: CSV, 2: SQLite): ").strip()

if save_option == '1':
    save_results_to_csv(all_results)
elif save_option == '2':
    save_results_to_db(all_results)
else:
    print("Invalid option chosen. Exiting.")


