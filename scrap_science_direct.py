from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Selenium WebDriver (you'll need to download a browser driver like ChromeDriver)
driver = webdriver.Chrome(executable_path='path_to_chromedriver')  # Make sure to replace this with the correct path

# Open ScienceDirect search page
driver.get("https://www.sciencedirect.com/search")

# Find the search input element and enter the query
search_input = driver.find_element(By.NAME, 'qs')
search_input.send_keys('"machine learning" AND "potential evapotranspiration"')

# Submit the form (this may vary depending on how the form is structured)
search_input.submit()

# Wait for results to load
time.sleep(5)  # Give time for the results to load

# Scrape the result links
articles = driver.find_elements(By.CSS_SELECTOR, '.ResultItem')
for article in articles:
    title = article.find_element(By.CSS_SELECTOR, '.result-list-title-link').text
    link = article.find_element(By.CSS_SELECTOR, '.result-list-title-link').get_attribute('href')
    print(f"Title: {title}")
    print(f"Link: {link}")

# Close the browser
driver.quit()