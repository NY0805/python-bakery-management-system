import json
import re
import cart_management
import order_tracking
import customer_product_review
import customer_loyalty_rewards
import product_browsing


# Define the function that loads data from the file
def load_data_from_customer():
    try:
        with open('customer.txt', 'r') as file:  # use with statement to open the file
            content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
            if content:  # check if the file is not empty
                try:
                    return json.loads(content)  # parse the content as json format into python dictionary and return the content if successfully parsed
                except json.JSONDecodeError:
                    return {}  # return empty dictionary if the content does not parse successfully
            else:
                return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


# Function to save customer information to the customer.txt file
def save_info(customer_info):
    with open('customer.txt', 'w') as file:  # use with statement to open the file
        json.dump(customer_info, file, indent=4)  # convert the dictionary into JSON format


customer_info = load_data_from_customer()


def sign_up():
    customer_name = input("Name: ")
    customer_username = input("Username: ")

    if customer_username in [info['customer_username'] for info in customer_info.values()]:
        print('\n+--------------------------------------------------+')
        print('|⚠️ Warning: One person can only have one account! |')
        print('+--------------------------------------------------+')
        print('You already have an account. Directing to the login page......')
        login()
    else:
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
            gender = input('Gender (m=male, f=female, x=prefer not to say): ')
            if gender not in ['f', 'm', 'x']:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+\n')
            else:
                gender = 'female' if gender == 'f' else 'male' if gender == 'm' else 'prefer not to say'
                break

        contact_no = input('Contact number (xxx-xxxxxxx): ')
        while not re.fullmatch(r'^\d{3}-\d{7}$', contact_no):
            print('\n+-----------------------------------------------+')
            print('|⚠️ Invalid contact number. Please enter again. |')
            print('+-----------------------------------------------+\n')
            contact_no = input('Contact number (xxx-xxxxxxx): ')

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
            'address': address,
            'account_status': 'active',
            'loyalty_points': 0
        }

        save_info(customer_info)
        print('\nInformation saved.')
        print(f'Welcome, {customer_name}! Your account has been created successfully!\n')


def login():
    customer_name = input('\nName: ')

    # Load customer_info to check customer’s details and account status
    if customer_name in customer_info:
        # Check the account status of the customer
        if customer_info[customer_name]['account_status'] == 'inactive':
            print('\n+---------------------------------------------------------+')
            print('|⚠️ Your account is INACTIVE. Please contact the manager. |')
            print('+---------------------------------------------------------+\n')
            return None  # Exit the login process if the account status is inactive

        while True:  # Loop until the correct username is entered
            customer_username = input("Username: ")
            if customer_info[customer_name]['customer_username'] == customer_username:
                break  # Exit the loop if the username is correct
            else:
                print('\n+-------------------------------------------+')
                print('|⚠️ Incorrect username. Please enter again. |')
                print('+-------------------------------------------+\n')

        customer_password = input("Password: ")
        while customer_password != customer_info[customer_name]['customer_password']:
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')
            customer_password = input("Password: ")

        print(f'\nWelcome back, {customer_name}!\n')
        return customer_username  # Return the username after successful login
    else:
        print('\n+------------------------------------------------------------+')
        print('|⚠️ This is your FIRST TIME logging in, please create an account. |')
        print('+------------------------------------------------------------+')
        print('Directing to sign-up page......\n')
        sign_up()
        return None


# Function to update customer information
def update_personal_information():
    if not customer_info:
        print("No customer data available.")
        return

    while True:  # Loop until the user enters the correct username
        customer_username = input("Enter your username: ")

        # Check if the username exists in customer_info
        if customer_username in customer_info:
            customers = customer_info[customer_username]
            print("What do you want to update?")
            print("1. Password")
            print("2. Age")
            print("3. Gender")
            print("4. Contact Number")
            print("5. Email")
            print("6. Address")

            choice = input("Choose the field number to update: ")

            if choice == "1":
                while True:
                    new_password = input("Enter new password: ")
                    if len(new_password) < 8 or len(new_password) > 12:
                        print('\n+---------------------------------------------------------------------------+')
                        print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
                        print('+---------------------------------------------------------------------------+\n')
                    else:
                        customers["customer_password"] = new_password
                        break

            elif choice == "2":
                while True:  # Loop to ensure valid age input
                    try:
                        new_age = int(input("Enter new age: "))
                        if new_age >= 12:
                            customers["age"] = new_age
                            break
                        else:
                            print('\n+----------------------+')
                            print('|⚠️ You are under age. |')
                            print('+----------------------+\n')
                    except ValueError:
                        print('\n+-------------------------------------------+')
                        print('|⚠️ Invalid age. Please enter numbers only. |')
                        print('+-------------------------------------------+\n')

            elif choice == "3":
                while True:
                    new_gender = input("Select your gender (m=male, f=female, x=prefer not to say): ")
                    if new_gender in ['f', 'm', 'x']:
                        if new_gender == 'f':
                            customers["gender"] = 'female'
                        elif new_gender == 'm':
                            customers["gender"] = 'male'
                        else:
                            customers["gender"] = 'prefer not to say'
                        break
                    else:
                        print('\n+--------------------------------------+')
                        print('|⚠️ Invalid input. Please enter again. |')
                        print('+--------------------------------------+\n')

            elif choice == "4":
                while True:  # Loop to ensure valid contact number input
                    new_contact_no = input("Enter new contact number: ")
                    if re.fullmatch(r'^\d{3}-\d{7}$', new_contact_no):
                        customers["contact_no"] = new_contact_no
                        break
                    else:
                        print('\n+-----------------------------------------------+')
                        print('|⚠️ Invalid contact number. Please enter again. |')
                        print('+-----------------------------------------------+\n')

            elif choice == "5":
                while True:  # Loop to ensure valid email input
                    new_email = input("Enter new email: ")
                    if re.fullmatch(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}$', new_email):
                        customers["email"] = new_email
                        break
                    else:
                        print('\n+--------------------------------------+')
                        print('|⚠️ Invalid email. Please enter again. |')
                        print('+--------------------------------------+\n')

            elif choice == "6":
                new_address = input("Enter new address: ")
                customers["address"] = new_address

            else:
                print("\n+----------------------------+")
                print("|⚠️ Invalid choice selected.  |")
                print("|   Please choose a valid option (1-6). |")
                print("+----------------------------+\n")
                continue # Loop back to prompt the user for a valid option

            save_info(customer_info)  # Save updated customer information to file
            print("Your information has been updated.")
            break  # Exit after successful update

        else:
            print("Customer not found. Please enter a valid username.\n")


