"""
Module to scrape car data from Autoscout24.ch using GeckoDriver (FirefoxDriver).
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait

# Path to GeckoDriver (FirefoxDriver)
driver_path = '/path/to/your/project/.venv/bin/geckodriver'  # Update this with your actual path

# Firefox options for headless mode
firefox_options = Options()
firefox_options.headless = True  # Run in headless mode

BASE_URL = "https://www.autoscout24.ch"


def construct_search_url(brand: str, model: str, year_range: str):
    """
    Constructs the search URL for Autoscout24.ch based on the user's input.

    Args:
        brand (str): Car brand.
        model (str): Car model.
        year_range (str): Year or range of years.

    Returns:
        str: Search URL.
    """
    base_search_url = f"{BASE_URL}/de/s/mo-{model}/mk-{brand}"

    # Adding the year range as query parameters
    year_query = f"?firstRegistrationYearFrom={year_range.split('-')[0]}&firstRegistrationYearTo={year_range.split('-')[-1]}"

    # Add vehicle condition to exclude rollover weighing
    vehicle_condition = "&conditionTypeGroups%5B0%5D=new&conditionTypes%5B0%5D=used"

    return base_search_url + year_query + vehicle_condition


def fetch_car_listings(url: str):
    """
    Fetches car listings from all pages of a given URL using GeckoDriver in headless mode.

    Args:
        url (str): The base URL to fetch.

    Returns:
        List[dict]: List of car listings with 'title', 'price', and 'mileage'.
    """
    try:
        # Use the Service object for GeckoDriver
        service = Service(driver_path)
        driver = webdriver.Firefox(service=service, options=firefox_options)

        # Open the URL
        print(f"Opening URL: {url}")
        driver.get(url)

        try:
            # Execute JavaScript to change the zoom level to make sure all dynamic content is loaded (Workaround required due to problems with scrolling execution
            driver.execute_script(f"document.body.style.zoom='{0.05}'")
            time.sleep(2)
        except Exception as e:
            print(f"Error setting zoom level: {e}")

        # Wait for the page to load completely
        WebDriverWait(driver, 5)

        # Parse the page source using BeautifulSoup
        print("Page loaded successfully. Fetching data...")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        # Extract car listings
        listings = soup.find_all("div", class_="chakra-stack css-2i9fo6")
        if not listings:
            print("No listings found. Check the page structure or update the selector.")
            return []
        else:
            print(f"Found {len(listings)} listings.")
        car_data = [
            {
                "title": listing.find("h2", class_="chakra-heading css-svmyrf").get_text(strip=True)
                if listing.find("h2", class_="chakra-heading css-svmyrf") else "No title",
                "price": listing.find("p", class_="chakra-text css-bwl0or").get_text(strip=True)
                if listing.find("p", class_="chakra-text css-bwl0or") else "No price",
                "mileage": (
                    listing.find("div", class_="css-e0jgn").find("p", class_="chakra-text css-rlwdn6").get_text(
                        strip=True)
                    if listing.find("div", class_="css-e0jgn") else "No mileage"
                )
            }
            for listing in listings
        ]
        print(car_data)
        return car_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        print("Please check the selector or the webpage structure.")
        return []


def scrape_autoscout_data(brand: str, model: str, year_range: str):
    """
    Scrapes car listings from all pages on Autoscout24.ch based on brand, model, and year range.

    Args:
        brand (str): Car brand (e.g., "BMW").
        model (str): Car model (e.g., "3 Series").
        year_range (str): Year or range of years (e.g., "2015-2018").

    Returns:
        List[dict]: List of car listings with 'price' and 'mileage'.
    """

    base_url = construct_search_url(brand, model, year_range)
    car_data = []
    page = 0

    while True:
        paginated_url = f"{base_url}&pagination[page]={page}"
        print(f"Start scraping page {page}: {paginated_url}")

        listings = fetch_car_listings(paginated_url)
        if not listings:
            print(f"Found {len(car_data)} listings.")
            break  # Stop when no more listings are found

        car_data.extend(listings)
        page += 1
        time.sleep(random.uniform(2, 4))  # Avoid being blocked

    return car_data

