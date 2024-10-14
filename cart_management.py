import json
import random
import product_menu

product_data = product_menu.product_data


# Function to generate a 10 digit numeric cart_id
def generate_cart_id():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])


# Function to generate a new order ID based on existing orders
def generate_order_id(order_data):
    existing_order_ids = [int(order['order_id'][3:]) for order in order_data.values()]
    new_order_num = max(existing_order_ids) + 1 if existing_order_ids else 1
    return f"ORD{new_order_num:03}"


# Function to load baker data from a JSON file
def load_baker_data():
    try:
        with open('baker_product_keeping.txt', 'r') as file:
            baker_data = json.load(file)
            return baker_data
    except FileNotFoundError:
        print("Error: baker_product_keeping.txt file not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: baker_product_keeping.txt file is not a valid JSON.")
        return {}


# Function to load manager data from a JSON file
def load_manager_data():
    try:
        with open('manager_product_inventory.txt', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: manager_product_inventory.txt file not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: manager_product_inventory.txt file is not a valid JSON.")
        return {}


# Function to load discount data from a JSON file
def load_discount_data():
    try:
        with open('product_discount.txt', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: product_discount.txt file not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: product_discount.txt file is not a valid JSON.")
        return {}


# Function to enable customers to add items to the cart (with discount check)
# Function to enable customers to add items to the cart (with discount check)
def add_item_to_cart(cart):
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
            discounted_price = product_price * (1 - discount_percentage)

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
            return  # Exit the function after processing

    # Print the message if product cannot be found
    print(" |⚠️ Invalid product code! Please ensure you entered it correctly.|")


# Function to remove an item from the cart
def remove_item_from_cart(cart):
    while True:
        product_code = input("\nPlease enter the product code of the item you wish to remove: ").strip()
        if product_code in cart:
            del cart[product_code]
            print(f"Product {product_code} has been removed from the cart successfully!")
        else:
            print("Product cannot be found in the cart.")

        continue_removing = input(
            "\nDo you want to continue removing from the cart? (yes = y / no = n): ").lower().strip()
        if continue_removing != 'y':
            print("Exiting item removal process.")
            break


# Function to modify the quantity of an item in the cart
def modify_item_quantity(cart):
    while True:
        product_code = input("\nPlease enter the product code of the item you wish to modify: ").strip()
        if product_code in cart:
            try:
                new_quantity = int(input(f"Enter new quantity for {cart[product_code]['product_name']}: "))
                if new_quantity < 0:
                    print("Quantity cannot be negative.")
                    return
                # Update quantity
                cart[product_code]['quantity'] = new_quantity

                # Calculate new total price
                new_total_price = new_quantity * cart[product_code]['price']

                # Display updated information and new total price
                print(f"Updated {cart[product_code]['product_name']} quantity to {new_quantity}.")
                print(f"New total price for {cart[product_code]['product_name']}: RM {new_total_price:.1f}")
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        else:
            print("⚠️ Product cannot be found in the cart!")

        # Ask if the user wants to continue modifying items
        continue_modifying = input("\nDo you want to continue modifying item quantities? (yes = y / no = n): ").lower().strip()
        if continue_modifying != 'y':
            print("Exiting item quantity modification process.")
            break


# Function to view the cart
def view_cart(cart):
    if not cart:
        print("Your cart is empty.") # Print this message if cart is empty
        return

    print("\nYour Cart:")
    print()
    print(f"{'Product':<20} | {'Quantity':<8} | Price (RM)")
    print("-" * 40)

    for item in cart.values():
        item_total = item['quantity'] * item['price']
        print(f"{item['product_name']:<20} | {item['quantity']:<8} | RM{item_total:.2f}")

    print("-" * 40)


# Function to save the order to a JSON file with cart_id as key
def save_order_to_file(cart, customer_name, cart_id, order_id, status):
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
        "status": status
    }

    # Write back to the file without overwriting existing orders
    with open("customer_order_list.txt", "w") as file:
        json.dump(order_data, file, indent=4)

    print("Order has been saved successfully.")


# Main checkout or cancel function
def checkout_or_cancel(cart, customer_name, cart_id):
    if not cart:
        print("\nYour cart is empty! Please add items before proceeding to checkout.")
        return

    # Display cart and total price before making a decision
    total_price = display_cart(cart)

    print("\nWould you like to:")
    print('...............................................')
    print("1. Proceed with your payment")
    print("2. Cancel your order")
    print('...............................................')

    choice = input("Please select your option: ").strip()

    try:
        with open("customer_order_list.txt", "r") as file:
            order_data = json.load(file)
    except FileNotFoundError:
        order_data = {}

    order_id = generate_order_id(order_data)  # Generate a new order ID

    # If user chooses to proceed with payment
    if choice == '1':
        print(f"\nTotal price to pay: RM {total_price:.2f}")
        print("\nPayment completed. Thank you for your purchase!")
        save_order_to_file(cart, customer_name, cart_id, order_id, "Payment Completed")
        cart.clear()  # Clear the cart after payment
    elif choice == '2':
        print("\nYour order has been canceled.")
        save_order_to_file(cart, customer_name, cart_id, order_id, "Canceled")
        cart.clear()  # Clear the cart after cancellation
    else:
        print("⚠️ Invalid option! Returning to the main menu.")



# Main shopping cart function
def shopping_cart():
    cart = {}  # Initialize cart as a regular dictionary
    customer_name = input("Please enter your username: ")
    cart_id = generate_cart_id()  # Generate a 10-digit numeric cart ID
    print(f"Hello, {customer_name}! Your cart ID is: {cart_id}\n")

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
        print("6. Exit to main menu")

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
            checkout_or_cancel(cart, customer_name, cart_id)
        elif option == '6':
            print("Exiting to main menu...Goodbye!")
            break
        else:
            print("⚠️ Invalid option! Please try again.")

# Start the shopping cart process
shopping_cart()
