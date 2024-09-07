import json
import re


# Define the function that loads data from the file
def load_data_from_customer():
    try:
        file = open('customer.txt', 'r')  # open the file and read
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


def save_info(customer_info):

    file = open('customer.txt', 'w')  # open the file to write
    json.dump(customer_info, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


customer_info = load_data_from_customer()


def sign_up():

    customer_name = input('\nName: ')
    if customer_name in customer_info:
        print('\n+--------------------------------------------------+')
        print('|⚠️ Warning: One person can only have one account! |')
        print('+--------------------------------------------------+')
        print('You already have an account.')
        print('Directing to the login page......')
        login()

    else:
        customer_username = input("Username: ")
        while customer_username in (customer_info[customer_name]['customer_username'] for customer_name in customer_info):
            print('\n+----------------------------------------------------------+')
            print('|⚠️ Username has been used. Please enter another username. |')
            print('+----------------------------------------------------------+\n')
            customer_username = input('Username: ')

        customer_password = input("Password: ")
        while len(customer_password) < 8 or len(customer_password) > 12:
            print('\n+---------------------------------------------------------------------------+')
            print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
            print('+---------------------------------------------------------------------------+\n')
            customer_password = input('Password: ')

        while True:
            try:
                age = int(input('Age: '))
                if age < 12:
                    print('\n+----------------------+')
                    print('|⚠️ You are under age. |')
                    print('+----------------------+\n')
                else:
                    break
            except ValueError:
                print('\n+-------------------------------------------+')
                print('|⚠️ Invalid age. Please enter numbers only. |')
                print('+-------------------------------------------+\n')

        while True:
            gender = input('Gender(m=male, f=female, x=prefer not to say): ')
            if gender not in ['f', 'm', 'x']:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+\n')
            else:
                if gender == 'f':
                    gender = 'female'
                    break
                elif gender == 'm':
                    gender = 'male'
                    break
                else:
                    gender = 'prefer not to say'
                    break

        contact_no = input('Contact number(xxx-xxxxxxx): ')
        while not re.fullmatch(r'^\d{3}-\d{7}$', contact_no):
            print('\n+-----------------------------------------------+')
            print('|⚠️ Invalid contact number. Please enter again. |')
            print('+-----------------------------------------------+\n')
            contact_no = input('Contact number(xxx-xxxxxxx): ')

        email = input('Email: ')
        while not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid email. Please enter again. |')
            print('+--------------------------------------+\n')
            email = input('Email: ')

        address = input('Address: ')

        customer_info[customer_name] = {
            'customer_username': customer_username,
            'customer_password': customer_password,
            'age': age,
            'gender': gender,
            'contact_no': contact_no,
            'email': email,
            "address": address
        }

        save_info(customer_info)
        print('\nInformation saved.')
        print(f'Welcome, {customer_name}! Your account has been created successfully!\n')


def login():

    customer_name = input('\nName: ')
    if customer_name in customer_info:
        customer_username = input("Username: ")
        while customer_username != customer_info[customer_name]['customer_username']:
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect username. Please enter again. |')
            print('+-------------------------------------------+\n')
            customer_username = input("Username: ")

        customer_password = input("Password: ")
        while customer_password != customer_info[customer_name]['customer_password']:
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')
            customer_password = input("Password: ")

        print(f'\nWelcome back, {customer_name}!\n')

    else:
        print('\n+------------------------------------------------------------+')
        print('|⚠️ This is your FIRST TIME login, please create an account. |')
        print('+------------------------------------------------------------+')
        print('Directing to sign up page......\n')
        sign_up()


def customer():
    #customer_info = load_data_from_customer()

    print('\n----------------------------------------------------')
    print('\t\t\t\t\t', '', 'CUSTOMER')
    print('----------------------------------------------------')
    print('\n+---------------------------------------------------------+')
    print('|💡 Please "sign up" if you\'re logging in the first time. |')
    print('|   Please "log in" if you already have an account.       |')
    print('+---------------------------------------------------------+\n')

    choice = input('1. Sign up\n'
                   '2. Log in\n'
                   'Enter your choice(1, 2):\n>>> ')

    while choice not in ['1', '2']:
        print('\n+--------------------------------------+')
        print('|⚠️ Invalid input. Please enter again. |')
        print('+--------------------------------------+\n')
        choice = input('1. Sign up\n'
                       '2. Log in\n'
                       'Enter your choice(1, 2):\n>>> ')

    if choice == '1':
        sign_up()
        customer_menu()

    else:
        login()
        customer_menu()


# Function to update customer information
def update_personal_information():

    if not customer_info:
        print("No customer data available.")
        return

    customer_username = input("Enter your username: ")
    found = False

    for customers in customer_info:
        if customers["customer_username"] == customer_username:
            found = True
            print("What do you want to update?")
            print("1. Password")
            print("2. Age")
            print("3. Gender")
            print("4. Contact Number")
            print("5. Email")
            print("6. Address")  # Added option to update address
            choice = input("Choose the field number to update: ")

            if choice == "1":
                while True:
                    new_password = input("Enter new password: ")
                    if len(new_password) < 8 or len(new_password) > 12:
                        print('\n+---------------------------------------------------------------------------+')
                        print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
                        print('+---------------------------------------------------------------------------+\n')

                    else:
                        customer_info["customer_password"] = new_password
                        break

            elif choice == "2":
                try:
                    new_age = int(input("Enter new age: "))
                    if new_age >= 12:
                        customer_info["age"] = new_age
                    else:
                        print('\n+----------------------+')
                        print('|⚠️ You are under age. |')
                        print('+----------------------+\n')
                except ValueError:
                    print('\n+-------------------------------------------+')
                    print('|⚠️ Invalid age. Please enter numbers only. |')
                    print('+-------------------------------------------+\n')

            elif choice == "3":
                new_gender = input("Select your gender(m=male, f=female, x=prefer not to say): ")
                if new_gender in ['f', 'm', 'x']:
                    if new_gender == 'f':
                        customer_info["gender"] = 'female'
                    elif new_gender == 'm':
                        customer_info['gender'] = 'male'
                    else:
                        customer_info['gender'] = 'prefer not to say'
                else:
                    print('\n+--------------------------------------+')
                    print('|⚠️ Invalid input. Please enter again. |')
                    print('+--------------------------------------+\n')

            elif choice == "4":
                while True:
                    new_contact_no = input("Enter new contact number: ")
                    if re.fullmatch(r'^\d{3}-\d{7}$', new_contact_no):
                        customer_info["contact_no"] = new_contact_no
                        break
                    else:
                        print('\n+-----------------------------------------------+')
                        print('|⚠️ Invalid contact number. Please enter again. |')
                        print('+-----------------------------------------------+\n')

            elif choice == "5":
                while True:
                    new_email = input("Enter new email: ")
                    if re.fullmatch(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}$', new_email):
                        customer_info["email"] = new_email
                        break
                    else:
                        print('\n+--------------------------------------+')
                        print('|⚠️ Invalid email. Please enter again. |')
                        print('+--------------------------------------+\n')

            elif choice == "6":  # Added case for updating address
                new_address = input("Enter new address: ")
                customer_info["address"] = new_address
            else:
                print("Invalid choice.")

            save_info(customer_info)
            print("Your information has been updated.")
            break

    if not found:
        print("Customer not found.")

def browse_products():
    try:
        # Load the products from the JSON file
        with open("products.txt", "r") as file:
            products = json.load(file)

        # Display the products to the customer
        print("\nAvailable Products:")
        for product in products:
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']}")
            print(f"Description: {product['description']}\n")

    except FileNotFoundError:
        print("Product data cannot be found.")

# Helper functions to manage the cart
def load_cart_from_file():
    try:
        with open('cart.txt', 'r') as file:
            content = file.read().strip()
            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return []
            else:
                return []
    except FileNotFoundError:
        return []

def save_cart_to_file(cart):
    with open('cart.txt', 'w') as file:
        json.dump(cart, file, indent=4)

def add_item_to_cart():
    cart = load_cart_from_file()
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

def load_orders(): #Load the order data from a file
    try:
        with open("orders.txt", "r") as file:
            orders = json.load(file)
        return orders
    except FileNotFoundError:
        print("Order data not found. Please make sure the file exists.")
        return []
    except json.JSONDecodeError:
        print("Error loading order data. The file format might be incorrect.")
        return []


orders = [
    {"order_id": 1001, "username": "Mark0825", "items_ordered": ["Bread x1", "Cake x1"], "total_price": 15.00, "status": "Pending Payment"},
    {"order_id": 1002, "username": "03jane_", "items_ordered": ["Muffin x2", "Cake x1"], "total_price": 12.50, "status": "Pending"},
    {"order_id": 1003, "username": "_eddie", "items_ordered": ["Bread x1", "Pastry x2"], "total_price": 8.00, "status": "Processing"},
    {"order_id": 1004, "username": "anna328_", "items_ordered": ["Biscuit x3"], "total_price": 3.75, "status": "Delivered"},
    {"order_id": 1005, "username": "andrew_520", "items_ordered": ["Muffin x1", "Cake x2"], "total_price": 10.00, "status": "Pending Payment"},
    {"order_id": 1006, "username": "chen0lee", "items_ordered": ["Pastry x1", "Bread x2"], "total_price": 7.00, "status": "Cancelled"},
    {"order_id": 1007, "username": "anna_", "items_ordered": ["Cake x2", "Muffin x1"], "total_price": 14.00, "status": "Processing"},
    {"order_id": 1008, "username": "boa20prim", "items_ordered": ["Bread x1", "Biscuit x2"], "total_price": 5.50, "status": "On the way"},
    {"order_id": 1009, "username": "october.06", "items_ordered": ["Cake x1", "Pastry x1"], "total_price": 10.00, "status": "Delivered"},
    {"order_id": 1010, "username": "ethan_wood", "items_ordered": ["Muffin x1", "Biscuit x1"], "total_price": 4.00, "status": "Pending"},
    {"order_id": 1011, "username": "im.david", "items_ordered": ["Pastry x2", "Bread x1"], "total_price": 9.00, "status": "Processing"},
    {"order_id": 1012, "username": "noah_lee", "items_ordered": ["Muffin x1", "Cake x1"], "total_price": 7.50, "status": "Cancelled"},
    {"order_id": 1013, "username": "scott_lee02", "items_ordered": ["Pastry x1", "Bread x2"], "total_price": 8.00, "status": "Delivered"},
    {"order_id": 1014, "username": "_orson_", "items_ordered": ["Biscuit x1", "Cake x1"], "total_price": 5.00, "status": "On the way"},
    {"order_id": 1015, "username": "yubin00", "items_ordered": ["Bread x2", "Muffin x1"], "total_price": 6.50, "status": "Processing"}
]


def order_tracking():
    # Prompt the user to enter their Order ID
    order_id = input("Enter your Order ID: ")

    # Load orders data
    orders = load_orders()

    # Check if the order_id exists in the loaded orders data
    order_exists = False  # Initialize a flag to track if the order is found

    # Iterate over each order to find the matching order ID
    for order in orders:
        if order["order_id"] == order_id:
            order_exists = True
            order_status = order["status"]
            order_details = order["items"]

            # Display order information
            print(f"Order ID: {order_id}")
            print(f"Status: {order_status}")
            print(f"Details: {order_details}")
            break

    # If the order ID was not found, show an error message
    if not order_exists:
        print("Order ID cannot be found. Please check and try again.")


def load_reviews(): #Load existing reviews from a file (reviews.json).
    try:
        with open("reviews.txt", "r") as file:
            reviews = json.load(file)
        return reviews
    except FileNotFoundError:
        # If file doesn't exist, return an empty list
        return []
    except json.JSONDecodeError:
        print("Error loading review data. The file format might be incorrect.")
        return []


def save_reviews(reviews): #Save the updated reviews to a file
    with open("reviews.txt", "w") as file:
        json.dump(reviews, file, indent=4)


def submit_review():# Allow the customer to submit a review for a purchased product
    # Get user input
    product_name = input("Enter the name of the product you want to review: ")
    review_text = input("Enter your review: ")
    rating = input("Rate your product (1-5): ")

    # Validate rating input
    if not rating.isdigit() or int(rating) not in range(1, 6):
        print("Invalid rating. Please enter a number between 1 and 5.")
        return

    # Create a review entry
    review = {
        "product_name": product_name,
        "review_text": review_text,
        "rating": int(rating)
    }

    # Load existing reviews
    reviews = load_reviews()

    # Add new review to the list
    reviews.append(review)

    # Save updated reviews
    save_reviews(reviews)

    print("Thank you for submitting your feedback! We have received your review.")


def load_reviews(): #Load existing reviews from a file (reviews.json)
    try:
        with open("reviews.txt", "r") as file:
            reviews = json.load(file)
        return reviews
    except FileNotFoundError:
        # If file doesn't exist, return an empty list
        return []
    except json.JSONDecodeError:
        print("Error loading review data. The file format might be incorrect.")
        return []


def save_reviews(reviews): #Save the updated reviews to a file
    with open("reviews.txt", "w") as file:
        json.dump(reviews, file, indent=4)


def submit_review(): #Allow customer to submit review for purchased product
    # Get user input
    product_name = input("Enter the name of the product you want to review: ")
    review_text = input("Enter your review: ")
    rating = input("Enter your rating (1-5): ")

    # Validate rating input
    if not rating.isdigit() or int(rating) not in range(1, 6):
        print("Invalid rating. Please enter a number between 1 and 5.")
        return

    # Manage customers' review in the dictionary
    review = {
        "product_name": product_name,
        "review_text": review_text,
        "rating": int(rating)
    }

    # Load existing reviews
    reviews = load_reviews()

    # Add new review to the list
    reviews.append(review)

    # Save updated reviews
    save_reviews(reviews)

    print("Thank you for your feedback! Your review has been submitted.")


# Function to load customer data
def load_customer_data():
    try:
        with open("customers.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Function to save customer data
def save_customer_data(data):
    with open("customers.json", "w") as file:
        json.dump(data, file)


# Function to update purchase history
def update_purchase_history(username, purchase_amount):
    customers = load_customer_data()

    if username in customers:
        customer = customers[username]
        customer['total_spent'] += purchase_amount
        customer['purchase_count'] += 1
    else:
        customer = {
            'total_spent': purchase_amount,
            'purchase_count': 1
        }

    # Apply reward if eligible
    if customer['purchase_count'] % 5 == 0:
        print("Congratulations! You've earned a 10% discount.")

    if customer['total_spent'] >= 100:
        print("Congratulations! You've earned a free item.")

    customers[username] = customer
    save_customer_data(customers)


# Example usage
def checkout(username, total_amount):
    update_purchase_history(username, total_amount)
    print(f"Order placed successfully! Your total amount is ${total_amount:.2f}.")


# Function to view loyalty rewards
def view_loyalty_rewards():
    username = input("Enter your username: ")
    # Placeholder: Load loyalty rewards for the username
    # Implement the logic to check loyalty rewards based on purchase history
    print(f"Checking loyalty rewards for {username}...")
    # Example: Assuming we have a function to check rewards
    # rewards = check_loyalty_rewards(username)
    # print(f"Rewards for {username}: {rewards}")


def customer_menu():
    while True:
        print("WELCOME TO MORNING GLORY BAKERY!")
        print("1. Sign Up")
        print("2. Login")
        print("3. Browse Products")
        print("4. View Cart")
        print("5. Order Tracking")
        print("6. Submit Review")
        print("7. View Loyalty Rewards")
        print("8. Update Personal Information")
        print("9. Manage Accounts")  # Added 'Manage Accounts' option
        print("0. Exit")

        option = input("Please select an option (0-9): ")

        if option == "1":
            sign_up()
        elif option == "2":
            login()
        elif option == "3":
            browse_products()
        elif option == "4":
            view_cart()  # Calls the function to view cart
        elif option == "5":
            order_tracking()
        elif option == "6":
            submit_review()
        elif option == "7":
            view_loyalty_rewards()
        elif option == "8":
            update_personal_information()
        elif option == "9":
            manage_accounts()  # Call the function to manage accounts
        elif option == "0":
            print("Thank you for visiting our bakery. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


