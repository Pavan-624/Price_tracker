import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Load environment variables
env_data = os.getenv('ENV_DATA')

if env_data:
    env_vars = json.loads(env_data)
    print("Loaded environment variables")
else:
    raise ValueError("ENV_DATA is not set or empty")

from_email = env_vars.get('FROM_EMAIL', '')
from_password = env_vars.get('EMAIL_PASSWORD', '')
to_email = env_vars.get('TO_EMAIL', '')

smtp_server = 'smtp.gmail.com'
smtp_port = 587

product = {
    "url": "https://www.amazon.in/Fossil-Analog-Black-Unisex-Watch/dp/B005LBZ6G6",
    "threshold": 150000.0
}

def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")

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

        # Wait for the product title element to be present and fetch it
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.a-size-large.product-title-word-break'))
        )
        product_title = title_element.text.strip()
        print(f"Product Title: {product_title}")

        # Wait for the product price element to be present and fetch it
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.a-price-whole'))
        )
        product_price = price_element.text.strip().replace(',', '')
        print(f"Product Price: {product_price}")

        if product_price != 'N/A':
            try:
                product_price = float(product_price)
                print(f"Fetched Price: {product_price}")

                if product_price <= product["threshold"]:
                    print(f'Price is below threshold for {product_title}: {product_price}')
                    # Send email notification
                    send_email(
                        'Price Drop Alert!',
                        f'The price of {product_title} has dropped to {product_price}.',
                        to_email
                    )
            except ValueError:
                print("Failed to convert price to float.")
        else:
            print("Price data not available.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    fetch_data()
