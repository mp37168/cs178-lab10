# name: Maddie Phillips
# date: 3/8
# description: CRUD interface for StarbucksDrinks DynamoDB table
# proposed score: 4, Had to use ChatGPT to find a foramt that worked for decimal values 

import boto3
from decimal import Decimal

REGION = "us-east-1"
TABLE_NAME = "StarbucksDrinks"

def get_table():
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table('StarbucksDrinks')


def print_drink(drink):
    name = drink.get("DrinkName", "Unknown")
    size = drink.get("Size", "Unknown")
    price = drink.get("Price", "Unknown")

    print(f"Drink Name: {name}")
    print(f"Size      : {size}")
    print(f"Price     : ${price}")
    print()


def print_all_drinks():
    table = get_table()
    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No drinks found")
        return

    print(f"\nFound {len(items)} drink(s):\n")
    for drink in items:
        print_drink(drink)

def create_drink():
    table = get_table()

    name = input("Enter drink name: ")
    size = input("Enter size (Small/Medium/Large): ")
    price = Decimal(input("Enter price: "))

    table.put_item(
        Item={
            "DrinkName": name,
            "Size": size,
            "Price": price
        }
    )

    print("Drink added successfully\n")

def update_price():
    table = get_table()

    try:
        name = input("Enter drink name: ")
        new_price = Decimal(input("Enter new price: "))

        table.update_item(
            Key={"DrinkName": name},
            UpdateExpression="SET Price = :p",
            ExpressionAttributeValues={
                ":p": new_price
            }
        )

        print("Price updated successfully\n")

    except:
        print("Error updating drink price\n")

def delete_drink():
    table = get_table()

    name = input("Enter drink name to delete: ")

    table.delete_item(
        Key={"DrinkName": name}
    )

    print("Drink deleted (if it existed)\n")

def query_drink():
    table = get_table()

    name = input("Enter drink name: ")

    response = table.get_item(
        Key={"DrinkName": name}
    )

    drink = response.get("Item")

    if drink is None:
        print("Drink not found\n")
        return

    print("\nDrink found:\n")
    print_drink(drink)

def main():

    while True:

        print("===== Starbucks Drinks Database =====")
        print("C - Create drink")
        print("R - Read all drinks")
        print("U - Update drink price")
        print("D - Delete drink")
        print("Q - Query drink")
        print("X - Exit")

        choice = input("Choose an option: ").upper()

        if choice == "C":
            create_drink()

        elif choice == "R":
            print_all_drinks()

        elif choice == "U":
            update_price()

        elif choice == "D":
            delete_drink()

        elif choice == "Q":
            query_drink()

        elif choice == "X":
            break

        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()