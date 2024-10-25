import json
import random
import product_menu
import cashier_transaction_completion
import customer_loyalty_rewards
from datetime import datetime
from manager_order_management import load_data_from_customer_order_list
from customer_loyalty_rewards import process_payment


# Function to generate a 10 digit numeric cart_id
def generate_cart_id():
    return ''.join([str(random.randint(1, 9)) for _ in range(10)])


# Function to generate a new order ID
def generate_order_id(order_data):
    existing_order_ids = [int(order['order_id'][3:]) for order in order_data.values()]
    new_order_num = max(existing_order_ids) + 1 if existing_order_ids else 1
    return f"ORD{new_order_num:03}"


# Function to load baker data from a JSON file
def load_baker_data():
    try:
        file = open('baker_product_keeping.txt', 'r')  # open the file and read
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


# Function to load manager data from a JSON file
def load_manager_data():
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


# Function to load discount data from a JSON file
def load_discount_data():
    try:
        file = open('product_discount.txt', 'r')  # open the file and read
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


# Function to enable customers to add items to the cart (with discount check)
def add_item_to_cart(cart):
    while True:  # Loop to allow re-entering product code if the user chooses 'no'
        product_menu.menu()
        baker_data = load_baker_data()  # Load baker product data
        manager_data = load_manager_data()  # Load manager product data
        discount_data = load_discount_data()  # Load discount data

        product_code_input = input("\nEnter the product code: ").strip()

        # Directly search for the product in baker_data
        for item in baker_data.values():
            if item['product_code'] == product_code_input:
                product_name = item["product_name"]  # Retrieve product name

                # Get the price from manager_data
                for key, value in manager_data.items():
                    if value['product_name'] == product_name:
                        product_price = float(value.get("price", 0).replace('RM ', ''))  # Convert price to float
                        break  # Exit loop once the product is found

                # Check if the product has a discount in discount_data
                discount_percentage = 0  # Default to 0% discount if no discount found
                for discount_item in discount_data.values():
                    if discount_item['product_code'] == product_code_input:
                        discount_percentage = float(discount_item['Discount'].replace('%', '')) / 100
                        break

                # Calculate the discounted price if applicable


                # Get the quantity to add to the cart
                while True:  # Loop until a valid quantity is entered
                    quantity = input(f"How many {product_name} would you like to add? ")

                    # Validate the quantity input
                    if quantity.isdigit() and int(quantity) > 0:
                        quantity = int(quantity)
                        break  # Exit loop if valid input
                    else:
                        print("Invalid quantity. Please enter a valid number greater than 0.")

                # Inform customer about the discount and price details
                if discount_percentage > 0:
                    print(f"\nThe product '{product_name}' has a discount of {discount_percentage * 100}%.")
                    print(f"Original price: RM {product_price} per unit.")
                    print(f"Discounted price: RM {discounted_price} per unit.")

                # Calculate the total price with discount
                total_price = discounted_price * quantity  # Calculate total price as float

                # Add to cart or update existing quantity
                if product_code_input not in cart:
                    cart[product_code_input] = {
                        'product_name': product_name,
                        'price': discounted_price,  # Store discounted price as float
                        'quantity': quantity  # Initialize quantity
                    }
                else:
                    cart[product_code_input]['quantity'] += quantity  # Update quantity in the cart

                print(f"\n{product_name} x{quantity} has been added to your cart.")
                print(f"Total price: RM {discounted_price} x {quantity} = RM {total_price}")

                # Prompt the user if they want to return to the main menu
                while True:
                    choice = input("\nDo you want to return to the main menu? (y/n): ").lower()

                    if choice == 'y':
                        print("Returning to the main menu...")
                        return  # Exit the function, returning to the main menu
                    elif choice == 'n':
                        print("\nYou can add more items. Showing the menu again...\n")
                        break  # Exit the inner loop and show the product menu again
                    else:
                        print("\n+--------------------------------------+")
                        print("|⚠️ Invalid input. Please enter 'y' or 'n'. |")
                        print("+--------------------------------------+\n")
                break  # Exit the outer loop if product is added successfully

        else:
            # Print the message if product cannot be found
            print(" |⚠️ Invalid product code! Please ensure you entered it correctly.|")


# Function to remove an item from the cart
def remove_item_from_cart(cart):
    # Check if the cart is empty
    if not cart:
        print("⚠️ Your cart is empty. There are no items to remove.")
        return  # Exit the function if the cart is empty

    while True:
        product_code = input("\nPlease enter the product code of the item you wish to remove: ").strip()

        # Check if the product exists in the cart
        if product_code in cart:
            del cart[product_code]  # Remove the item from the cart
            print(f"Product {product_code} has been removed from the cart successfully!")
        else:
            print("⚠️ Product cannot be found in the cart.")

        # Ask if the user wants to continue removing items
        continue_removing = input(
            "\nDo you want to continue removing from the cart? (yes = y / no = n): ").lower().strip()

        # Check user input for continuation or exit
        if continue_removing in ['y', 'yes']:
            continue  # Continue the loop to remove more items
        elif continue_removing in ['n', 'no']:
            print("Exiting item removal process.")
            break  # Exit the removal process
        else:
            print("|⚠️Invalid input! Please enter 'y' for yes or 'n' for no.|")


