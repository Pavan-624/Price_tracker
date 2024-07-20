from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json

# Load environment variables
env_data = os.getenv('ENV_DATA')

if env_data:
    secrets = json.loads(env_data)
    print("Loaded environment variables")
else:
    print("ENV_DATA is not set or empty")
    secrets = {}

# Define path for GeckoDriver installed via Snap
geckodriver_path = '/snap/bin/geckodriver'

# Set up Firefox options
options = Options()
options.add_argument('--headless')  # Uncomment if you need headless mode

# Set up Firefox service
service = Service(executable_path=geckodriver_path)

# Initialize Firefox WebDriver
driver = None  # Initialize driver to None

try:
    driver = webdriver.Firefox(service=service, options=options)
    
    # Open the URL
    driver.get('https://www.amazon.in/s?k=iphone+15+pro+max')
    
    # Wait for elements with the class "a-size-medium a-color-base a-text-normal" to appear
    try:
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.a-size-medium.a-color-base.a-text-normal'))
        )
        
        # Print the text of each product element
        for product in product_elements:
            print(product.text)
        
    except Exception as e:
        print(f"Product elements not detected: {e}")
    
    print(driver.title)  # Print the page title to verify it loads correctly

finally:
    if driver:
        driver.quit()
