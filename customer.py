import json

def create_account():
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
        with open('accounts.txt', 'r') as file:
            accounts = file.readlines()
            # Check to see whether the username is already in use
            for account in accounts:
                stored_username = account.split(',')[0]
                if stored_username == username:
                    print("Username already exists, please try another.")
                    return
    except FileNotFoundError:
        # If the file doesn't exist, treat it as an empty file
        accounts = []

    # If the username is new, add the new account information
    with open('accounts.txt', 'a') as file:
        file.write(f"{username},{password},{personal_info['age']},{personal_info['gender']},{personal_info['contact_no']},{personal_info['email']}\n")

    print("Welcome,your account has been created successfully!")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        with open("customers.json", "r") as file:
            customers = json.load(file)
    except FileNotFoundError:
        print("No accounts found. Please create an account first.")
        return

    for customer in customers:
        if customer["username"] == username and customer["password"] == password:
            print("Login successful!")
            return

    print("Invalid username or password.")
    def customer():
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

    # Run the customer function to start the program
    customer()