# Function to modify the quantity of an item in the cart
def modify_item_quantity(cart):
    if not cart:  # Check if the cart is empty
        print("|⚠️ Your cart is empty. You cannot modify item quantities.|")
        return  # Exit the function if the cart is empty

    while True:
        product_code = input("\nPlease enter the product code of the item you wish to modify: ").strip()

        if product_code in cart:
            while True:
                try:
                    new_quantity = int(input(f"Enter new quantity for {cart[product_code]['product_name']}: "))
                    if new_quantity < 0:
                        print("Quantity cannot be negative.")
                        continue  # Prompt again for a valid quantity
                    # Update quantity
                    cart[product_code]['quantity'] = new_quantity

                    # Calculate new total price
                    new_total_price = new_quantity * cart[product_code]['price']

                    # Display updated information and new total price
                    print(f"Updated {cart[product_code]['product_name']} quantity to {new_quantity}.")
                    print(f"New total price for {cart[product_code]['product_name']}: RM {new_total_price:.2f}")
                    break  # Exit the quantity loop after a successful update

                except ValueError:
                    print("|⚠️ Invalid input! Please enter a valid number.|")

        else:
            print("|⚠️ Product cannot be found in the cart!|")

        while True:
            continue_modifying = input(
                "\nDo you want to continue modifying item quantities? (yes = y / no = n): ").lower().strip()
            if continue_modifying == 'y':
                break  # Continue modifying
            elif continue_modifying == 'n':
                print("Exiting item quantity modification process.")
                return  # Or use break to exit the loop
            else:
                print("|⚠️ Invalid input! Please enter 'y' for yes or 'n' for no.|")


# Function to view the cart
def view_cart(cart):
    while True:  # Loop to allow re-viewing the cart if 'no' is selected
        if not cart:
            print("Your cart is empty.")  # Print this message if the cart is empty
            return

        print("\nYour Cart:")
        print()
        print(f"{'Product':<20} | {'Quantity':<8} | Price (RM)")
        print("-" * 40)

        for item in cart.values():
            item_total = item['quantity'] * item['price']
            print(f"{item['product_name']:<20} | {item['quantity']:<8} | RM{item_total:.2f}")

        print("-" * 40)

        # Prompt the user if they want to return to the main menu
        choice = input("\nDo you want to return to the main menu? (y/n): ").lower()

        if choice == 'y':
            print("Returning to the main menu...")
            return  # Exit the function and return to the main menu
        elif choice == 'n':
            print("Here is your cart again.\n")  # Reloop to show the cart again
        else:
            print("\n+--------------------------------------+")
            print("|⚠️ Invalid input. Please enter 'y' or 'n'. |")
            print("+--------------------------------------+\n")


# Function to save the order to a JSON file with cart_id as key
def save_order_to_file(cart, customer_name, cart_id, order_id, status):
    # Get the current date in 'DD-MM-YYYY' format
    order_date = datetime.now().strftime("%d-%m-%Y")  # Date in 'DD-MM-YYYY' format

    try:
        with open("customer_order_list.txt", "r") as file:
            order_data = json.load(file)
    except FileNotFoundError:
        order_data = {}  # If file not found, start with an empty dictionary

    # Create the new order entry
    order_data[cart_id] = {
        "order_id": order_id,
        "username": customer_name,
        "items_ordered": [f"{item['product_name']} x {item['quantity']}" for item in cart.values()],
        "total_price (RM)": f"{sum(item['quantity'] * item['price'] for item in cart.values()):.2f}",  # Format total price
        "order_date": order_date,  # Add the order date in 'DD-MM-YYYY' format
        "status": status
    }

    # Write back to the file without overwriting existing orders
    with open("customer_order_list.txt", "w") as file:
        json.dump(order_data, file, indent=4)

    print("Order has been saved successfully.")


# Function to display the cart and calculate the total price
def display_cart(cart):
    total_price = 0.0
    print("\nYour cart contains:")
    for item in cart.values():
        print(f"{item['product_name']} x {item['quantity']} at RM {item['price']:.2f}")
        total_price += item['quantity'] * item['price']
    print(f"\nTotal price: RM {total_price:.2f}")
    return total_price


