"""
Utility functions for the car analysis project.
"""

import re
import numpy as np


def parse_user_input():
    """
    Parses user input for brand, model, year range, price, and mileage.

    Returns:
        dict: Dictionary containing parsed user inputs:
            - brand (str): Car brand.
            - model (str): Car model.
            - year_range (str): Year range (e.g., "2015-2018").
            - mileage (float): Offer mileage.
            - price (float): Offer price.
    """
    print("Please provide the following details:")

    # Brand and model
    brand = input("Brand: ").strip().lower()
    model = input("Model: ").strip().lower()

    # Year range validation
    while True:
        year_range = input("Year or range of years (e.g., 2015 or 2015-2018): ").strip()
        if re.match(r"^\d{4}(-\d{4})?$", year_range):
            break
        print("Invalid year or range. Please enter a valid year (e.g., '2015') or range (e.g., '2015-2018').")


    # Mileage validation
    while True:
        try:
            mileage = float(input("Mileage (km): ").strip())
            if mileage > 0:
                break
            print("Mileage must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Price validation
    while True:
        try:
            price = float(input("Asked/Offered Price (CHF): ").strip())
            if price > 0:
                break
            print("Price must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


    return {"brand": brand, "model": model, "year_range": year_range, "price": price, "mileage": mileage}


def clean_data(data):
    """
    Cleans the scraped data by preprocessing and removing outliers.

    Args:
        data (list): List of car listings with 'price' and 'mileage'.

    Returns:
        list: Cleaned list of car data.
    """
    if not data:
        return []


    # Preprocess price and mileage
    cleaned_data = []
    for item in data:
        try:
            # Clean price: Remove "CHF", non-numeric characters, and special formatting
            price_raw = str(item["price"])
            price = int(
                price_raw.replace("CHF", "")
                .replace("\xa0", "")
                .replace("'", "")
                .replace(".–", "")
                .strip()
            )

            # Clean mileage
            mileage_raw = str(item['mileage']).strip()
            if mileage_raw in {"Neues Fahrzeug", "No mileage"}:
                mileage = 0
            else:
                mileage = int(
                    mileage_raw.replace("'", "").replace(" km", "").strip()
                )
            print(f"Mileage '{mileage_raw}' parsed as {mileage}")

            # Append cleaned data
            cleaned_data.append({"price": price, "mileage": mileage})
        except (ValueError, AttributeError) as e:
            # Skip invalid data
            print(f"Skipping invalid data entry: {item} due to error: {e}")

    if not cleaned_data:
        print("No valid data to process after cleaning.")
        return []

    # Convert to numpy arrays for statistical filtering
    prices = [item["price"] for item in cleaned_data]
    mileages = [item["mileage"] for item in cleaned_data]

    # Ensure prices and mileages are numpy arrays of numeric types
    prices = np.array(prices, dtype=np.float64)
    mileages = np.array(mileages, dtype=np.float64)

    # Calculate thresholds for filtering outliers (1.5x IQR)
    price_q1, price_q3 = np.percentile(prices, [25, 75])
    valid_mileages = [m for m in mileages if m > 0]  # Excluded listings with mileage 0 for correct IQR calculations
    mileage_q1, mileage_q3 = np.percentile(valid_mileages, [25, 75])

    price_iqr = price_q3 - price_q1
    mileage_iqr = mileage_q3 - mileage_q1

    price_lower_bound = price_q1 - 1.5 * price_iqr
    price_upper_bound = price_q3 + 1.5 * price_iqr

    mileage_lower_bound = mileage_q1 - 1.5 * mileage_iqr
    mileage_upper_bound = mileage_q3 + 1.5 * mileage_iqr

    # Filter out outliers
    final_data = [
        item
        for item in cleaned_data
        if price_lower_bound <= item["price"] <= price_upper_bound
        and (item["mileage"] == 0 or mileage_lower_bound <= item["mileage"] <= mileage_upper_bound)
    ]
    print(final_data)
    return final_data
