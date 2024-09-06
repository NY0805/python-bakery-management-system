# Account login
# Recipe Management: Create, update, and delete digital recipes.
# Inventory Check: Verify availability of required ingredients.
# Production Record-keeping: Record production quantities, batch numbers, and expiration dates.
# Equipment Management: Report equipment malfunctions or maintenance

import re  # import the regular expressions(regex), a type of text pattern matching tool to check if a string contains the specified search pattern
import json  # import json text file to record data

# Define the function that loads data from the file
def load_data_from_file():
    try:
        file = open('baker.txt', 'r')  # open the file and read
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
def save_info(baker_info):

    file = open('baker.txt', 'w')  # open the file to write
    json.dump(baker_info, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def baker_accounts():
    baker_info = load_data_from_file()  # initialize 'info' as the name of dictionary that store data loaded from file

    baker_name = input('Name: ')
    if baker_name in baker_info:
        baker_username = input('Username: ')
        while baker_username != (baker_info[baker_name]['baker_username']):
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect username. Please enter again. |')
            print('+-------------------------------------------+\n')
            baker_username = input('Username: ')

        baker_password = input('Password: ')
        while len(baker_password) < 8 or len(baker_password) > 12:
            print('\n+---------------------------------------------------------------------------+')
            print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
            print('+---------------------------------------------------------------------------+\n')
            baker_password = input('Password: ')

        while baker_password != 'b@k3rm4st3r!':
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')
            baker_password = input('Password: ')

        print('\nLogin successfully!')
        print('Welcome, baker', baker_name, '!')
        while True:
            print('\n-----------------------------------------------')
            print('\t\t\t', '', '', 'BAKER PRIVILEGE')
            print('-----------------------------------------------\n')
            print('a. Recipe management\n'
                  'b. Inventory check\n'
                  'c. Product record-keeping\n'
                  'd. Equipment management\n'
                  'e. Exit')

            choice = input('\nSelect a choice (a, b, c, d, e): \n>>> ')

            if choice == 'a':
                print('in progress a')

            elif choice == 'b':
                print('in progress b')

            elif choice == 'c':
                print('in progress c')

            elif choice == 'd':
                print('in progress d')

            elif choice == 'e':
                print('Exiting to main page......')
                return False

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

    else:
        print('\n+----------------------------------------------------------------------+')
        print('|⚠️ You are unable to access the system because you are not our baker. |')
        print('|   If you are keen to join our team, kindly contact the manager.      |')
        print('+----------------------------------------------------------------------+\n')
        print('Exiting to main page......\n')