def checkout_or_cancel(cart, customer_name, cart_id):
    if not cart:
        print("\nYour cart is empty! Please add items before proceeding to checkout.")
        return

    total_price = display_cart(cart)  # Displays and calculates total price
    print(f"Current cart ID: {cart_id}")

    print("\nWould you like to:")
    print("1. Place order")
    print("2. Cancel your order")

    choice = input("Please select your option (1 or 2): ").strip()
    print(f"User choice: {choice}")  # Debugging choice

    # Load existing order data
    try:
        with open("customer_order_list.txt", "r") as file:
            order_data = json.load(file)
    except FileNotFoundError:
        order_data = {}

    order_id = generate_order_id(order_data)  # Generate order ID

    if choice == '1':
        print(f"\nTotal price to pay: RM {total_price:.2f}")
        print("\nOrder placed. Please proceed to payment to view the receipt.")

        # Save the updated order to the file
        save_order_to_file(cart, customer_name, cart_id, order_id, "Order Placed")

        # Load loyalty rewards data
        loyalty_data = customer_loyalty_rewards.load_loyalty_rewards()

        # Check if the customer exists in loyalty rewards
        order_info = None  # Initialize variable
        for info in loyalty_data.values():
            if info['username'] == customer_name:
                order_info = info
                break  # Exit loop once the customer is found

        points_change = customer_loyalty_rewards.determine_loyalty_points(total_price)

        if order_info:  # If customer exists, update points
            order_info['loyalty_points'] += points_change  # Add points
            print(f"{customer_name}'s loyalty points updated to: {order_info['loyalty_points']}")

            # Check if status needs to be updated
            new_status = customer_loyalty_rewards.update_customer_status(order_info['loyalty_points'])
            if new_status != order_info['status']:  # Update status if it changes
                order_info['status'] = new_status
                print(f"{customer_name}'s loyalty status updated to: {new_status}")

        else:  # New user, initialize their data in loyalty rewards
            new_order_id = str(len(loyalty_data) + 1)  # Generate new order ID
            loyalty_data[new_order_id] = {
                "username": customer_name,
                "total_spending (RM)": total_price,
                "loyalty_points": points_change,
                "status": "MORNING GLORY'S STANDARD",
                "redeem_rate (RM)": 0,
                "voucher_redeem": 0,
                "redeem_history": []
            }
            print(f"New user {customer_name} added to loyalty rewards with points: {points_change}")

        # Update loyalty rewards in file
        customer_loyalty_rewards.save_loyalty_rewards(loyalty_data)

        # Update customer.txt with the new loyalty points
        try:
            with open("customer.txt", "r") as file:
                customer_data = json.load(file)
        except FileNotFoundError:
            customer_data = {}

        # Update or add customer loyalty points in customer.txt
        customer_found = False
        for key, customer_info in customer_data.items():
            if customer_info['customer_username'] == customer_name:
                customer_info['loyalty_points'] += points_change  # Add points
                customer_found = True
                break

        if customer_found:
            with open("customer.txt", "w") as file:
                json.dump(customer_data, file, indent=4)
        else:
            print(f"Customer {customer_name} does not exist in our system.")

        # Process payment
        process_payment(customer_name, total_price)  # Corrected argument order

        # Clear cart after receipt generation
        cart.clear()
        return

    elif choice == '2':
        print("Order canceled. Your cart has been cleared!")
        cart.clear()
    else:
        print("|⚠️Invalid choice. Please select 1 or 2.|")
    return


def view_payment_receipt(cart_id):
    with open('customer_order_list.txt', 'r') as file:
        order_list = json.load(file)
        order = order_list.get(str(cart_id))
        if order and order['status'] == 'Payment Completed':
            cashier_transaction_completion.receipt(str(cart_id))
        else:
            print('\nThe receipt will only be generated after payment has completed. Please proceed to payment at the counter or via online.')


# Main shopping cart function
def shopping_cart(logged_in_username):  # Accept the logged-in username as an argument
    cart = {}  # Initialize cart as a regular dictionary
    cart_id = generate_cart_id()  # Generate a 10-digit numeric cart ID
    print(f"Hello, {logged_in_username}! Your cart ID is: {cart_id}\n")  # Use logged_in_username

    print('\n-----------------------------------------------')
    print('\t\t\t', '', 'CART MANAGEMENT')
    print('-----------------------------------------------')

    while True:
        print("\n Please select an option:")
        print()
        print("1. Add item")
        print("2. Remove item")
        print("3. Modify item quantity in cart")
        print("4. View cart")
        print("5. Checkout or cancel")
        print("6. View payment receipt")
        print("7. Exit to main menu")

        option = input("Select your option: ").strip()

        if option == '1':
            add_item_to_cart(cart)
        elif option == '2':
            remove_item_from_cart(cart)
        elif option == '3':
            modify_item_quantity(cart)
        elif option == '4':
            view_cart(cart)
        elif option == '5':
            checkout_or_cancel(cart, logged_in_username, cart_id)  # Use the logged-in username
        elif option == '6':
            view_payment_receipt(cart_id)
        elif option == '7':
            print("Exiting to main menu... Goodbye!")
            break
        else:
            print("⚠️ Invalid option! Please try again.")

#shopping_cart()
