import re  # import the regular expressions(regex), a type of text pattern matching tool to check if a string contains the specified search pattern
import json  # import json text file to record data
import system_administration



# Define the function that loads data from the file
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
def save_info(info):

    file = open('manager.txt', 'w')  # open the file to write
    json.dump(info, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# create a function for manager
def manager():

    info = load_data_from_manager()  # initialize 'info' as the name of dictionary that store data loaded from file

    manager_username = input('Please enter your username: ')
    while True:
        manager_password = input('Please enter your password: ')
        if 7 < len(manager_password) < 13:
            if manager_username in info:

                if info[manager_username]['manager_password'] == manager_password:
                    print('\nLogin successfully!')
                    print('Welcome, manager ', manager_username, '!')
                    while True:
                        print(
                            '\n-----------------------------------------------\n'
                            '\t\t\t', '', '', 'MANAGER PRIVILEGE\n'
                            '-----------------------------------------------\n'
                            'a. system administration\n'
                            'b. order management\n'
                            'c. financial management\n'
                            'd. inventory control\n'
                            'e. customer feedback\n'
                            'f. Exit')
                        choice = input('Select a choice (a, b, c, d, e, f): \n>>> ')
                        if choice == 'a':
                            system_administration.system_administration()

                        elif choice == 'b':
                            print('enter again.')

                        elif choice == 'c':
                            print('enter again.')

                        elif choice == 'd':
                            print('enter again.')

                        elif choice == 'e':
                            print('enter again.')

                        elif choice == 'f':
                            print('Exiting to main page......')
                            return

                        else:
                            print('invalid input. Please enter again.')

                else:
                    print('\nInvalid password. Please try again.')
            else:
                print('------------------------------------------------------------------')
                print('', '', 'REMEMBER your username and password, they will be used later.')
                print('This is your FIRST TIME login, kindly complete your personal info.')
                print('------------------------------------------------------------------')
                while True:
                    try:
                        age = int(input('Age: '))
                        if age < 18 or age > 60:
                            print('\nThe required age is between 18 and 60.')
                            print('Please enter a valid age.')
                        else:
                            break  # Exit the loop if age is valid
                    except ValueError:
                        print('Please enter a valid age.')

                while True:
                    gender = input('Gender(m=male, f=female): ')
                    if gender not in ['f', 'm']:
                        print('\nInvalid input. Please enter again.')
                    elif gender == 'f':
                        gender = 'female'
                        break
                    else:
                        gender = 'male'
                        break  # Exit the loop if age is valid

                while True:
                    contact_no = input('Contact number(xxx-xxx xxxx): ')
                    pattern = r'^\d{3}-\d{7}$'  # define the format of contact number
                    if not re.fullmatch(pattern, contact_no):
                        print('\nInvalid contact number. Please enter again.')
                    else:
                        break  # Exit the loop if age is valid

                while True:
                    email = input('Email: ')
                    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # define the format of email
                    if not re.fullmatch(pattern, email):
                        print('\nInvalid email. Please enter again.')
                    else:
                        break  # Exit the loop if age is valid

                # update the dictionary with user input
                info[manager_username] = {
                    'manager_username': manager_username,
                    'manager_password': manager_password,
                    'age': age,
                    'gender': gender,
                    'contact_no': contact_no,
                    'email': email
                }
                save_info(info)
                print('Information saved.\n')  # let user know their information are saved
                print('--------------------------------------------------')
                print('Thank you for completing the personal information.')
                print('--------------------------------------------------')
                print('For security purpose, please log in again to access the system.\n')
                manager()

        else:
            print('\nInvalid password length. Please make sure it is between 8 to 12 digits!')


