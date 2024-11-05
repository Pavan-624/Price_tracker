import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from bs4 import BeautifulSoup


# Load environment variables from variables.env file
dotenv_path = 'F:/pricetracker_project/variables.env'
load_dotenv(dotenv_path=dotenv_path)

from_email = os.getenv('FROM_EMAIL', '')
from_password = os.getenv('EMAIL_PASSWORD', '')

smtp_server = 'smtp.gmail.com'
smtp_port = 587

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

def fetch_data(product_url, threshold_value, recipient_email):
    print(f"Fetching data for {product_url} with threshold {threshold_value} and email {recipient_email}")
    driver = None
    try:
        firefox_options = Options()
        firefox_options.add_argument("--headless")

        # Define path for GeckoDriver
        geckodriver_path = r'C:\Users\Pavan\Downloads\geckodriver-v0.34.0-win64\geckodriver.exe'
        service = Service(geckodriver_path)

        # Initialize the Firefox WebDriver
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        delay_time = 15  # Increase delay time for debugging

        print(f"Navigating to {product_url}")
        driver.get(product_url)
        time.sleep(delay_time)  # Wait for the page to load

        # Get page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract product title
        name_tag = soup.find('span', class_='a-size-large product-title-word-break')
        product_title = name_tag.text.strip() if name_tag else 'N/A'
        print(f"Product Title: {product_title}")

        # Extract product price
        price_tag = soup.find('span', class_='a-price-whole')
        product_price = price_tag.text.strip().replace(',', '') if price_tag else 'N/A'
        print(f"Product Price: {product_price}")

        if product_price != 'N/A':
            try:
                product_price = float(product_price)
                print(f"Fetched Price: {product_price}")

                if product_price <= threshold_value:
                    print(f'Price is below threshold for {product_title}: {product_price}')
                    # Send email notification
                    send_email(
                        'Price Drop Alert!',
                        f'The price of {product_title} has dropped to {product_price}.',
                        recipient_email
                    )
            except ValueError:
                print("Failed to convert price to float.")
        else:
            print("Price data not available or empty.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    # Example usage
    fetch_data('https://www.amazon.in/Fossil-Analog-Black-Unisex-Watch/dp/B005LBZ6G6', 150000.0, 'pavanthatikonda235@gmail.com')
