from dotenv import load_dotenv
import os
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Load environment variables from .env file
dotenv_path = 'F:/pricetracker_project/variables.env'
load_dotenv(dotenv_path=dotenv_path)

# Fetch environment variables
from_email = os.getenv('FROM_EMAIL')
from_password = os.getenv('EMAIL_PASSWORD')
to_email = os.getenv('TO_EMAIL')

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

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

def setup_database():
    try:
        print(f"Connecting to database at {db_host} with user {db_user}")
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = mydb.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                price FLOAT
            )
        ''')
        
        mydb.commit()
        cursor.close()
        mydb.close()
        print("Database setup complete.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

def fetch_data():
    driver = None
    try:
        print(f"Connecting to database at {db_host} with user {db_user}")
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = mydb.cursor()
        
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Add this to avoid detection
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
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

            # Update or insert the product record into the database
            cursor.execute('''
                INSERT INTO product (name, price)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE price = VALUES(price)
            ''', (name, price))
            print(f'Inserted/Updated product: {name} with price {price}')

            mydb.commit()
        else:
            print("Price data not available.")

        cursor.close()
        mydb.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    setup_database()
    fetch_data()
