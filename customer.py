import json
import re
import product_menu,order_tracking,product_review,cart_management


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
            product_menu.menu()
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


customer_menu()