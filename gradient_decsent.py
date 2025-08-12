import json
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Read the dataset
def read_data():
    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        print("data.csv file not found\n")
        sys.exit(1)
    mileage = df["km"].to_numpy()
    price = df["price"].to_numpy()
    return mileage, price


def standardize(data):
    return (data - np.mean(data)) / np.std(data)


# Revert slope
def revert_slope(theta1, mileage, price):
    return theta1 * (np.std(price) / np.std(mileage))


# Revert intercept
def revert_intercept(theta0, theta1, mileage, price):
    return theta0 * np.std(price) + np.mean(price) - (theta1 * np.mean(mileage))


# Estimate price
def estimated_price(theta0, theta1, mileage):
    return theta0 + theta1 * mileage


# Gradient Descent implementation
def gradient_descent(mileage, price):
    # Initialize parameters
    tmp_theta0, tmp_theta1 = 0, 0
    data_length = len(mileage)
    learning_rate = 0.01
    iterations = 10000
    
    mileage_standardized = standardize(mileage)
    price_standardized = standardize(price)


    # Gradient descent loop
    for i in range(iterations):
        predicted_price = estimated_price(
            tmp_theta0, tmp_theta1, mileage_standardized
        )

        # Update parameters
        tmp_theta0 = tmp_theta0 - learning_rate * (1 / data_length) * np.sum((predicted_price - price_standardized))
        tmp_theta1 = tmp_theta1 - learning_rate * (1 / data_length) * np.sum((predicted_price - price_standardized) * mileage_standardized)


    # revert theta1 and theta0
    theta1 = revert_slope(tmp_theta1, mileage, price)
    theta0 = revert_intercept(tmp_theta0, theta1, mileage, price)

    return theta0, theta1


def plot_data(mileage, price):
    plt.scatter(mileage, price, color="blue", label="mileage, price Points")
    plt.xlabel("mileage")
    plt.ylabel("price")
    plt.title("Car Price")
    plt.show()


def plot_regression_line(mileage, price, theta0, theta1):
    plt.scatter(mileage, price, color="blue", label="mileage price Points")
    plt.plot(
        mileage,
        estimated_price(theta0, theta1, mileage),
        color="red",
        label="mileage, predicted price (aka regression line)",
    )
    plt.xlabel("mileage")
    plt.ylabel("price")
    plt.title("Predicted car Price")
    plt.legend()
    plt.show()


def main():
    mileage, price = read_data()

    if (
        len(mileage) == 0
        or len(price) == 0
        or len(mileage) != len(price)
        or np.isnan(price).any()
        or np.isnan(mileage).any()
    ):
        print("data is invalid\n")
        sys.exit(1)

    theta0, theta1 = gradient_descent(mileage, price)

    with open("thetas.json", "w") as f:
        json.dump({"theta0": theta0, "theta1": theta1}, f)
    f.close()

    print(f"intercept(theta0) = {theta0}\nslope(theta1) = {theta1}\n")

    if len(sys.argv) == 1:
        print("use -h or --help to see the other optional arguments\n")

    elif len(sys.argv) > 1 and sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print(
            """optional arguments:
                -h, --help           show this help message and exit
                -plt, --plot-data    show the mileage and price data points distribution
                -p, --prediction     show the predicted price and mileage line"""
        )

    elif len(sys.argv) > 1 and sys.argv[1] == "--plot-data" or sys.argv[1] == "-plt":
        plot_data(mileage, price)

    elif len(sys.argv) > 1 and sys.argv[1] == "-p" or sys.argv[1] == "--prediction":
        plot_regression_line(mileage, price, theta0, theta1)

    else:
        print("use -h or --help to see the other optional arguments\n")


if __name__ == "__main__":
    main()
