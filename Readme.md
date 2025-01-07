💰 Price Tracker System Using Python and Selenium
A Python-based Price Tracker System that monitors product prices on e-commerce websites, compares them against user-defined thresholds, and sends email notifications for price drops. The system leverages web scraping, automation, and Flask for seamless user interaction.

📜 Table of Contents
Abstract
Project Overview
Features
Technologies Used
Workflow
Advantages and Disadvantages
Deployment
Future Enhancements
Contributors
📝 Abstract
The Price Tracker System is designed to track prices of products on e-commerce platforms like Amazon. Users provide product URLs and desired price thresholds. The system continuously monitors these products and sends email alerts when prices drop below the specified thresholds. Key highlights include:

Data Collection and Parsing: Automated scraping of product details and prices.
Threshold Monitoring: Real-time price comparison against user-defined thresholds.
Notification System: Email alerts for price drops.
User-Friendly Web Interface: Interactive platform to manage tracked products.
🌟 Project Overview
The Price Tracker System addresses the challenge of monitoring fluctuating product prices on e-commerce websites. It allows users to save time by automating price tracking and notification processes.

Automated Scraping: Extracts product details using Selenium.
Dynamic Thresholding: Tracks multiple products with individual thresholds.
Interactive Web Interface: Enables user registration, login, and management of tracking preferences.
🚀 Features
Automated Product Tracking: Fetches product details and prices from e-commerce platforms.
Price Comparison: Monitors product prices against user-defined thresholds.
Email Notifications: Sends alerts when prices drop below thresholds.
Web-Based Interface: Allows users to manage products and preferences easily.
Admin Controls: Enables admins to manage user accounts and system settings.
🛠️ Technologies Used
Programming Language: Python
Libraries: Selenium, Flask, pandas, numpy, dotenv
Database: SQLite
Email Service: SMTP with Gmail
📈 Workflow
Data Collection
Users provide product links and thresholds via the web interface. Selenium scrapes product details and prices from the URL.

Data Processing
Extract product attributes like title, price, and availability. Compare scraped prices with user-defined thresholds.

Notification System
Trigger email alerts for price drops below thresholds.

Web Integration
Flask-based interface for user registration, login, and product management.

Admin Controls
Admin can manage user accounts and update system settings (e.g., CSS selectors).

✔️ Advantages and Disadvantages
Advantages

Automation: Eliminates the need for manual price checking.
User-Centric: Tailored notifications for each user.
Scalable: Handles multiple products and users simultaneously.
Disadvantages

Platform Dependency: Depends on stable HTML structure of e-commerce websites.
Data Accuracy: Scraping errors may occur if website layouts change.
Limited API Use: Fully dynamic platforms may limit scraping capabilities.
🖥️ Deployment
Prerequisites

Python 3.x installed on your system.
Required libraries installed (selenium, flask, etc.).
Browser driver (e.g., GeckoDriver) configured for Selenium.
Steps to Run Locally

Clone the repository:
 git clone https://github.com/your-username/price-tracker.git  
cd price-tracker   
Install dependencies:
 pip install -r requirements.txt  
 
Start the application:
python app.py  
📋Future Enhancements
Dynamic Website Support: Integrate support for JavaScript-heavy websites.
API Integration: Fetch real-time data from e-commerce APIs.
Mobile App: Develop a mobile application for on-the-go tracking.
Enhanced Analytics: Provide insights into price trends for tracked products.
User Feedback System: Allow users to provide feedback for improved recommendations.
