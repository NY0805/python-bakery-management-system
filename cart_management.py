import json
import random
from product_menu import product_data
from manager_inventory_control import product_inventory

# Function to display the product menu
def display_menu(products, product_details):
    print("\nProduct Menu:")
    print(f"{'Code':<6} | {'Name':<20} | {'Price':<6}")
    print("-" * 40)
    for (product, detail) in zip(products.values(), product_details.values()):
        print(f"{product['product_code']:<6} | {product['product_name'].title():<20} | {detail['price']}")
    print("-" * 40)


# Function to generate a 10-digit numeric cart_id
def generate_cart_id():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])


def generate_order_id(order_data):
    existing_order_ids = [int(order['order_id'][3:]) for order in order_data.values()]
    if existing_order_ids:
        new_order_num = max(existing_order_ids) + 1
    else:
        new_order_num = 1
    return f"ORD{new_order_num:03}"


# Function to enable customers to add items to the cart
def add_item_to_cart(cart, products):
    display_menu(product_data, product_inventory)  # Show the product menu to the user
    product_code = input("\nEnter the product code: ").strip()

    # Find the product by code
    product = next((item for item in products.values() if item['product_code'] == product_code), None)

    if product:
        quantity = int(input(f"How many {product['product_name']} would you like to add? "))
        if product_code in cart:
            cart[product_code]['quantity'] += quantity
        else:
            cart[product_code] = {'product_name': product['product_name'], 'price': float(product['price']),
                                  'quantity': quantity}
        print(f"\n{product['product_name']} x{quantity} has been added to your cart.")
    else:
        print("Invalid product code.")


# Function to remove an item from the cart
def remove_item_from_cart(cart):
    product_code = input("\nPlease enter the product code of the item you wish to remove: ").strip()
    if product_code in cart:
        del cart[product_code]
        print(f"Product {product_code} has been removed from the cart successfully!")
    else:
        print("Product cannot be found in the cart.")  # Display this message if the product is not in the cart


# Function to modify the quantity of an item in the cart
def modify_item_quantity(cart):
    product_code = input("\nPlease enter the product code of the item you wish to modify: ").strip()
    if product_code in cart:
        new_quantity = int(input(f"Enter new quantity for {cart[product_code]['product_name']}: "))
        cart[product_code]['quantity'] = new_quantity
        print(f"Updated {cart[product_code]['product_name']} quantity to {new_quantity}.")
    else:
        print(" ⚠️Product cannot be found in the cart!")


# Function to view the cart
def view_cart(cart):
    if not cart:
        print("\nYour cart is empty.")
    else:
        print("\nYour Cart:")
        print(f"{'Product':<20} | {'Quantity':<8} | {'Price (RM)':<10}")
        print("-" * 40)
        total_price = 0
        for item in cart.values():
            item_total = item['quantity'] * item['price']
            print(f"{item['product_name']:<20} | {item['quantity']:<8} | RM{item_total:.2f}")
            total_price += item_total
        print("-" * 40)
        print(f"Total Price: RM{total_price:.2f}")


# Function to save the order to a JSON file with cart_id as key
def save_order_to_file(cart, customer_name, cart_id, order_id, status):
    try:
        # Try to load the existing orders
        with open("customer_order_list.txt", "r") as file:
            order_data = json.load(file)
    except FileNotFoundError:
        order_data = {}  # If file not found, start with an empty dictionary

    # Create the new order entry
    order_data[cart_id] = {
        "order_id": order_id,
        "username": customer_name,
        "items_ordered": [f"{item['product_name']} x{item['quantity']}" for item in cart.values()],
        "total_price (RM)": sum(item['quantity'] * item['price'] for item in cart.values()),
        "status": status
    }

    # Write back to the file without overwriting existing orders
    with open("customer_order_list.txt", "w") as file:
        json.dump(order_data, file, indent=4)

    print("Order has been saved successfully.")


def make_payment_or_cancel(cart, customer_name, cart_id):
    if not cart:
        print("\nYour cart is empty. Please add items before proceeding to checkout.")
        return

    print("\nWould you like to:")
    print("1. Proceed with your payment")
    print("2. Cancel your order")

    choice = input("Please select your option: ").strip()

    try:
        with open("customer_order_list.txt", "r") as file:
            order_data = json.load(file)
    except FileNotFoundError:
        order_data = {}

    order_id = generate_order_id(order_data)  # Generate a new order ID

    if choice == '1':
        print("\nPayment completed. Thank you for your purchase!")
        save_order_to_file(cart, customer_name, cart_id, order_id, "Payment Complete")
        cart.clear()  # Clear the cart after payment
    elif choice == '2':
        print("\nYour order has been canceled.")
        save_order_to_file(cart, customer_name, cart_id, order_id, "Canceled")
        cart.clear()  # Clear the cart after cancellation
    else:
        print(" |⚠️Invalid option!Returning to the main menu.|")


# Main shopping cart function
def shopping_cart():
    cart = {}
    customer_name = input("Please enter your name: ")
    cart_id = generate_cart_id()  # Generate a 10-digit numeric cart ID
    print(f"Hello, {customer_name}! Your cart ID is: {cart_id}\n")

    print('\n-----------------------------------------------')
    print('\t\t\t', '', 'CART MANAGEMENT')
    print('-----------------------------------------------')

    while True:
        print("\nPlease select an option:")
        print()
        print("1. Add item")
        print("2. Remove item")
        print("3. Modify item quantity in cart")
        print("4. View cart")
        print("5. Make payment or cancel")
        print("6. Exit to main menu")

        option = input("Select your option: ").strip()

        if option == '1':
            add_item_to_cart(cart, product_data)
        elif option == '2':
            remove_item_from_cart(cart)
        elif option == '3':
            modify_item_quantity(cart)
        elif option == '4':
            view_cart(cart)
        elif option == '5':
            make_payment_or_cancel(cart, customer_name, cart_id)
        elif option == '6':
            print("Thank you for using shopping cart. Goodbye!")
            break
        else:
            print("|⚠️Invalid option. Please try again.|")


# Call the cart management function
shopping_cart()
