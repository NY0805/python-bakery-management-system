import re  # import the regular expressions(regex), a type of text pattern matching tool to check if a string contains the specified search pattern
import json  # import json text file to record data

import manager_customer_feedback
import manager_financial_management
import manager_notifications
import system_administration
import manager_order_management
import manager_inventory_control


# Define the function that loads manager data from the file
def load_data_from_manager():
    try:
        file = open('manager.txt', 'r')  # open the file and read
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


# Define the function that saves information to the file
def save_info(manager_info):
    file = open('manager.txt', 'w')  # open the file to write
    json.dump(manager_info, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


manager_info = load_data_from_manager()  # store the data that retrieved from file into manager_info


# manager account sign up page
def manager_accounts():

    print('\n+----------------------------------------------------------------+')
    print('|⚠️ This is your FIRST TIME login, kindly complete your profile. |')
    print('+----------------------------------------------------------------+\n')

    manager_name = input('Name: ')  # ask for manager name

    manager_username = input('Username: ')  # ask for manager username
    while manager_username in (manager_info[manager_name]['manager_username'] for manager_name in manager_info):  # continue looping if username not match with the name
        print('\n+----------------------------------------------------------+')
        print('|⚠️ Username has been used. Please enter another username. |')
        print('+----------------------------------------------------------+\n')
        manager_username = input('Username: ')

    manager_password = 'd0ugh8o5s'  # create a password specifically for manager
    print('Password: ', manager_password)
    print('\n+-------------------------------------------------------------------------------+')
    print('|💡 This is the unique password for manager. Keep confidential and REMEMBER it! |')
    print('+-------------------------------------------------------------------------------+\n')

    while True:
        try:
            age = int(input('Age: '))  # ask for manager age
            if age < 18 or age > 60:  # validate whether the age is in range between 18-60
                print('\n+------------------------------------------+')
                print('|⚠️ The required age is between 18 and 60. |')
                print('+------------------------------------------+\n')
            else:
                break
        except ValueError:  # error message appears when input is not an integer
            print('\n+-----------------------------+')
            print('|⚠️ Please enter a valid age. |')
            print('+-----------------------------+\n')

    while True:
        gender = input('Gender(m=male, f=female): ')  # ask for manager gender
        if gender not in ['f', 'm']:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+\n')
        else:
            if gender == 'f':
                gender = 'female'
                break
            else:
                gender = 'male'
                break

    contact_no = input('Contact number(xxx-xxxxxxx): ')  # ask for manager contact number
    while not re.fullmatch(r'^\d{3}-\d{7}$', contact_no):  # validate the contact number pattern
        print('\n+-----------------------------------------------+')
        print('|⚠️ Invalid contact number. Please enter again. |')
        print('+-----------------------------------------------+\n')
        contact_no = input('Contact number(xxx-xxxxxxx): ')

    email = input('Email: ')  # ask for manager email
    while not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):  # validate the email pattern
        print('\n+--------------------------------------+')
        print('|⚠️ Invalid email. Please enter again. |')
        print('+--------------------------------------+\n')
        email = input('Email: ')

    # update the dictionary with user input
    manager_info[manager_name] = {
        'manager_username': manager_username,
        'manager_password': manager_password,
        'age': age,
        'gender': gender,
        'contact_no': contact_no,
        'email': email
    }

    save_info(manager_info)
    print('\nInformation saved.')  # inform users about their information has been saved


# create a function for manager
def manager():

    print('\n----------------------------------------------------')
    print('\t\t\t\t\t', '', 'MANAGER')
    print('----------------------------------------------------')
    manager_name = input('Name: ')
    if manager_name in manager_info:

        manager_username = input('Username: ')
        while manager_username != (manager_info[manager_name]['manager_username']):
            print('\n+-----------------------------------------------+')
            print('|⚠️ Username doesn\'t match. Please enter again. |')
            print('+-----------------------------------------------+\n')
            manager_username = input('Username: ')

        manager_password = input('Password: ')
        while manager_password != 'd0ugh8o5s':  # check whether the manager password is correct
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')
            manager_password = input('Password: ')

    else:
        # prevent unauthorized user to access manager privilege
        print('\n+--------------------------------------------------------------+')
        print('|⚠️ You are not a manager, cannot access to manager privilege. |')
        print('+--------------------------------------------------------------+\n')
        while True:
            become_manager = input('Do you want to be a manager (y=yes, n=no)?\n>>> ')  # ask user if they want to be a manager
            if become_manager == 'y':
                if len(manager_info) == 1:
                    print('\n💡Sorry, the manager position is not vacant.')  # the request fallback to users when manager position is full
                    print('Exiting to Main page......')
                    return False
                else:
                    manager_accounts()  # the request succeed and call the first time login function when the manager position is empty
                    break

            elif become_manager == 'n':
                print('\nExiting to Main page......')
                return False
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+\n')

    print('\nLogin successfully!')  # login successfully if all the requirements in sign up and login page are fulfilled
    print('Welcome, manager', manager_name, '!')
    # display manager privilege
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t', '', '', 'MANAGER PRIVILEGE')
        print('-----------------------------------------------')
        print('a. System Administration\n'
              'b. Order Management\n'
              'c. Financial Management\n'
              'd. Inventory Control\n'
              'e. Customer Feedback\n'
              'f. Notifications\n'
              'g. Back to Main page')

        #  collect the choice of user and execute corresponding functions
        choice = input('\nSelect a choice (a, b, c, d, e, f, g): \n>>> ')
        if choice == 'a':
            system_administration.system_administration()

        elif choice == 'b':
            manager_order_management.order_management()

        elif choice == 'c':
            manager_financial_management.financial_management()

        elif choice == 'd':
            manager_inventory_control.inventory_control()

        elif choice == 'e':
            manager_customer_feedback.monitor_review()

        elif choice == 'f':
            manager_notifications.notification()

        elif choice == 'g':
            print('\nExiting to Main page......')
            return False

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


manager()


