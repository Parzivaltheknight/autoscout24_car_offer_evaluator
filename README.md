# Autoscout24 Scraper & Car Offer Evaluator

This project is a Python-based scraper designed to extract used car listings from the Autoscout24 platform and perform a regression analysis to evaluate whether a car offer is competitively priced based on its mileage. It combines data scraping and analysis to help users make informed decisions about car purchases.

## Features

- **Custom User-Agent**: Avoids bot detection and ensures smoother scraping.
- **Headless Browsing**: Uses Selenium for browser-based scraping in headless mode.
- **Rate Limiting**: Implements delays to prevent IP blocking.
- **Data Extraction**: Gathers car listings with attributes like price, mileage, and title.
- **Regression Analysis**: Uses a spline regression model to predict car prices based on mileage.
- **Fair Price Evaluation**: Assesses whether an offer is great, fair, or overpriced based on predicted values.

## Requirements

Before running the project, ensure you meet the following prerequisites:

- **Python Version**: Python 3.8 or higher.
- **Browser**: Firefox (latest version) or another browser of your choice.
- **Driver**: GeckoDriver (for Firefox) or the corresponding driver for your browser (e.g., ChromeDriver for Chrome).

## Setup Instructions

### 1. Install Required Dependencies

Create a virtual environment and install the necessary dependencies from `requirements.txt`:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Update Browser Driver Path

If the browser driver (e.g., GeckoDriver) is not in your system's PATH, update the `driver_path` variable in `autoscout_scraper.py` with the location of your driver.

### 3. Run the Program

Execute the main script to scrape data and analyze car offers:

```bash
python main.py
```

Follow the interactive prompts to enter car details and receive an evaluation.

## File Structure

```bash
autoscout24_car_offer_evaluator/
│
├── autoscout_scraper.py        # Scraper module for Autoscout24.ch
├── regression_analysis_mae.py  # Module for regression analysis
├── utils.py                    # Utility functions for input handling and data cleaning
├── main.py                     # Main script to integrate and run the project
├── requirements.txt            # List of dependencies
└── README.md                   # Project overview and setup instructions
```

## Example Output

```plaintext
Welcome to the Autoscout24.ch Car Offer Evaluator!
This tool helps you decide if a car offer is great, fair, or overpriced.

Please provide the following details:
Brand: BMW
Model: M135
Year or range of years (e.g., 2015 or 2015-2018): 2018-2024
Mileage (km): 50000
Asked/Offered Price (CHF): 35000

Fetching data from Autoscout24.ch...
Found 123 listings.

Analyzing your offer...

Spline Regression model trained with Mean Absolute Error: CHF 3281.98
The MAE indicates the average deviation between the predicted and actual prices.

--- Analysis Result ---
This is a great offer!
Predicted Price: CHF 36799.11
Fair Price Range: CHF 35246.04 - CHF 38352.18

Top 3 Lucrative Offers:
1. Price: CHF 25900, Mileage: [119333] km
2. Price: CHF 26500, Mileage: [96000] km
3. Price: CHF 27800, Mileage: [109600] km

Thank you for using the Autoscout24.ch Car Offer Evaluator!

```

## Notes

- This project assumes the structure of Autoscout24.ch does not change. If updates occur, adjust the scraping logic in `autoscout_scraper.py`.
- The regression analysis uses a spline regression model for improved price prediction accuracy.
- Results depend on the availability and quality of scraped data.

## Disclaimer

This project was created with significant assistance from ChatGPT, an AI language model developed by OpenAI. ChatGPT was utilized throughout the development process, including but not limited to:

- Creating the code's initial structure and implementation.  
- Refining, optimizing, and improving the functionality of the code.  
- Debugging and resolving technical issues encountered during development.  
- Writing documentation, comments, and other explanatory materials related to the code.  

While every effort has been made to ensure the accuracy and functionality of the code, users should be aware that the involvement of an AI tool means that the code may contain unintentional errors or inefficiencies.  

**It is the responsibility of the user to test and validate the software for their specific use case.**  

If you notice any issues, or have suggestions for improvements, please feel free to contribute or report them via this project's repository.

## License

This project is licensed under the GNU General Public License (v3.0). See the [LICENSE](LICENSE) file for more details.

