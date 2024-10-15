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
        return customer_username  # Return the username after successful login
    else:
        print('\n+------------------------------------------------------------+')
        print('|⚠️ This is your FIRST TIME login, please create an account. |')
        print('+------------------------------------------------------------+')
        print('Directing to sign up page......\n')
        sign_up()
        return None  # Return None if sign-up is initiated


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

    customer_username = input("Enter your name: ")

    # Check if the username exists in customer_info
    if customer_username in customer_info:
        customers = customer_info[customer_username]  # Access the user's info dictionary
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
                        break  # Exit the loop on success
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
                    customers["gender"] = 'female'
                elif new_gender == 'm':
                    customers["gender"] = 'male'
                else:
                    customers["gender"] = 'prefer not to say'
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
            return

        save_info(customer_info)  # Save the entire customer_info dictionary
        print("Your information has been updated.")
    else:
        print("Customer not found.")


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

def customer_menu():
    logged_in_username = None  # Initialize username

    while True:
        print('\n-----------------------------------------------')
        print("WELCOME TO MORNING GLORY BAKERY!")
        print('\n-----------------------------------------------')
        print("1. Sign Up")
        print("2. Login")
        print("3. Browse Products")
        print("4. View Cart")
        print("5. Order Tracking")
        print("6. Submit Review")
        print("7. View Loyalty Rewards")
        print("8. Update Personal Information")
        print("0. Exit")

        option = input("Please select an option (0-9): ")

        if option == "1":
            sign_up()
        elif option == "2":
            logged_in_username = login()  # Update the username variable
        elif option == "3":
            product_browsing.browse_products()
        elif option == "4":
            cart_management.shopping_cart()
        elif option == "5":
            order_tracking.order_tracking()
        elif option == "6":
            if logged_in_username:  # Check if the user is logged in
                customer_product_review.submit_review(logged_in_username)  # Pass the logged-in username
            else:
                print("You need to log in first to submit a review.")
        elif option == "7":
            customer_loyalty_rewards.view_loyalty_rewards()
        elif option == "8":
           update_personal_information()
        elif option == "0":
            print("Thank you for visiting our bakery. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


customer_menu()