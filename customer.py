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
                return json.loads(content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist

def save_info(info):
    file = open('customer.txt', 'w')  # open the file to write
    json.dump(info, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing

def create_customer_account():
    info = load_data_from_customer()  # initialize 'info' as the name of dictionary that store data loaded from file

    # Getting user input
    username = input("Enter username: ")
    while True:
        password = input("Enter password: ")
        if is_valid_password(password):# Check if the entered password meets the defined requirement (at least one uppercase letter, one number, and six characters long)
            break
        else: # If not, then the `password` is invalid
            print("Password must include at least one uppercase letter, one number, and be at least six characters long.")
    age = input("Enter your age: ")
    gender = input("Select your gender (M = male, F = female): ")
    if gender == "M":
        print("Gender selected: Male")
    elif gender == "F":
        print("Gender selected: Female")
    else:
        print("Invalid input, please select M or F.")
    contact_no = input("Enter your contact number: ")
    email = input("Enter your email: ")

    # Manage customers' information in the dictionary
    personal_info = {
        "username": username,
        "password": password,
        "age": age,
        "gender": gender,
        "contact_no": contact_no,
        "email": email
    }

    # Try to access and read the accounts.txt file
    try:
        with open("accounts.txt", "r") as file:
            accounts = file.readlines()
            flag = False
            for line in accounts:
                stored_username = line.split(',')[0]
                if username == stored_username:
                    flag = True
                    print("This Username already exists. Please try another")
                    return  # Stop the function if the username already exists

    except FileNotFoundError:
        accounts = []  # Treat accounts as an empty list if the file doesn't exist

    # If the username is new, add the new account information to the file
    with open("accounts.txt", "a") as file:
        file.write(f"{username},{password},{age},{gender},{contact_no},{email}\n")
    print(f"Welcome, {username}! Your account has been created successfully!")

def is_valid_password(password):
    # Check if the entered password meets the defined criteria (at least one uppercase letter, one number, and six characters long)
    length = len(password) # Calculate the length of the password
    if len(password) < 6:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    customers = load_data_from_customer()  # Use the loaded customer data

    for customer in customers:
        # Confirm that the username and password match the provided login details
        if customer["username"] == username and customer["password"] == password:
            print("Welcome back!")
            return

    print("Invalid username or password.") # If none of the records match,print an error message

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

# Example call to the function
order_tracking()

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


import json


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
        print("\nWelcome to the Bakery Management System!")
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