# Function to enable customer to manage their account
def account_management():
    customer_info = load_data_from_customer()

    if not customer_info:  # Check if customer data is loaded
        print("No customer data available.")
        return

    # Let customer enter their username
    customer_name = input("Please enter your name: ")

    # Check if the customer_name exists in the loaded customer data
    if customer_name in customer_info:
        print(f"Welcome, {customer_name}!")
        print("What would you like to do?")
        print("1. View Account Details")
        print("2. Delete Account")
        print("3. Exit to main menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Display account details
            customer = customer_info[customer_name]
            print("\n+---------------------------+")
            print(f"Username: {customer_name}")
            print(f"Password: {customer['customer_password']}")
            print(f"Age: {customer['age']}")
            print(f"Gender: {customer['gender']}")
            print(f"Contact No: {customer['contact_no']}")
            print(f"Email: {customer['email']}")
            print(f"Address: {customer['address']}")
            print(f"Account status: {customer['account_status']}")
            print(f"Loyalty points: {customer['loyalty_points']}")
            print("+---------------------------+\n")

        elif choice == "2":
            # Confirm account deletion
            confirm = input("Are you sure you want to delete your account? (y/n): ").lower()
            if confirm == 'y':
                del customer_info[customer_name]  # Remove the customer from the dictionary
                save_info(customer_info)  # Save the updated data back to the file
                print(f"Account '{customer_name}' has been deleted.")
            elif confirm == 'n':
                print("Account deletion canceled.")
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        elif choice == "3":
            return
        else:
            print("Invalid choice.")
    else:
        print(f"Account with the name '{customer_name}' not found.")


# Function to load customer data
def load_customer_data():
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


# Function to save customer data
def save_customer_data():
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


def customer_menu():
    logged_in_username = None  # Initialize as None, means that no user is logged in yet

    while True:
        print('\n----------------------------------------------------')
        print('\t\t\t\t\t', '', 'CUSTOMER')
        print('----------------------------------------------------')
        print('\n+---------------------------------------------------------+')
        print('|💡 Please "Sign Up" if you\'re logging in the first time. |')
        print('|   Please "Login" if you already have an account.       |')
        print('+---------------------------------------------------------+\n')

        print('\n-----------------------------------------------')
        print("WELCOME TO MORNING GLORY BAKERY!")
        print('-----------------------------------------------')
        print("1. Sign Up")
        print("2. Login")
        print("3. Browse Products")
        print("4. Shopping Cart")
        print("5. Order Tracking")
        print("6. Submit Review")
        print("7. View Loyalty Rewards")
        print("8. Update Personal Information")
        print("9. Manage Account")
        print("0. Exit")

        option = input("Please select an option (0-9): ")

        if option == "1":
            sign_up()
        elif option == "2":
            logged_in_username = login()
        elif option == "3":
            product_browsing.browse_products()
        elif option == "4":
            if logged_in_username:
                cart_management.shopping_cart(logged_in_username)
            else:
                print("You need to log in first.")
        elif option == "5":
            order_tracking.order_tracking()
        elif option == "6":
            if logged_in_username:  # Check if the user is logged in
                customer_product_review.submitted_review(logged_in_username)
            else:
                print("You need to log in first to submit a review.")
        elif option == "7":
            customer_loyalty_rewards.loyalty_rewards()
        elif option == "8":
            update_personal_information()
        elif option == "9":
            if logged_in_username:
                account_management()
            else:
                print("You need to log in first to manage your account.")
        elif option == "0":
            print("Thank you for visiting our bakery. Goodbye!")
            break
        else:
            print("|⚠️ Invalid option, please try again.|")


