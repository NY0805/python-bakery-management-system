import json

# Define the function that loads data from the file
def load_data_from_customer():
    try:
        file = open('customers.txt', 'r')  # open the file and read
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

    file = open('manager.txt', 'w')  # open the file to write
    json.dump(info, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing

def create_customer_account():
    info = load_data_from_customer()  # initialize 'info' as the name of dictionary that store data loaded from file

    # Getting user input
    username = input("Enter username: ")
    password = input("Enter password: ")
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
        "username":username,
        "password":password,
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
                    print("That Username already exists, Please try another")
                    break
            if flag:
                return  # Stop the function if the username already exists

    except FileNotFoundError:
        accounts = []  # Treat accounts as an empty list if the file doesn't exist

    # If the username is new, add the new account information to the file
    with open("accounts.txt", "a") as file:
        file.write(f"{username},{password},{age},{gender},{contact_no},{email}\n")
    print(f"Okay, {username} is your username")
    print("Welcome, your account has been created successfully!")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    customers = load_data_from_customer()  # Use the loaded customer data

    for customer in customers:
        if customer["username"] == username and customer["password"] == password:
            print("Welcome back!")
            return

    print("Invalid username or password.")
    def customer_menu():
        while True:
            print("\nWelcome to the Bakery Management System!")
            print("1. Sign Up")
            print("2. Login")
            print("3. Browse Products")
            print("4. View Cart")
            print("5. Exit")

            option = input("Please select an option (1/2/3/4/5): ")

            if option == "1":
                create_account()
            elif option == "2":
                login()
            elif option == "3":
                browse_products()
            elif option == "4":
                view_cart()
            elif option == "5":
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid option, please try again.")

    def manage_account(customer):
        print("\n--- Manage Account ---")
        print(f"Username: {customer['username']}")
        print(f"Age: {customer['age']}")
        print(f"Gender: {customer['gender']}")
        print(f"Contact Number: {customer['contact_no']}")
        print(f"Email: {customer['email']}")
        print("\nIf you want to update your information, please select the 'Update Information' option.")

    def update_information(customer):
        print("\n--- Update Personal Information ---")
        print("1. Update Password")
        print("2. Update Contact Number")
        print("3. Update Email")
        print("4. Go Back")

        option = input("Select an option (1/2/3/4): ")

        if option == "1":
            new_password = input("Enter new password: ")
            customer["password"] = new_password
            print("Password updated successfully!")
        elif option == "2":
            new_contact_no = input("Enter new contact number: ")
            customer["contact_no"] = new_contact_no
            print("Contact number updated successfully!")
        elif option == "3":
            new_email = input("Enter new email: ")
            customer["email"] = new_email
            print("Email updated successfully!")
        elif option == "4":
            return
        else:
            print("Invalid option, please try again.")

        # Save the updated information
        customers = load_data_from_customer()
        for i, c in enumerate(customers):
            if c["username"] == customer["username"]:
                customers[i] = customer
                break
        save_data_to_customer(customers)
        print("Your information has been updated!")
    def browse_products():
        try:
            # Load the products from the JSON file
            with open("products.json", "r") as file:
                products = json.load(file)

            # Display the products to the customer
            print("\nAvailable Products:")
            for product in products:
                print(f"Name: {product['name']}")
                print(f"Price: ${product['price']}")
                print(f"Description: {product['description']}\n")

        except FileNotFoundError:
            print("Product data not found.")

    import json

    # Load products from the bakery section (your teammate's data)
    def load_products():
        try:
            with open("bakery_products.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Product data not found.")
            return []

    # Add items to cart
    def add_to_cart(cart, products):
        product_name = input("Enter the name of the product to add: ")
        quantity = int(input(f"Enter quantity for {product_name}: "))

        for product in products:
            if product['name'] == product_name:
                cart.append({
                    'name': product_name,
                    'quantity': quantity,
                    'price': product['price']
                })
                print(f"{product_name} added to your cart.")
                return

        print(f"Product {product_name} not found.")

    # Remove items from cart
    def remove_from_cart(cart):
        product_name = input("Enter the name of the product to remove: ")

        for item in cart:
            if item['name'] == product_name:
                cart.remove(item)
                print(f"{product_name} removed from your cart.")
                return

        print(f"Product {product_name} not found in your cart.")

    # Modify items in cart
    def modify_cart(cart):
        product_name = input("Enter the name of the product to modify: ")

        for item in cart:
            if item['name'] == product_name:
                new_quantity = int(input(f"Enter new quantity for {product_name}: "))
                item['quantity'] = new_quantity
                print(f"Quantity for {product_name} updated to {new_quantity}.")
                return

        print(f"Product {product_name} not found in your cart.")

    # Main function to manage the cart
    def cart_management():
        cart = []
        products = load_products()

        while True:
            print("\nCart Management:")
            print("1. Add to Cart")
            print("2. Remove from Cart")
            print("3. Modify Cart")
            print("4. View Cart")
            print("5. Exit")

            option = input("Please select an option (1/2/3/4/5): ")

            if option == "1":
                add_to_cart(cart, products)
            elif option == "2":
                remove_from_cart(cart)
            elif option == "3":
                modify_cart(cart)
            elif option == "4":
                print("\nYour Cart:")
                for item in cart:
                    print(
                        f"Product: {item['name']}, Quantity: {item['quantity']}, Price: ${item['price'] * item['quantity']}")
            elif option == "5":
                print("Exiting cart management.")
                break
            else:
                print("Invalid option, please try again.")
    def track_order():
        order_id = input("Enter your Order ID: ")

        try:
            with open("orders.json", "r") as file:
                orders = json.load(file)

            for order in orders:
                if order["order_id"] == order_id:
                    print(f"\nOrder ID: {order['order_id']}")
                    print(f"Status: {order['status']}")
                    print(f"Items: {order['items']}")
                    print(f"Total Price: ${order['total_price']}")
                    return

            print("Order not found. Please check your Order ID.")

        except FileNotFoundError:
            print("No orders found.")

# Run the customer function to start the program
create_customer_account()
customer_menu()
