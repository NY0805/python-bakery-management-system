import json  # import json text file to record data
from manager import load_data_from_manager

# Define the function that loads baker data from the file
def load_data_from_file():
    try:
        file = open('baker.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # check if the file is not empty
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


baker_info = load_data_from_file()  # store the data that retrieved from file into baker_info
manager = load_data_from_manager()  # store the data that retrieved from file into manager


# baker account login function
def baker_accounts():

    print('\n----------------------------------------------------')
    print('\t\t\t\t\t', '', 'BAKER')
    print('----------------------------------------------------')
    baker_name = input('Name: ')  # ask for baker name
    if baker_name in baker_info:  # check if baker name in the baker_info
        baker_username = input('Username: ')  # ask for username
        while baker_username != (baker_info[baker_name]['baker_username']):  # continue looping if username not match with the name
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect username. Please enter again. |')
            print('+-------------------------------------------+\n')
            baker_username = input('Username: ')

        baker_password = input('Password: ')  # ask for baker password
        while len(baker_password) < 8 or len(baker_password) > 12:  # repeating the prompt to input when password length is not between 8-12 digits
            print('\n+---------------------------------------------------------------------------+')
            print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
            print('+---------------------------------------------------------------------------+\n')
            baker_password = input('Password: ')

        while baker_password != 'b@k3rm4st3r!':  # continue to validate the password of baker after the password length is correct
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')
            baker_password = input('Password: ')

        print('\nLogin successfully!')  # login successfully if the password meet the 2 requirements above
        print('Welcome, baker', baker_name, '!')
        #  display baker privilege
        while True:
            print('\n-----------------------------------------------')
            print('\t\t\t', '', '', 'BAKER PRIVILEGE')
            print('-----------------------------------------------')
            print('a. Recipe management\n'
                  'b. Inventory check\n'
                  'c. Product record-keeping\n'
                  'd. Equipment management\n'
                  'e. Exit')

            #  collect the choice of user and execute corresponding functions
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
                print('\nExiting to main page......')
                return False

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

    # notify users they are not a baker if their names not in baker_info
    else:
        print('\n+----------------------------------------------------------+')
        print('|⚠️ You are not a baker, cannot access to baker privilege. |')
        print('+----------------------------------------------------------+\n')
        while True:
            become_baker = input('Do you want to be a baker (y=yes, n=no)?\n>>> ')  # ask users if they want to be a baker
            if become_baker == 'y':
                print('\nPlease contact manager by the methods below👇 to register as a cashier. Upon approval, you can log in again.')
                for manager_details in manager.values():
                    print(
                        f'✉️ {manager_details["email"]}\n📞 {manager_details["contact_no"]}\n')  # provide contact details of manager
                print('Exiting to main page......')
                break
            elif become_baker == 'n':
                break
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+\n')







