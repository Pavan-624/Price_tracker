from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os

# Fetch environment variables
from_email = os.getenv('FROM_EMAIL')
from_password = os.getenv('EMAIL_PASSWORD')
to_email = os.getenv('TO_EMAIL')

# SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# URL and threshold for a single product
product = {
    "url": "https://www.amazon.in/Fossil-Analog-Black-Unisex-Watch/dp/B005LBZ6G6",
    "threshold": 141489.0
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
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Add this to avoid detection
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Specify the path to the Chrome binary and ChromeDriver executable
        # Download ChromeDriver from: https://chromedriver.chromium.org/downloads
        # Download Google Chrome from: https://www.google.com/chrome/
        chrome_options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        driver = webdriver.Chrome(service=Service(r'C:\Users\Pavan\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe'), options=chrome_options)

        delay_time = 10  # Fixed delay time in seconds

        # Process a single product
        driver.get(product["url"])
        time.sleep(delay_time)  # Use fixed delay time

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Adjust these selectors based on actual HTML structure
        name_tag = soup.find('span', class_='a-size-large product-title-word-break')
        name = name_tag.text.strip() if name_tag else 'N/A'
        print(f"Product Name: {name}")

        price_tag = soup.find('span', class_='a-price-whole')
        price = price_tag.text.strip().replace(',', '') if price_tag else 'N/A'
        print(f"Product Price: {price}")

        if price != 'N/A':
            price = float(price)
            print(f"Fetched Price: {price}")

            # Always send an email if the price is below the threshold
            if price <= product["threshold"]:
                print(f'Price is below threshold for {name}: {price}')
                send_email(
                    'Price Drop Alert!',
                    f'The price of {name} has dropped to {price}.',
                    to_email
                )
        else:
            print("Price data not available.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    fetch_data()
