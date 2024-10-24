import json  # import json text file to record data
import main
import baker_recipe
import baker_inventory_check
import baker_product_keeping
import baker_equipment_management
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


def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


baker_info = load_data_from_file()  # store the data that retrieved from file into baker_info
manager = load_data_from_manager()  # store the data that retrieved from file into manager


# baker account login function
def baker_accounts():

    print('')
    printed_centered('BAKER')
    baker_username = input('Username: ')  # ask for username
    if baker_username not in baker_info:  # continue looping if username not match with the name
        print('\n+----------------------------------------------------------+')
        print('|⚠️ You are not a baker, cannot access to baker privilege. |')
        print('+----------------------------------------------------------+\n')
        print('Exiting to Main Page......')
        return False

    else:
        baker_password = input('Password: ')  # ask for baker's password
        while len(baker_password) < 8 or len(baker_password) > 12:  # repeating the prompt to input when password length is not between 8-12 digits
            print('\n+---------------------------------------------------------------------------+')
            print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
            print('+---------------------------------------------------------------------------+\n')
            baker_password = input('Password: ')

        while baker_password != baker_info[baker_username]['baker_password']:  # continue to validate the password of baker after the password length is correct
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')
            baker_password = input('Password: ')

        print('\nLogin successfully!')  # login successfully if the password meet the 2 requirements above
        print(f"Welcome, baker {baker_username}!")

        while True:
            print('')
            printed_centered('BAKER PRIVILEGE')

            print('1. Recipe management\n'
                  '2. Inventory check\n'
                  '3. Product record-keeping\n'
                  '4. Equipment management\n'
                  '5. Back to Main page')

            #  collect the choice of user and execute corresponding functions
            choice = input('\nSelect a choice (1, 2, 3, 4, 5): \n>>> ')

            if choice == '1':
                baker_recipe.recipe_management()

            elif choice == '2':
                baker_inventory_check.recipe_lists()

            elif choice == '3':
                baker_product_keeping.product_management()

            elif choice == '4':
                baker_equipment_management.equipment_management()

            elif choice == '5':
                print('\nExiting to main page......')
                return False

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')
        #  display baker privilege


def baker_privilege():
    while True:
        print('')
        printed_centered('BAKER PRIVILEGE')

        print('1. Recipe management\n'
              '2. Inventory check\n'
              '3. Product record-keeping\n'
              '4. Equipment management\n'
              '5. Back to Main page')

        #  collect the choice of user and execute corresponding functions
        choice = input('\nSelect a choice (1, 2, 3, 4, 5): \n>>> ')

        if choice == '1':
            baker_recipe.recipe_management()

        elif choice == '2':
            baker_inventory_check.recipe_lists()

        elif choice == '3':
            baker_product_keeping.product_management()

        elif choice == '4':
            baker_equipment_management.equipment_management()

        elif choice == '5':
            print('\nExiting to main page......')
            return False

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


baker_accounts()
#baker_privilege()

hhh
