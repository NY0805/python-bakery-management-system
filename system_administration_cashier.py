import json
import re
import system_administration


def load_data_from_cashier():
    try:
        file = open('cashier.txt', 'r')  # open the file and read
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


# Define the function that saves information to the file
def save_info(cashier):
    file = open('cashier.txt', 'w')  # open the file to write
    json.dump(cashier, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()


def cashier_accounts():
    cashier = load_data_from_cashier()

    cashier_name = input('\nName: ')
    while cashier_name in cashier:
        print('\n+--------------------------------------------------+')
        print('|⚠️ Warning: One person can only have one account! |')
        print('+--------------------------------------------------+')
        cashier_name = input('\nName: ')

    cashier_username = input('Username: ')
    while cashier_username in (cashier[cashier_name]['cashier_username'] for cashier_name in cashier):
        print('Username has been used. Please enter another username.')
        cashier_username = input('\nUsername: ')

    while True:
        cashier_password = input('Password: ')
        if cashier_password == 'securec@sh123':
            while True:
                try:
                    age = int(input('Age: '))
                    if age < 18 or age > 60:
                        print('\nThe required age is between 18 and 60.')
                        print('Please enter a valid age.')
                    else:
                        break  # Exit the loop if age is valid
                except ValueError:
                    print('\nPlease enter a valid age.')

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
                    break

            # update the dictionary with user input
            cashier[cashier_name] = {
                'cashier_username': cashier_username,
                'cashier_password': cashier_password,
                'age': age,
                'gender': gender,
                'contact_no': contact_no,
                'email': email
            }
            save_info(cashier)

            print(f'\n{cashier_username} is added.\n')  # let user know their information are saved
            print('--------------------------------------------------')
            print('Thank you for completing the personal information.')
            print('--------------------------------------------------')
            return False

        else:
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')


def system_administration_cashier():
    cashier = load_data_from_cashier()

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'SERVICES')
        print('-----------------------------------------------')
        print('1. add cashier(s)\n2. remove cashier(s)\n3. edit cashier(s)\n4. exit')

        manage_cashier = input('\nPlease choose a service:\n>>> ')

        if manage_cashier == '1':
            while True:
                cashier_accounts()
                cashier = load_data_from_cashier()

                while True:
                    add_more = input('Continue to add? (y=yes, n=no)\n>>> ')
                    if add_more == 'y':
                        break
                    elif add_more == 'n':
                        break
                    else:
                        print('\ninvalid input. Enter again.')
                if add_more == 'n':
                    print('Stop adding. Exiting to the service page......')
                    break

        elif manage_cashier == '2':
            while True:
                if len(cashier) <= 1:
                    print('To ensure the daily normal operation, you cannot remove the last cashier in the list. ')
                    break

                else:
                    print('\n-----------------------------------------------')
                    print('\t\t\t\t', '', 'Cashier list')
                    print('-----------------------------------------------')
                    for index, key in enumerate(cashier, start=1):
                        print(f'{index}. {key}')
                    print(f'{len(cashier) + 1}. cancel')

                    try:
                        index_of_cashier_to_remove = int(
                            input(f'Which baker do you want to remove? (or enter {len(cashier) + 1} to cancel)\n>>> '))
                        if index_of_cashier_to_remove == len(cashier) + 1:
                            print('Cancelling. Exiting to the service page......')
                            break

                        elif 1 <= index_of_cashier_to_remove <= len(cashier):
                            cashier_to_remove = list(cashier.keys())[index_of_cashier_to_remove - 1]
                            del cashier[cashier_to_remove]
                            save_info(cashier)
                            print(f'{cashier_to_remove} removed.\n')

                            while True:
                                remove_more = input('Continue remove? (y=yes, n=no)\n>>> ')
                                if remove_more == 'y':
                                    break

                                elif remove_more == 'n':
                                    break

                                else:
                                    print('\ninvalid input. Enter again.')

                            if remove_more == 'n':
                                print('Stop removing. Exiting to the service page......')
                                break

                        else:
                            print('Invalid input.\n')

                    except ValueError:
                        print('Invalid input. Please enter a number.\n')

        elif manage_cashier == '3':
            while True:
                print('\n-----------------------------------------------')
                print('\t\t\t\t', '', 'Cashier list')
                print('-----------------------------------------------')
                for cashier_list_index, cashier_list_key in enumerate(cashier, start=1):
                    print(f'{cashier_list_index}. {cashier_list_key}')
                print(f'{len(cashier) + 1}. cancel')

                try:
                    index_of_cashier_to_edit = int(input('\nWhich cashier do you want to edit? (or enter \"cancel\")\n>>> '))
                    if index_of_cashier_to_edit == len(cashier) + 1:
                        print('Cancelling. Exiting to the service page......')
                        break

                    elif 1 <= index_of_cashier_to_edit <= len(cashier):
                        selected_cashier = list(cashier.keys())[index_of_cashier_to_edit - 1]
                        while True:
                            print('\n-----------------------------------------------')
                            print(f'\t\t\t\t {selected_cashier}\'s data')
                            print('-----------------------------------------------')

                            for cashier_data_key, cashier_data_value in (cashier[selected_cashier].items()):
                                print(f'{cashier_data_key}: {cashier_data_value}')

                            attribute_of_cashier_data = input('\nWhich information do you want to modify? (or enter \"cancel\")\n>>> ')
                            if attribute_of_cashier_data in cashier[selected_cashier]:

                                while True:
                                    try:
                                        new_value = input(f'\nEnter new {attribute_of_cashier_data}: ')

                                        if attribute_of_cashier_data == 'cashier_username':
                                            if new_value in (cashier[baker_name]['baker_username'] for baker_name in cashier):
                                                print('Username has been used. Please enter another username.')
                                                continue

                                        elif attribute_of_cashier_data == 'cashier_password':
                                            if new_value != 'securec@sh123':
                                                print('Password incorrect. Please try again.')
                                                continue

                                        elif attribute_of_cashier_data == 'age':
                                            if int(new_value) < 18 or int(new_value) > 60:
                                                print('\nThe required age is between 18 and 60.')
                                                print('Please enter a valid age.')
                                                continue

                                        elif attribute_of_cashier_data == 'gender':
                                            if new_value not in ['f', 'm']:
                                                print('\nInvalid input. Please enter again.')
                                                continue
                                            elif new_value == 'f':
                                                new_value = 'female'

                                            else:
                                                new_value = 'male'

                                        elif attribute_of_cashier_data == 'contact_no':
                                            if not re.fullmatch(r'^\d{3}-\d{7}$', new_value):
                                                print('\nInvalid contact number. Please enter again.')
                                                continue

                                        elif attribute_of_cashier_data == 'email':  # define the format of email
                                            if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                                                                new_value):
                                                print('\nInvalid email. Please enter again.')
                                                continue

                                        cashier[selected_cashier][attribute_of_cashier_data] = new_value
                                        print(f'\n{attribute_of_cashier_data} of {selected_cashier} is updated.')
                                        save_info(cashier)
                                        break

                                    except ValueError:
                                        print('\nPlease enter a valid age.')

                            elif attribute_of_cashier_data == 'cancel':
                                print('Cancelling. Exiting to the cashier list......')
                                break

                            else:
                                print('\nData not found.')

                    else:
                        print('\nCashier not found.')

                except ValueError:
                    print('\nInvalid input. Please enter a number.')

        elif manage_cashier == '4':
            print('Exiting to role selection......')
            system_administration.system_administration()
            break

        else:
            print('invalid input.')


