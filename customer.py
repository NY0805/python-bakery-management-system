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

def save_data_to_customer(customers):
    with open('customers.txt', 'w') as file:
        json.dump(customers, file)  # Save the customer data back to the file

def create_customer_account():
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

    # Run the customer function to start the program
    customer_menu()
