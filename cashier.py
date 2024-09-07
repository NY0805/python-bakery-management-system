import json  # import json text file to record data


# Define the function that loads data from the file
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


# Define the function that saves information to the file
def save_info(cashier_info):

    file = open('cashier.txt', 'w')  # open the file to write
    json.dump(cashier_info, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def cashier_accounts():
    cashier_info = load_data_from_file()  # initialize 'info' as the name of dictionary that store data loaded from file

    cashier_name = input('Name: ')
    if cashier_name in cashier_info:
        cashier_username = input('Username: ')
        while cashier_username != (cashier_info[cashier_name]['cashier_username']):
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect username. Please enter again. |')
            print('+-------------------------------------------+\n')
            cashier_username = input('Username: ')

        cashier_password = input('Password: ')
        while len(cashier_password) < 8 or len(cashier_password) > 12:
            print('\n+---------------------------------------------------------------------------+')
            print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
            print('+---------------------------------------------------------------------------+\n')
            cashier_password = input('Password: ')

        while cashier_password != 'securec@sh$':
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')
            cashier_password = input('Password: ')

        print('\nLogin successfully!')
        print('Welcome, cashier', cashier_name, '!')
        while True:
            print('\n-----------------------------------------------')
            print('\t\t\t', '', '', 'CASHIER PRIVILEGE')
            print('-----------------------------------------------')
            print('a. Product display\n'
                  'b. Manage discount\n'
                  'c. Transaction completion\n'
                  'd. Reporting\n'
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
                print('\nExiting to main page......\n')
                return False

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

    else:
        print('\n+----------------------------------------------------------------------+')
        print('|⚠️ You are unable to access the system because you are not our cashier. |')
        print('|   If you are keen to join our team, kindly contact the manager.        |')
        print('+----------------------------------------------------------------------+\n')
        print('Exiting to main page......\n')
