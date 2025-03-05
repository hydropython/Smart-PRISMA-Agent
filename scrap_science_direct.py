from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize WebDriver using ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# List of queries for ScienceDirect search
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

# Open ScienceDirect
driver.get("https://www.sciencedirect.com/")

# Wait for the page to load completely (longer timeout and check for a different element)
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '//input[@id="search-field"]'))  # Search field is used to check page load
)

# Ensure the page is fully loaded
if driver.execute_script("return document.readyState;") == "complete":
    print("Page loaded successfully!")
else:
    print("Page failed to load.")

# Function to perform search for a given query
def perform_search(query, start_year, end_year):
    # Find the search input box and enter the query
    search_box = driver.find_element(By.XPATH, '//input[@id="search-field"]')
    search_box.clear()  # Clear any previous searches
    search_box.send_keys(query)
    
    # Submit the search form (simulated by pressing the enter key)
    search_box.submit()

    # Wait for the search results to load
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "result-list")]'))  # Results list is loaded
    )

    # Optionally, handle date filtering (if it's available or needed)
    try:
        # Wait for the "Custom Date Range" option to appear
        date_range_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="search-custom-range"]'))
        )
        date_range_button.click()

        # Select the start year
        start_year_input = driver.find_element(By.XPATH, '//input[@id="search-custom-range-start"]')
        start_year_input.clear()
        start_year_input.send_keys(start_year)

        # Select the end year
        end_year_input = driver.find_element(By.XPATH, '//input[@id="search-custom-range-end"]')
        end_year_input.clear()
        end_year_input.send_keys(end_year)

        # Click Apply
        apply_button = driver.find_element(By.XPATH, '//*[@id="search-custom-range-apply"]')
        apply_button.click()

    except Exception as e:
        print("Date filter not found or failed to apply:", e)
    
    # Wait for results to load with date filter applied
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "result-list")]'))  # Results list is loaded
    )

    # Collect and print the search results
    articles = driver.find_elements(By.XPATH, '//a[contains(@class, "result-title")]')
    for i, article in enumerate(articles, 1):
        print(f"Result {i}: {article.text}")
        print(f"URL: {article.get_attribute('href')}")
        print("=" * 50)

# Loop through the queries and perform search for each
for query, start_year, end_year in queries:
    print(f"Searching for: {query} from {start_year} to {end_year}")
    perform_search(query, start_year, end_year)
    time.sleep(5)  # Add delay to avoid hitting the server too frequently

# Close the driver after all searches
driver.quit()


