import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

# Load environment variables
env_data = os.getenv('ENV_DATA')

if env_data:
    env_vars = json.loads(env_data)
    print("Loaded environment variables")
else:
    raise ValueError("ENV_DATA is not set or empty")

product = {
    "url": "https://www.amazon.in/Fossil-Analog-Black-Unisex-Watch/dp/B005LBZ6G6",
    "threshold": 141489.0
}

def fetch_data():
    driver = None
    try:
        firefox_options = Options()
        firefox_options.add_argument("--headless")

        # Define path for GeckoDriver
        geckodriver_path = '/snap/bin/geckodriver'
        service = Service(geckodriver_path)

        # Initialize the Firefox WebDriver
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        delay_time = 10

        driver.get(product["url"])
        time.sleep(delay_time)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        name_tag = soup.find('span', class_='a-size-large product-title-word-break')
        name = name_tag.text.strip() if name_tag else 'N/A'
        print(f"Product Name: {name}")

        price_tag = soup.find('span', class_='a-price-whole')
        price = price_tag.text.strip().replace(',', '') if price_tag else 'N/A'
        print(f"Product Price: {price}")

        if price != 'N/A':
            price = float(price)
            print(f"Fetched Price: {price}")

            if price <= product["threshold"]:
                print(f'Price is below threshold for {name}: {price}')
        else:
            print("Price data not available.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    fetch_data()
