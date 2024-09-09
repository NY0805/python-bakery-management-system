import json
import re


# Define the function that loads data from the file
def load_data_from_cart():
    try:
        file = open('cart_management.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(
                    content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist

def load_cart():
    try:
        with open("cart.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_cart_to_file(cart):
    with open('cart_management.txt', 'w') as file:
        json.dump(cart, file, indent=4)

def add_item_to_cart():
    cart = load_data_from_cart()
    product_id = input("Enter the product ID to add to cart: ")
    quantity = int(input("Enter the quantity: "))

    # Check if product already exists in cart
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            save_cart_to_file(cart)
            print("Item quantity updated.")
            return

    # If product not in cart, add new item
    cart.append({"product_id": product_id, "quantity": quantity})
    save_cart_to_file(cart)
    print("Item added to cart.")

def remove_item_from_cart():
    cart = load_cart_from_file()
    product_id = input("Enter the product ID to remove from cart: ")

    # Filter out the item to remove
    new_cart = [item for item in cart if item['product_id'] != product_id]

    if len(new_cart) == len(cart):
        print("Item not found in cart.")
    else:
        save_cart_to_file(new_cart)
        print("Item removed from cart.")

def modify_item_in_cart():
    cart = load_cart_from_file()
    product_id = input("Enter the product ID to modify: ")

    for item in cart:
        if item['product_id'] == product_id:
            new_quantity = int(input("Enter the new quantity: "))
            item['quantity'] = new_quantity
            save_cart_to_file(cart)
            print("Item quantity updated.")
            return

    print("Item not found in cart.")

def view_cart():
    cart = load_cart_from_file()
    if not cart:
        print("Your cart is empty.")
        return

    print("Your Cart:")
    for item in cart:
        print(f"Product ID: {item['product_id']}, Quantity: {item['quantity']}")
