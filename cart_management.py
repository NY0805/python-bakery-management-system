import json
import random


def cart_management():
    try:
        file = open('manager_product_inventory.txt', 'r')  # open the file and read
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


# Function to display the product menu
def display_menu(products):
        print('\n-----------------------------------------------')
        print('\t\t\t', '', '📍PRODUCT MENU📍')
        print('-----------------------------------------------')
        print(f"{'Code':<6} | {'Name':<20} | {'Price':<6}")
        print("-" * 30)

        # Iterate through the dictionary, using the key as the product code
        for product_code, product in products.items():
            print(
                f"{product_code:<6} | {product['product_name'].title():<20} | RM{float(product['price'].replace('RM', '').strip()):.2f}")

        print("-" * 30)


# Function to enable customers to add items to the cart
def add_item_to_cart(cart, products):
    display_menu(products)  # Show the menu again before selecting the item

    # Get the product code from the user
    product_code = input("\nEnter the product code: ").strip()

    # Check if the entered product code exists in the products dictionary
    if product_code in products:
        product = products[product_code]  # Get the product details
        try:
            quantity = int(input(f"How many {product['product_name']} would you like to add?: "))
            if quantity <= 0:
                print("Invalid quantity. Please enter a positive number.")
                return  # Exit the function if quantity is invalid

            # Add the item to the cart
            if product_code in cart:
                # If the product is already in the cart, update the quantity
                cart[product_code]['quantity'] += quantity
            else:
                # If the product is not in the cart, add it with the specified quantity
                cart[product_code] = {'product_name': product['product_name'], 'price': product['price'],
                                      'quantity': quantity}

            print(f"\n{quantity} x {product['product_name']} has been added to your cart.")
        except ValueError:
            print("Invalid input. Please enter a valid number for quantity.")
    else:
        print("Invalid product code. Please try again.")


# Function to remove an item from the cart
def remove_item_from_cart(cart):
    product_code = input("\nPlease enter the product code of the item you wish to remove: ").strip()
    if product_code in cart:
        del cart[product_code]
        print(f"Product {product_code} has been removed from the cart successfully!")
    else:
        print("|⚠️Product cannot be found in the cart!|")


# Function to modify the quantity of an item in the cart
def modify_item_quantity(cart):
    product_code = input("\nPlease enter the product code of the item you wish to modify: ").strip()
    if product_code in cart:
        new_quantity = int(input(f"Enter new quantity for {cart[product_code]['product_name']}: "))
        cart[product_code]['quantity'] = new_quantity
        print(f"Updated {cart[product_code]['product_name']} quantity to {new_quantity}.")
    else:
        print(" |⚠️Product cannot be found in the cart!|")


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


def save_order_to_file(cart, customer_name, cart_id, status):
    order = {
        cart_id: {
            "username": customer_name,  # Use customer_name to maintain consistency
            "items_ordered": [
                f"{item['product_name']} x{item['quantity']}" for item in cart.values()
            ],
            "total_price": sum(float(item['price'].replace('RM', '').strip()) * item['quantity'] for item in cart.values()),
            "status": status
        }
    }

    # Open the file in append mode to add new orders
    with open('customer_order_list.txt', 'a') as file:
        json.dump(order, file, indent=4)  # Use indent=4 for better formatting
        file.write('\n')  # Add a newline to separate each order


def make_payment_or_cancel(cart, customer_name, cart_id):
    total_price = sum(float(item['price'].replace('RM ', '')) * item['quantity'] for item in cart.values())
    print()
    print(f"Total price for your order: RM{total_price:.2f}")

    print("Would you like to:")
    print()
    print("1. Proceed with your payment")
    print("2. Cancel your order")
    choice = input("Please select your option: ")

    if choice == '1':
        # Proceed with payment logic
        save_order_to_file(cart, customer_name, cart_id, "Payment Complete")
        print("Thank you for your payment!")
    elif choice == '2':
        # Cancel the order
        save_order_to_file(cart, customer_name, cart_id, "Canceled")
        print("Your order has been canceled.")
    else:
        print("|⚠️Invalid option! Returning to the main menu.|")


# Main shopping cart function
def shopping_cart():
    # Load product data from file
    product_data = cart_management()

    # Check if product data was loaded successfully
    if not product_data:
        print("|⚠️Error: Could not load product data or no products available.|")
        return

    # Display the product menu at the start
    display_menu(product_data)

    cart = {}
    customer_name = input("Please enter your name: ")
    cart_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])  # Generate a 10-digit cart ID
    print(f"Hello, {customer_name}! Your cart ID is: {cart_id}\n")

    print('\n-----------------------------------------------')
    print('\t\t\t', '', 'CART MANAGEMENT')
    print('-----------------------------------------------')

    while True:
        print("\nPlease select an option:")
        print("1. Add item")
        print("2. Remove item")
        print("3. Modify item quantity in cart")
        print("4. View cart")
        print("5. Make payment or cancel")
        print("6. Exit to main menu")

        option = input("Select your option: ").strip()

        if option == '1':
            add_item_to_cart(cart, product_data)  # Use product_data here
        elif option == '2':
            remove_item_from_cart(cart)
        elif option == '3':
            modify_item_quantity(cart)
        elif option == '4':
            view_cart(cart)
        elif option == '5':
            make_payment_or_cancel(cart, customer_name, cart_id)
        elif option == '6':
            print("Thank you for using the shopping cart. Goodbye!")
            break
        else:
            print("|⚠️Invalid option! Please try again.|")


# Call the shopping cart function to start the program
shopping_cart()

