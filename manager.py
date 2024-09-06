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
def save_info(manager_info):
    file = open('manager.txt', 'w')  # open the file to write
    json.dump(manager_info, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def manager_accounts():
    manager_info = load_data_from_manager()  # initialize 'info' as the name of dictionary that store data loaded from file

    print('\n+----------------------------------------------------------------+')
    print('|⚠️ This is your FIRST TIME login, kindly complete your profile. |')
    print('+----------------------------------------------------------------+\n')

    manager_name = input('Name: ')
    while manager_name in manager_info:
        print('\n+--------------------------------------------------+')
        print('|⚠️ Warning: One person can only have one account! |')
        print('+--------------------------------------------------+\n')
        manager_name = input('Name: ')

    manager_username = input('Username: ')
    while manager_username in (manager_info[manager_name]['manager_username'] for manager_name in manager_info):
        print('\n+----------------------------------------------------------+')
        print('|⚠️ Username has been used. Please enter another username. |')
        print('+----------------------------------------------------------+\n')
        manager_username = input('Username: ')

    manager_password = 'd0ugh8o5s'
    print('Password: ', manager_password)
    print('\n+-------------------------------------------------------------------------------+')
    print('|💡 This is the unique password for manager. Keep confidential and REMEMBER it! |')
    print('+-------------------------------------------------------------------------------+\n')

    ''' while len(manager_password) < 8 or len(manager_password) > 12:
        print('\n+---------------------------------------------------------------------------+')
        print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
        print('+---------------------------------------------------------------------------+\n')
        manager_password = input('Password: ') '''

    while True:
        try:
            age = int(input('Age: '))
            if age < 18 or age > 60:
                print('\n+------------------------------------------+')
                print('|⚠️ The required age is between 18 and 60. |')
                print('+------------------------------------------+\n')
            else:
                break
        except ValueError:
            print('\n+-----------------------------+')
            print('|⚠️ Please enter a valid age. |')
            print('+-----------------------------+\n')

    while True:
        gender = input('Gender(m=male, f=female): ')
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
    print('\nInformation saved.')  # let user know their information are saved


# create a function for manager
def manager():
    manager_info = load_data_from_manager()  # initialize 'info' as the name of dictionary that store data loaded from file

    manager_name = input('\nName: ')
    if manager_name in manager_info:

        manager_username = input('Username: ')
        while manager_username != (manager_info[manager_name]['manager_username']):
            print('\n+-----------------------------------------------+')
            print('|⚠️ Username doesn\'t match. Please enter again. |')
            print('+-----------------------------------------------+\n')
            manager_username = input('Username: ')

        manager_password = input('Password: ')
        while manager_password != 'd0ugh8o5s':
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')
            manager_password = input('Password: ')

    else:
        manager_accounts()

    print('\nLogin successfully!')
    print('Welcome, manager', manager_name, '!')
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t', '', '', 'MANAGER PRIVILEGE')
        print('-----------------------------------------------')
        print('a. System administration\n'
              'b. Order management\n'
              'c. Financial management\n'
              'd. Inventory control\n'
              'e. Customer feedback\n'
              'f. Exit')

        choice = input('\nSelect a choice (a, b, c, d, e, f): \n>>> ')
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
            print('\nExiting to main page......\n')
            return False

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


