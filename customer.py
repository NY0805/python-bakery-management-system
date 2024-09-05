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
def save_info(info):

    file = open('manager.txt', 'w')  # open the file to write
    json.dump(info, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing

def create_customer_account():
    info = load_data_from_customer()

    username = input("Enter username: ")
    while True:
        password = input("Enter password: ")
        if len(password) < 6:
            print("Your password must be at least six characters long.")
        elif password.islower():
            print("Your password must contain at least one uppercase letter.")
        elif password.isupper():
            print("Your password must contain at least one lowercase letter.")
        elif not any(char.isdigit() for char in password):
            print("Your password must contain at least one number.")
        else:
            break

    while True:
        age = input("Enter your age: ")
        if age.isdigit():
            break
        else:
            print("Invalid age. Please enter numbers only.")

    gender = input("Select your gender (M = male, F = female): ")
    if gender not in ["M", "F"]:
        print("Invalid input, please select M or F.")
        return

    while True:
        contact_no = input("Enter your contact number: ")
        if contact_no.isdigit():
            break
        else:
            print("Invalid format. Please enter digits only.")

    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}$'
    while True:
        email = input("Enter your email: ")
        if re.fullmatch(regex, email):
            break
        else:
            print("Invalid Email. Please try again.")

    address = input("Enter your address: ")

    personal_info = {
        "username": username,
        "password": password,
        "age": age,
        "gender": gender,
        "contact_no": contact_no,
        "email": email,
        "address": address
    }

    existing_users = load_data_from_customer()
    if any(user["username"] == username for user in existing_users):
        print("This Username already exists. Please try another")
        return

    existing_users.append(personal_info)
    save_info(existing_users)
    print(f"Welcome, {username}! Your account has been created successfully!")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    customers = load_data_from_customer()

    if isinstance(customers, list):
        for customer in customers:
            if customer["username"] == username and customer["password"] == password:
                print("Welcome back!")
                return

    print("Invalid username or password.")


# Function to update customer information
def update_personal_information():
    customers = load_data_from_customer()
    if not customers:
        print("No customer data available.")
        return

    username = input("Enter your username: ")
    found = False

    for customer in customers:
        if customer["username"] == username:
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
                    if len(new_password) < 6:
                        print("Your password must be at least six characters long.")
                    elif new_password.islower():
                        print("Your password must contain at least one uppercase letter.")
                    elif new_password.isupper():
                        print("Your password must contain at least one lowercase letter.")
                    elif not any(char.isdigit() for char in new_password):
                        print("Your password must contain at least one number.")
                    else:
                        customer["password"] = new_password
                        break
            elif choice == "2":
                new_age = input("Enter new age: ")
                if new_age.isdigit():
                    customer["age"] = new_age
                else:
                    print("Invalid age. Please enter numbers only.")
            elif choice == "3":
                new_gender = input("Select your gender (M = male, F = female): ")
                if new_gender in ["M", "F"]:
                    customer["gender"] = new_gender
                else:
                    print("Invalid input, please select M or F.")
            elif choice == "4":
                while True:
                    new_contact_no = input("Enter new contact number: ")
                    if new_contact_no.isdigit():
                        customer["contact_no"] = new_contact_no
                        break
                    else:
                        print("Invalid format. Please enter digits only.")
            elif choice == "5":
                regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}$'
                while True:
                    new_email = input("Enter new email: ")
                    if re.fullmatch(regex, new_email):
                        customer["email"] = new_email
                        break
                    else:
                        print("Invalid Email. Please try again.")
            elif choice == "6":  # Added case for updating address
                new_address = input("Enter new address: ")
                customer["address"] = new_address
            else:
                print("Invalid choice.")

            save_info(customers)
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

# Fictional list of 15 customer orders
orders = [
    {
        "order_id": 1001,
        "username": "Mark0825",
        "items_ordered": ["Bread", "Cookie", "Cake"],
        "total_price": 19.00,
        "status": "Delivered"
    },
    {
        "order_id": 1002,
        "username": "03jane_",
        "items_ordered": ["Muffin", "Cake"],
        "total_price": 18.00,
        "status": "Shipped"
    },
    {
        "order_id": 1003,
        "username": "_eddie",
        "items_ordered": ["Bread", "Cookie"],
        "total_price": 4.00,
        "status": "Processing"
    },
    {
        "order_id": 1004,
        "username": "anna328_",
        "items_ordered": ["Croissant", "Bagel"],
        "total_price": 5.50,
        "status": "Delivered"
    },
    {
        "order_id": 1005,
        "username": "andrew_520",
        "items_ordered": ["Donut", "Brownie", "Muffin"],
        "total_price": 10.75,
        "status": "Shipped"
    },
    {
        "order_id": 1006,
        "username": "chen0lee",
        "items_ordered": ["Cupcake", "Scone"],
        "total_price": 6.00,
        "status": "Cancelled"
    },
    {
        "order_id": 1007,
        "username": "anna_",
        "items_ordered": ["Pie", "Cookie"],
        "total_price": 8.25,
        "status": "Processing"
    },
    {
        "order_id": 1008,
        "username": "boa20prim",
        "items_ordered": ["Cake", "Muffin"],
        "total_price": 15.00,
        "status": "Delivered"
    },
    {
        "order_id": 1009,
        "username": "october.06",
        "items_ordered": ["Bread", "Croissant"],
        "total_price": 5.50,
        "status": "Delivered"
    },
    {
        "order_id": 1010,
        "username": "ethan_wood",
        "items_ordered": ["Bagel", "Donut"],
        "total_price": 4.50,
        "status": "Shipped"
    },
    {
        "order_id": 1011,
        "username": "im.david",
        "items_ordered": ["Cookie", "Scone", "Brownie"],
        "total_price": 9.25,
        "status": "Processing"
    },
    {
        "order_id": 1012,
        "username": "noah_lee",
        "items_ordered": ["Muffin", "Cupcake"],
        "total_price": 6.50,
        "status": "Cancelled"
    },
    {
        "order_id": 1013,
        "username": "scott_lee02",
        "items_ordered": ["Cake", "Brownie"],
        "total_price": 11.00,
        "status": "Delivered"
    },
    {
        "order_id": 1014,
        "username": "_orson_",
        "items_ordered": ["Bagel", "Muffin", "Cookie"],
        "total_price": 7.75,
        "status": "Shipped"
    },
    {
        "order_id": 1015,
        "username": "yubin00",
        "items_ordered": ["Donut", "Croissant", "Cake"],
        "total_price": 12.50,
        "status": "Processing"
    }
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
        print("\nWELCOME TO MORNING GLORY BAKERY!")
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
            create_customer_account()
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
            print("Thank you for visiting our system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

customer_menu()
