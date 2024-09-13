import uuid
import json

# Define the function that loads data from the file
def load_data_from_products():
    try:
        file = open('customer_order_list.txt', 'r')  # open the file and read
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

# Define the path to the order file
ORDER_FILE = 'customer_order_list.txt'

def generate_cart_id():
    """Generate a unique cart ID using UUID."""
    return str(uuid.uuid4())

def load_orders():
    """Load orders from the file."""
    try:
        with open(ORDER_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if the file is missing or empty

def save_orders(orders):
    """Save orders to the file."""
    with open(ORDER_FILE, 'w') as file:
        json.dump(orders, file, indent=4)

def update_order_list(order_id, username, items_ordered, total_price, status):
    """Update the customer order list and save to file."""
    orders = load_orders()  # Load existing orders from file
    order_exists = False

    for order in orders:
        if order["order_id"] == order_id:
            # Update existing order
            order["items_ordered"] = items_ordered
            order["total_price"] = total_price
            order["status"] = status
            order_exists = True
            break

    if not order_exists:
        # Append new order
        orders.append({
            "order_id": order_id,
            "username": username,
            "items_ordered": items_ordered,
            "total_price": total_price,
            "status": status
        })

    save_orders(orders)  # Save the updated orders back to file

def shopping_cart():
    print("Welcome to the Shopping Cart Program!")

    # Ask for customer name and create a new cart ID
    customer_name = input("Please enter your name: ")
    cart_id = generate_cart_id()
    print(f"Hello, {customer_name}! Your cart ID is: {cart_id}")

    # Initialize the cart for the customer
    cart = []
    quantities = []
    prices = []

    def view_cart():
        if len(cart) == 0:
            print("Your shopping cart is empty.")
        else:
            print("This is what is in your shopping cart:")
            for i in range(len(cart)):
                print(f"{cart[i]} - Quantity: {quantities[i]}, Price: ${prices[i]:.2f}")

    while True:
        print("\nPlease choose one of the following options:")
        print("1. Add item")
        print("2. Remove item")
        print("3. Modify item quantity in cart")
        print("4. View cart")
        print("5. Make payment or cancel")
        print("6. Exit to main menu")

        select = int(input("Select your option: "))

        if select == 1:
            item = input("What would you like to add? ")
            quantity = int(input("Enter the quantity: "))
            price = float(input("Enter the price of the item: $"))
            if item in cart:
                index = cart.index(item)
                quantities[index] += quantity
                prices[index] = price
                print(f"Updated quantity of '{item}' to {quantities[index]}, price updated to ${price:.2f}.")
            else:
                cart.append(item)
                quantities.append(quantity)
                prices.append(price)
                print(f"'{item}' has been added to your cart with quantity {quantity} and price ${price:.2f}.")

        elif select == 2:
            remove_item = input("Type the name of the item you would like to remove: ")
            if remove_item in cart:
                index = cart.index(remove_item)
                cart.pop(index)
                quantities.pop(index)
                prices.pop(index)
                print(f"'{remove_item}' has been removed from your cart.")
            else:
                print(f"'{remove_item}' is not in your cart.")

        elif select == 3:
            modify_item = input("Type the name of the item you want to modify: ")
            if modify_item in cart:
                index = cart.index(modify_item)
                new_quantity = int(input(f"Enter the new quantity for '{modify_item}': "))
                new_price = float(input(f"Enter the new price for '{modify_item}': $"))
                quantities[index] = new_quantity
                prices[index] = new_price
                print(f"The quantity of '{modify_item}' has been updated to {new_quantity} and price to ${new_price:.2f}.")
            else:
                print(f"'{modify_item}' is not in your cart.")

        elif select == 4:
            view_cart()

        elif select == 5:
            view_cart()
            if len(cart) > 0:
                action = input("Would you like to (P)ay or (C)ancel your order? ").upper()
                if action == "P":
                    total_price = sum([quantities[i] * prices[i] for i in range(len(cart))])
                    print(f"Your total is: ${total_price:.2f}. Payment processing...")
                    update_order_list(int(cart_id[:8], 16), customer_name, [f"{cart[i]} x{quantities[i]}" for i in range(len(cart))], total_price, "Payment Complete")
                    print("Payment completed successfully!")
                    break
                elif action == "C":
                    update_order_list(int(cart_id[:8], 16), customer_name, [f"{cart[i]} x{quantities[i]}" for i in range(len(cart))], 0, "Canceled")
                    print("Your order has been canceled.")
                    break
                else:
                    print("Invalid option. Please try again.")
            else:
                print("Your cart is empty; no action needed.")

        elif select == 6:
            print("Returning to the main menu.")
            break

        else:
            print("Invalid option. Please try again.")

    # Print the updated orders
    print("Updated Customer Orders:")
    for order in load_orders():
        print(order)

# Call the shopping_cart function
shopping_cart()
