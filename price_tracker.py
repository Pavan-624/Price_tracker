import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

# Load environment variables
env_data = os.getenv('ENV_DATA')

if env_data:
    env_vars = json.loads(env_data)
    print("Loaded environment variables")
else:
    raise ValueError("ENV_DATA is not set or empty")

product = {
    "url": "https://www.amazon.in/Fossil-Analog-Black-Unisex-Watch/dp/B005LBZ6G6"
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

        print(f"Navigating to {product['url']}")
        driver.get(product["url"])
        time.sleep(delay_time)

        # Get the title of the page
        page_title = driver.title
        print(f"Page Title: {page_title}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    fetch_data()
