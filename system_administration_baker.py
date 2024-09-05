import json
import re
import system_administration


def load_data_from_baker():
    try:
        file = open('baker.txt', 'r')  # open the file and read
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
def save_info(baker):
    file = open('baker.txt', 'w')  # open the file to write
    json.dump(baker, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()


def baker_accounts():
    baker = load_data_from_baker()

    baker_name = input('\nName: ')
    while baker_name in baker:
        print('\n+--------------------------------------------------+')
        print('|⚠️ Warning: One person can only have one account! |')
        print('+--------------------------------------------------+')
        baker_name = input('\nName: ')

    baker_username = input('Username: ')
    while baker_username in (baker[baker_name]['baker_username'] for baker_name in baker):
        print('Username has been used. Please enter another username.')
        baker_username = input('\nUsername: ')

    while True:
        baker_password = input('Password: ')
        if baker_password == 'bbb':
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
            baker[baker_name] = {
                'baker_username': baker_username,
                'baker_password': baker_password,
                'age': age,
                'gender': gender,
                'contact_no': contact_no,
                'email': email
            }
            save_info(baker)

            print(f'\n{baker_username} is added.\n')  # let user know their information are saved
            print('--------------------------------------------------')
            print('Thank you for completing the personal information.')
            print('--------------------------------------------------')
            return False

        else:
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')


def system_administration_baker():
    baker = load_data_from_baker()

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'SERVICES')
        print('-----------------------------------------------')
        print('1. add baker(s)\n2. remove baker(s)\n3. edit baker(s)\n4. exit')

        manage_baker = input('\nPlease choose a service:\n>>> ')

        if manage_baker == '1':
            while True:
                baker_accounts()

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

        elif manage_baker == '2':
            while True:
                if len(baker) <= 1:
                    print('To ensure the daily normal operation, you cannot remove the last baker in the list. ')
                    break

                else:
                    print('\n-----------------------------------------------')
                    print('\t\t\t\t', '', 'Baker list')
                    print('-----------------------------------------------')
                    for index, key in enumerate(baker, start=1):
                        print(f'{index}. {key}')

                    while True:
                        try:
                            index_of_baker_to_remove = int(input('Which baker do you want to remove? \n>>> '))
                            if 1 <= index_of_baker_to_remove <= len(baker):
                                baker_to_remove = list(baker.keys())[index_of_baker_to_remove - 1]
                                del baker[baker_to_remove]
                                save_info(baker)

                                print(f'{baker_to_remove} removed.\n')
                                while True:
                                    remove_more = input('Continue remove? (y=yes, n=no)\n>>> ')
                                    if remove_more == 'y':
                                        break

                                    elif remove_more == 'n':
                                        break

                                    else:
                                        print('\ninvalid input. Enter again.')

                                if remove_more == 'y':
                                    break
                                elif remove_more == 'n':
                                    print('Stop removing. Exiting to the service page......')
                                    break

                            else:
                                print('Invalid input.\n')

                        except ValueError:
                            print('Invalid input. Please enter a number.\n')

                    if remove_more == 'n':
                        break

        elif manage_baker == '3':
            while True:
                print('\n-----------------------------------------------')
                print('\t\t\t\t', '', 'Baker list')
                print('-----------------------------------------------')
                for baker_list_index, baker_list_key in enumerate(baker, start=1):
                    print(f'{baker_list_index}. {baker_list_key}')
                print(f'{len(baker)+ 1}. cancel')

                try:
                    index_of_baker_to_edit = int(input(f'\nWhich baker do you want to edit? (or enter {len(baker) + 1} to cancel)\n>>> '))
                    if index_of_baker_to_edit == len(baker) + 1:
                        break

                    elif 1 <= index_of_baker_to_edit <= len(baker):
                        selected_baker = list(baker.keys())[index_of_baker_to_edit - 1]
                        while True:
                            print('\n-----------------------------------------------')
                            print(f'\t\t\t\t {selected_baker}\'s data')
                            print('-----------------------------------------------')

                            for baker_data_key, baker_data_value in (baker[selected_baker].items()):
                                print(f'{baker_data_key}: {baker_data_value}')

                            attribute_of_baker_data = input('\nWhich information do you want to modify? (or enter \"cancel\")\n>>> ')
                            if attribute_of_baker_data in baker[selected_baker]:
                                new_value = input(f'\nEnter new {attribute_of_baker_data}: ')
                                baker[selected_baker][attribute_of_baker_data] = new_value
                                print(f'\n{attribute_of_baker_data} of {selected_baker} is updated.')
                                save_info(baker)

                            elif attribute_of_baker_data == 'cancel':
                                break

                            else:
                                print('\nData not found.')

                    else:
                        print('\nBaker not found.')

                except ValueError:
                    print('\nInvalid input. Please enter a number.')

        elif manage_baker == '4':
            print('Exiting to role selection......')
            system_administration.system_administration()
            break

        else:
            print('invalid input.')



