"""
This script uses spline regression to analyze car price vs. mileage data, evaluate user car offers, and identify lucrative deals based on fair price ranges.
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import SplineTransformer
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt


def preprocess_data(data):
    """
    Extracts features and targets from the scraped data.

    Args:
        data (list): List of car listings with 'price' and 'mileage'.

    Returns:
        tuple: Tuple containing:
            - np.ndarray: Feature array (mileage).
            - np.ndarray: Target array (price).
    """
    mileage = np.array([item['mileage'] for item in data]).reshape(-1, 1)  # Reshape for sklearn
    price = np.array([item['price'] for item in data])
    return mileage, price


def fit_spline_regression_model(mileage, price, n_knots=5):
    """
    Fits a spline regression model to the mileage and price data.

    Args:
        mileage (np.ndarray): Array of mileage data.
        price (np.ndarray): Array of price data.
        n_knots (int): Number of knots for the spline transformation.

    Returns:
        tuple: Tuple containing:
            - LinearRegression: The trained spline regression model.
            - SplineTransformer: The transformer for spline features.
            - float: Mean Absolute Error (MAE) of the model.
    """
    # Apply spline transformation
    spline_transformer = SplineTransformer(n_knots=n_knots, degree=3, include_bias=False)
    mileage_spline = spline_transformer.fit_transform(mileage)

    # Fit the spline regression model
    model = LinearRegression()
    model.fit(mileage_spline, price)

    # Compute Mean Absolute Error
    predictions = model.predict(mileage_spline)
    mae = mean_absolute_error(price, predictions)

    # Plot the regression
    plot_regression(mileage, price, model, spline_transformer)

    return model, spline_transformer, mae


def plot_regression(mileage, price, model, spline_transformer):
    """
    Plots the regression model against the original and transformed data.

    Args:
        mileage (np.ndarray): Original mileage data.
        price (np.ndarray): Original price data.
        model (LinearRegression): Trained regression model.
        spline_transformer (SplineTransformer): Transformer for spline features.
    """
    # Generate smooth predictions for plotting
    smooth_mileage = np.linspace(mileage.min(), mileage.max(), 500).reshape(-1, 1)
    smooth_mileage_transformed = spline_transformer.transform(smooth_mileage)
    smooth_predictions = model.predict(smooth_mileage_transformed)

    print("Close plot to get analysis result.")

    # Plot the original data
    plt.figure(figsize=(10, 6))
    plt.scatter(mileage, price, color="blue", label="Actual Data", alpha=0.6)
    plt.plot(smooth_mileage, smooth_predictions, color="red", label="Spline Regression Line", linewidth=2)
    plt.xlabel("Mileage (km)")
    plt.ylabel("Price (CHF)")
    plt.title("Spline Regression: Price vs. Mileage")
    plt.legend()
    plt.grid(True)
    plt.show()


def evaluate_offer(model, spline_transformer, offer_mileage, offer_price, prices, mileages, threshold=0.1):
    """
    Evaluates the user's car offer using the regression model and calculates a fair price range.

    Args:
        model (LinearRegression): The trained spline regression model.
        spline_transformer (SplineTransformer): Transformer for spline features.
        offer_mileage (float): Mileage of the user's car.
        offer_price (float): Price of the user's car.
        prices (np.ndarray): Array of actual car prices.
        mileages (np.ndarray): Array of actual car mileages.
        threshold (float): Percentage deviation allowed for a "fair" offer.

    Returns:
        dict: Decision, fair price range, and the top three lucrative offers.
    """
    # Transform the offer mileage
    offer_features = spline_transformer.transform(np.array([[offer_mileage]]))
    predicted_price = model.predict(offer_features)[0]

    # Calculate fair price range
    price_std = np.std(prices)
    fair_price_min = predicted_price - threshold * price_std
    fair_price_max = predicted_price + threshold * price_std

    if fair_price_min <= offer_price <= fair_price_max:
        decision = "This offer is fair."
    elif offer_price < fair_price_min:
        decision = "This is a great offer!"
    else:
        decision = "This offer is overpriced."

    # Identify the top three lucrative offers
    lucrative_offers = [
        {'price': price, 'mileage': mileage}
        for price, mileage in zip(prices, mileages)
        if price < fair_price_min
    ]
    lucrative_offers = sorted(lucrative_offers, key=lambda x: x['price'])[:3]

    return {
        'decision': decision,
        'predicted_price': predicted_price,
        'fair_range': (fair_price_min, fair_price_max),
        'top_three_offers': lucrative_offers
    }


def analyze_offer(data, offer_price, offer_mileage, n_knots=5, threshold=0.1):
    """
    Main function to analyze the user's car offer using a spline regression model.

    Args:
        data (list): List of car listings with 'price' and 'mileage'.
        offer_price (float): Price of the user's car.
        offer_mileage (float): Mileage of the user's car.
        n_knots (int): Number of knots for the spline transformation.
        threshold (float): Percentage deviation allowed for a "fair" offer.

    Returns:
        str: Decision about whether the offer is great, fair, or overpriced, along with the fair price range
             and top three lucrative offers.
    """
    if not data:
        return "No data available for analysis. Please try with different criteria."

    # Preprocess the data
    mileage, price = preprocess_data(data)

    # Fit the spline regression model
    model, spline_transformer, mae = fit_spline_regression_model(mileage, price, n_knots=n_knots)
    print(f"Spline Regression model trained with Mean Absolute Error: CHF {mae:.2f}")
    print("The MAE indicates the average deviation between the predicted and actual prices.")

    # Evaluate the user's offer
    result = evaluate_offer(model, spline_transformer, offer_mileage, offer_price, price, mileage, threshold)
    output = (f"{result['decision']}\n"
              f"Predicted Price: CHF {result['predicted_price']:.2f}\n"
              f"Fair Price Range: CHF {result['fair_range'][0]:.2f} - CHF {result['fair_range'][1]:.2f}\n")
    if result['top_three_offers']:
        output += "\nTop 3 Lucrative Offers:\n"
        for i, offer in enumerate(result['top_three_offers'], 1):
            output += f"{i}. Price: CHF {offer['price']}, Mileage: {offer['mileage']} km\n"
    else:
        output += "\nNo lucrative offers found below the fair price range."

    return output
