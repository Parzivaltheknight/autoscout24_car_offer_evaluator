"""
Main script for assessing car offers on Autoscout24.ch.
"""

from autoscout_scraper import scrape_autoscout_data
from regression_analysis_mae2 import analyze_offer
from utils import parse_user_input, clean_data


def main():
    """
    Main function to run the car offer analysis program.
    """
    print("Welcome to the Autoscout24.ch Car Offer Evaluator!")
    print("This tool helps you decide if a car offer is great, fair, or overpriced.\n")

    # Step 1: Collect user input
    user_input = parse_user_input()
    brand = user_input["brand"]
    model = user_input["model"]
    year_range = user_input["year_range"]
    offer_mileage = user_input["mileage"]
    offer_price = user_input["price"]

    # Step 2: Scrape data from Autoscout24.ch
    print("\nFetching data from Autoscout24.ch...")
    try:
        listings = scrape_autoscout_data(brand, model, year_range)
        print(listings)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # Step 3: Clean scraped data
    print("\nCleaning the data...")
    cleaned_data = clean_data(listings)
    if not cleaned_data:
        print("No valid data found for analysis. Please try with different criteria.")
        return

    print(f"Data cleaned. {len(cleaned_data)} valid listings available for analysis.")

    # Step 4: Analyze the user's car offer
    print("\nAnalyzing your offer...")
    result = analyze_offer(cleaned_data, offer_price, offer_mileage)

    # Step 5: Display results
    print("\n--- Analysis Result ---")
    print(result)
    print("\nThank you for using the Autoscout24.ch Car Offer Evaluator!")


if __name__ == "__main__":
    main()

# ======================== Explenation ========================
# 1. Workflow
# User Input:
# Collects car brand, model, year range, offer price, and mileage using parse_user_input from utils.py.
#
# 2. Scraping:
# Fetches data from Autoscout24.ch using scrape_autoscout_data from autoscout_scraper_old2.py.
#
# 3. Cleaning:
# Removes outliers from scraped data using clean_data from utils.py.
#
# 4. Analysis:
# Uses the regression model in regression_analysis_linear.py to assess whether the user's offer is great, fair, or overpriced.
#
# 5. Output:
# Prints a user-friendly result with the predicted price.
# ======================== Explenation End ========================
