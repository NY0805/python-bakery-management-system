import json  # import json text file to record data

import cashier_discount_management
import product_menu
import cashier_sales_report

import cashier_transaction_completion
from manager import load_data_from_manager

# Define the function that loads cashier data from the file
def load_data_from_file():
    try:
        file = open('cashier.txt', 'r')  # open the file and read
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


# Define the function that saves cashier data to the file
def save_info(cashier_info):

    file = open('cashier.txt', 'w')  # open the file to write
    json.dump(cashier_info, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


cashier_info = load_data_from_file()  # store the data that retrieved from file into cashier_info
manager = load_data_from_manager()  # store the data that retrieved from file into manager


# cashier account login function
def cashier_accounts():

    print('')
    printed_centered('CASHIER')
    cashier_username = input('Username: ')  # ask for username
    if cashier_username not in cashier_info:  # continue looping if username not match with the name
        print('\n+--------------------------------------------------------------+')
        print('|⚠️ You are not a cashier, cannot access to cashier privilege. |')
        print('+--------------------------------------------------------------+\n')
        print('Exiting to Main Page......')
        return False

    else:
        cashier_password = input('Password: ')  # ask for cashier's password
        while len(cashier_password) < 8 or len(cashier_password) > 12:  # repeating the prompt to input when password length is not between 8-12 digits
            print('\n+---------------------------------------------------------------------------+')
            print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
            print('+---------------------------------------------------------------------------+\n')
            cashier_password = input('Password: ')

        while cashier_password != cashier_info[cashier_username]['cashier_password']:  # continue to validate the password of baker after the password length is correct
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')
            cashier_password = input('Password: ')

        print('\nLogin successfully!')  # login successfully if the password meet the 2 requirements above
        print('Welcome, cashier', cashier_username, '!')
        #  display cashier privilege
        while True:
            print('')
            printed_centered('CASHIER PRIVILEGE')
            print('a. Product display\n'
                  'b. Manage discount\n'
                  'c. Transaction completion\n'
                  'd. Reporting\n'
                  'e. Back to Main page')

            #  collect the choice of user and execute corresponding functions
            choice = input('\nSelect a choice (a, b, c, d, e): \n>>> ')

            if choice == 'a':
                product_menu.menu()

            elif choice == 'b':
                cashier_discount_management.manage_discounts()

            elif choice == 'c':
                cashier_transaction_completion.manual_generate_receipt()

            elif choice == 'd':
                cashier_sales_report.generate_sales_report()

            elif choice == 'e':
                print('\nExiting to main page......')
                return False

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

cashier_accounts()