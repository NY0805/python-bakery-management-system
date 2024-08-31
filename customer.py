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

    # Manage customers' personal information in the dictionary
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

def load_orders():
    """
    Load the order data from a file (orders.json).
    """
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
    """
    Allow the customer to check the status of their placed order.
    """
    order_id = input("Enter your Order ID: ")

    # Load orders data
    orders = load_orders()

    # Search for the order by order_id
    for order in orders:
        if order["order_id"] == order_id:
            print(f"\nOrder ID: {order['order_id']}")
            print(f"Status: {order['status']}")
            print(f"Items: {order['items']}")
            print(f"Total Price: ${order['total_price']:.2f}")
            return

    # If the order is not found
    print("Order not found. Please check your Order ID.")

def load_reviews():
    """
    Load existing reviews from a file (reviews.json).
    """
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

def save_reviews(reviews):
    """
    Save the updated reviews to a file (reviews.json).
    """
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

def load_reviews():
    """
    Load existing reviews from a file (reviews.json).
    """
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

def save_reviews(reviews):
    """
    Save the updated reviews to a file (reviews.json).
    """
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

    print("Thank you for your feedback! Your review has been submitted.")

def customer_menu():
    while True:
        print("\nWelcome to the Bakery Management System!")
        print("1. Sign Up")
        print("2. Login")
        print("3. Browse Products")
        print("4. View Cart")
        print("5. Order Tracking")  # Changed for consistency
        print("6. Submit Review")  # Option for submitting a review
        print("7. Exit")

        option = input("Please select an option (1/2/3/4/5/6/7): ")

        if option == "1":
            create_customer_account()
        elif option == "2":
            login()
        elif option == "3":
            browse_products()
        elif option == "4":
             load_orders()
        elif option == "5":
            order_tracking()  # Calls the order tracking function
        elif option == "6":
            submit_review()  # Calls the submit review function
        elif option == "7":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")



# Run the customer function to start the program
customer_menu()

