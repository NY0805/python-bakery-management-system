import json
import re

def load_data_from_customer():
    try:
        with open('customer.txt', 'r') as file:
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

def save_info(info):
    with open('customer.txt', 'w') as file:
        json.dump(info, file, indent=4)

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

    personal_info = {
        "username": username,
        "password": password,
        "age": age,
        "gender": gender,
        "contact_no": contact_no,
        "email": email
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
        print("Product data not found.")

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

def customer_menu():
    while True:
        print("\nWELCOME TO MORNING GLORY BAKERY!")
        print("1. Sign Up")
        print("2. Login")
        print("3. Browse Products")
        print("4. View Cart")
        print("5. Order Tracking")
        print("6. Submit Review")
        print("7. View Loyalty Rewards")  # Added option for viewing loyalty rewards
        print("8. Exit")

        option = input("Please select an option (1/2/3/4/5/6/7/8): ")

        if option == "1":
            create_customer_account()
        elif option == "2":
            login()
        elif option == "3":
            browse_products()
        elif option == "4":
            # Placeholder for view cart function
            print("View Cart functionality is not yet implemented.")
        elif option == "5":
            order_tracking()
        elif option == "6":
            submit_review()
        elif option == "7":
            view_loyalty_rewards()  # Calls the function to view loyalty rewards
        elif option == "8":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

# Function to view loyalty rewards
def view_loyalty_rewards():
    username = input("Enter your username: ")
    # Placeholder: Load loyalty rewards for the username
    # Implement the logic to check loyalty rewards based on purchase history
    print(f"Checking loyalty rewards for {username}...")
    # Example: Assuming we have a function to check rewards
    # rewards = check_loyalty_rewards(username)
    # print(f"Rewards for {username}: {rewards}")

# Run the customer function to start the program
customer_menu()
