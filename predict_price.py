import json
import sys


def read_thetas(file_name):
    # Open and read the JSON file
    with open(file_name, "r") as file:
        thetas = json.load(file)
    file.close()
    return thetas[("theta0")], thetas[("theta1")]


def calculate_price(theta0, theta1, mileage):
    price = theta0 + theta1 * mileage
    return price


def main():
    theta0, tetha1 = read_thetas("thetas.json")
    mileage = 0

    while True:
        try:
            mileage = input(
                "Enter your mileage—don’t worry, I won’t judge if it’s been around the block a few times! 🚗😜\n - "
            )

            assert (
                all([c in "1234567890-" for c in mileage]) == True and mileage != ""
            ), "\nLooks like your mileage took a wrong turn—let’s keep it on the road with a valid number! 🚗🤪\n"

            assert (
                int(mileage) >= 0
            ), "\nNegative mileage? Unless your car’s been driving backwards its whole life, let’s keep it positive! 🚗🔄\n"

        except KeyboardInterrupt:
            sys.exit(0)

        except AssertionError as error:
            print(error)
            continue

        price = int(calculate_price(theta0, tetha1, int(mileage)))
        if price < 0:
            print(
                "\nOops! It looks like your car is worth less than zero—might want to check if it's a time machine that's gone back to the Stone Age! 🚗💨\n"
            )

        elif price < 1000:
            print(
                f"\nYour car price is: {price} dollars! 🚗💸 Looks like you're getting a vintage deal—hope it still has wheels!\n"
            )
        else:
            print(
                f"\nYour car price is: {price} dollars! 🚗💸 Hope it comes with a VIP parking spot!\n"
            )
        break


if __name__ == "__main__":
    main()
