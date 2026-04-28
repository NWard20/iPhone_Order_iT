"""
ASSIGNMENT 12B: SPRINT 6 - Object Refactor
Project: Instant IPhones 
Developer: Nick Ward
"""


import datetime
from iphone_order import IPhoneOrder

# GLOBAL CONSTANTS
DATA_FILE = "order_history.txt"       
HUMAN_REPORT = "latest_receipt.txt"    
COLOR_OPTIONS = ("Black", "Silver", "Blue", "Gold", "Purple")


def get_customer_info():
    name = input("Customer Name: ").title()
    address = input("Shipping Address: ")
    return name, address


def take_order(order):
    order.set_model(input("iPhone Model (Standard/Plus/Pro/Pro Max): "))
    order.set_storage(input("Storage (128GB/256GB/512GB/1TB): "))

    print(f"Available Colors: {COLOR_OPTIONS}")
    order.set_color(input("Choice of color: "))

    order.set_applecare(input("AppleCare+ (Yes/No): "))
    order.set_charger(input("Fast Charger (Yes/No): "))


def calculate_total(order):
    base_price = 999  

    if order.get_model() == "Standard":
        base_price = 799
    elif order.get_model() == "Plus":
        base_price = 899
    elif order.get_model() == "Pro":
        base_price = 999
    elif order.get_model() == "Pro Max":
        base_price = 1199

    storage_cost = 0
    if order.get_storage() == "256GB":
        storage_cost = 100
    elif order.get_storage() == "512GB":
        storage_cost = 300
    elif order.get_storage() == "1TB":
        storage_cost = 500

    total = base_price + storage_cost

    if order.get_applecare() == "Yes":
        total += 199
    if order.get_charger() == "Yes":
        total += 29

    return total


def save_data_and_label(order, total):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # save order
    with open(DATA_FILE, "a") as file:
        file.write(f"{order.get_customer()},{order.get_address()},{total:.2f}\n")

    # receipt
    with open(HUMAN_REPORT, "w") as file:
        file.write(f"Receipt - {time}\n")
        file.write(f"{order.get_customer()} | {order.get_address()}\n")

        file.write(f"model: {order.get_model()}\n")
        file.write(f"storage: {order.get_storage()}\n")
        file.write(f"color: {order.get_color()}\n")
        file.write(f"applecare: {order.get_applecare()}\n")
        file.write(f"charger: {order.get_charger()}\n")

        file.write(f"Total: ${total:.2f}\n")
        file.write("------------------\n")

    print("Receipt saved.")


def review_orders():
    print("\nPast Orders:")

    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                print(line.strip())
    except:
        print("No orders yet.")


def main():
    choice = input("Type 'review' to see old orders or Enter to continue: ")

    if choice.lower() == "review":
        review_orders()

    name, address = get_customer_info()

    order = IPhoneOrder(name, address)

    take_order(order)

    order.display_order()  

    total = calculate_total(order)

    save_data_and_label(order, total)


main()