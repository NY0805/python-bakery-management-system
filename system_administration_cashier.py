import json
import re
import system_administration


# Define the function that loads cashier data from the file
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


# Define the function that saves cashier data to the file
def save_info(cashier):
    file = open('cashier.txt', 'w')  # open the file to write
    json.dump(cashier, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()


def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


# define the function to register cashiers
def cashier_accounts():
    cashier = load_data_from_cashier()  # store the data that retrieved from file into cashier

    cashier_username = input('Username: ')  # ask for cashier's username
    while cashier_username in (cashier[cashier_name]['cashier_username'] for cashier_name in cashier):  # continue looping if there is a duplication of username
        print('\n+----------------------------------------------------------+')
        print('|⚠️ Username has been used. Please enter another username. |')
        print('+----------------------------------------------------------+')
        cashier_username = input('\nUsername: ')

    while True:
        cashier_password = input('Password: ')  # set the password for cashier
        if cashier_password == 'securec@sh123':
            while True:
                try:
                    age = int(input('Age: '))  # ask for cashier's age
                    if age < 18 or age > 60:  # check if the age is between 18 - 60
                        print('\n+--------------------------------------------------------------------+')
                        print('|⚠️ The required age is between 18 and 60. Please enter a valid age. |')
                        print('+--------------------------------------------------------------------+\n')
                    else:
                        break  # exit the loop if age is valid
                except ValueError:
                    print('\n+-----------------------------+')
                    print('|⚠️ Please enter a valid age. |')
                    print('+-----------------------------+\n')

            while True:
                gender = input('Gender(m=male, f=female): ')  # ask for cashier's gender
                if gender not in ['f', 'm']:
                    print('\n+--------------------------------------+')
                    print('|⚠️ Invalid input. Please enter again. |')
                    print('+--------------------------------------+\n')
                elif gender == 'f':
                    gender = 'female'
                    break
                else:
                    gender = 'male'
                    break

            while True:
                contact_no = input('Contact number(xxx-xxxxxxx): ')  # ask for cashier's contact number
                if not re.fullmatch(r'^\d{3}-\d{7}$', contact_no):  # check if the contact number match the specific pattern
                    print('\n+-----------------------------------------------+')
                    print('|⚠️ Invalid contact number. Please enter again. |')
                    print('+-----------------------------------------------+\n')
                else:
                    break

            while True:
                email = input('Email: ')  # ask for cashier's email
                if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):  # check if the email match the specific pattern
                    print('\n+--------------------------------------+')
                    print('|⚠️ Invalid email. Please enter again. |')
                    print('+--------------------------------------+\n')
                else:
                    break

            # update the dictionary with user input
            cashier[cashier_username] = {
                'cashier_username': cashier_username,
                'cashier_password': cashier_password,
                'age': age,
                'gender': gender,
                'contact_no': contact_no,
                'email': email
            }
            save_info(cashier)

            print(f'\n{cashier_username} is added.\n')  # inform user that their information is saved
            return False

        else:
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')


# define the function to manage cashier
def system_administration_cashier():
    cashier = load_data_from_cashier()  # store the data that retrieved from file into cashier

    while True:
        print('')
        printed_centered('SERVICES')
        print('1. Add Cashier(s)\n2. Remove Cashier(s)\n3. Update Cashier(s)\n4. Back to Manager Privilege')  # provide the option for cashier management

        manage_cashier = input('\nPlease choose a service:\n>>> ')

        if manage_cashier == '1':  #add cashier
            if len(cashier) == 2:
                print('\nThe cashier position is currently full.')
            else:
                while True:
                    print('')
                    printed_centered('NEW CASHIER ENTRY FORM')
                    cashier_accounts()  # fill up the details of cashier to complete the registration
                    cashier = load_data_from_cashier()  # read the information of cashier again from file (if don't put, the data will not save into dictionary)

                    while True:
                        add_more = input('Continue to add? (y=yes, n=no)\n>>> ')  # after one cashier has been added, ask user if they want continue adding
                        if add_more == 'y':
                            if len(cashier) == 2:
                                print('\nThe cashier position is currently full.')
                                break
                            else:
                                break
                        elif add_more == 'n':
                            break
                        else:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+\n')
                    if add_more == 'n':
                        print('\nStop adding. Exiting to Services page......')
                        break

        elif manage_cashier == '2':  # remove cashier
            while True:
                if len(cashier) <= 1:  # if the current cashier is 1, prevent user from removing the last cashier to ensure the daily operation of the bakery
                    print('\n+---------------------------------------------------------------------------------------+')
                    print('|💡 To ensure the daily normal operation, you cannot remove the last cashier in the list. |')
                    print('+---------------------------------------------------------------------------------------+\n')
                    break

                else:  # if baker more than 1
                    print('')
                    printed_centered('CASHIER LIST')
                    index = 1
                    for key in cashier:
                        print(f'{index}. {key}')
                        index += 1
                    print(f'{len(cashier) + 1}. cancel')

                    try:
                        index_of_cashier_to_remove = int(
                            input(f'\nWhich cashier do you want to remove? (or enter {len(cashier) + 1} to cancel)\n>>> '))
                        if index_of_cashier_to_remove == len(cashier) + 1:  # cancel the process
                            print('\nCancelling. Exiting to Services page......')
                            break

                        elif 1 <= index_of_cashier_to_remove <= len(cashier):
                            cashier_to_remove = list(cashier.keys())[index_of_cashier_to_remove - 1]  # identify cashier to remove by accesing the index of key of cashier
                            del cashier[cashier_to_remove]  # delete the selected cashier
                            save_info(cashier)
                            print(f'\n{cashier_to_remove} removed.\n')  # inform user that the selected cashier is removed successfully

                            while True:
                                remove_more = input('Continue remove? (y=yes, n=no)\n>>> ')  # ask user if they want to continue removing
                                if remove_more == 'y':
                                    break

                                elif remove_more == 'n':
                                    break

                                else:
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter again. |')
                                    print('+--------------------------------------+\n')

                            if remove_more == 'n':
                                print('\nStop removing. Exiting to Services page......')
                                break

                        else:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+\n')

                    except ValueError:
                        print('\n+-----------------------------------------+')
                        print('|⚠️ Invalid input. Please enter a number. |')
                        print('+-----------------------------------------+\n')

        elif manage_cashier == '3':  # update cashier
            while True:
                print('')
                printed_centered('CASHIER LIST')
                index = 1
                for cashier_list_key in cashier:
                    print(f'{index}. {cashier_list_key}')
                    index += 1
                print(f'{len(cashier) + 1}. cancel')

                try:
                    index_of_cashier_to_edit = int(
                        input(f'\nWhich cashier do you want to edit? (or enter {len(cashier) + 1} to cancel)\n>>> '))
                    if index_of_cashier_to_edit == len(cashier) + 1:
                        print('\nCancelling. Exiting to Services page......')
                        break

                    elif 1 <= index_of_cashier_to_edit <= len(cashier):
                        selected_cashier = list(cashier.keys())[index_of_cashier_to_edit - 1]  # identify the selected cashier to update
                        while True:
                            print('\n-----------------------------------------------')
                            print(f'\t\t\t\t {selected_cashier.upper()}\'S DATA')
                            print('-----------------------------------------------')

                            for cashier_data_key, cashier_data_value in (cashier[selected_cashier].items()):
                                print(f'{cashier_data_key}: {cashier_data_value}')  # print the details of cashier and replace the underscore with a space

                            attribute_of_cashier_data = input('\nWhich information do you want to update? (or enter \"cancel\")\n>>> ')
                            if attribute_of_cashier_data in cashier[selected_cashier]:  # check if the attribute inputted found in cashier's data

                                while True:
                                    if attribute_of_cashier_data == 'cashier_password':
                                        print('\n+------------------------------------------------------------------------+')
                                        print('|⚠️ This password is created by manager. You are not allow to change it. |')
                                        print('+------------------------------------------------------------------------+')
                                        break
                                    else:
                                        try:
                                            new_value = input(f'\nEnter new {attribute_of_cashier_data}: ')

                                            if attribute_of_cashier_data == 'cashier_username':
                                                if new_value in (cashier[cashier_name]['cashier_username'] for cashier_name in cashier):  # if new value same with the current username in file, duplication occurs
                                                    print('\n+----------------------------------------------------------+')
                                                    print('|⚠️ Username has been used. Please enter another username. |')
                                                    print('+----------------------------------------------------------+')
                                                    continue

                                            elif attribute_of_cashier_data == 'age':
                                                if int(new_value) < 18 or int(new_value) > 60:  # check if the age is between 18 - 60
                                                    print('\n+--------------------------------------------------------------------+')
                                                    print('|⚠️ The required age is between 18 and 60. Please enter a valid age. |')
                                                    print('+--------------------------------------------------------------------+')
                                                    continue

                                            elif attribute_of_cashier_data == 'gender':
                                                if new_value not in ['f', 'm']:
                                                    print('\n+--------------------------------------+')
                                                    print('|⚠️ Invalid input. Please enter again. |')
                                                    print('+--------------------------------------+')
                                                    continue
                                                elif new_value == 'f':
                                                    new_value = 'female'

                                                else:
                                                    new_value = 'male'

                                            elif attribute_of_cashier_data == 'contact_no':
                                                if not re.fullmatch(r'^\d{3}-\d{7}$', new_value):  # check if the contact number match the specific pattern
                                                    print('\n+-----------------------------------------------+')
                                                    print('|⚠️ Invalid contact number. Please enter again. |')
                                                    print('+-----------------------------------------------+')
                                                    continue

                                            elif attribute_of_cashier_data == 'email':  # define the format of email
                                                if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', new_value):  # check if the email match the specific pattern
                                                    print('\n+--------------------------------------+')
                                                    print('|⚠️ Invalid email. Please enter again. |')
                                                    print('+--------------------------------------+')
                                                    continue

                                            cashier[selected_cashier][attribute_of_cashier_data] = new_value  # update the value of attributes
                                            print(f'\n{attribute_of_cashier_data} of {selected_cashier} is updated.')  # inform user that the information is updated
                                            save_info(cashier)
                                            break

                                        except ValueError:
                                            print('\n+-----------------------------+')
                                            print('|⚠️ Please enter a valid age. |')
                                            print('+-----------------------------+')

                            elif attribute_of_cashier_data == 'cancel':
                                print('\nCancelling. Exiting to Cashier List......')
                                break

                            else:
                                print('\n❗Data not found.')  # selected attribute not found

                    else:
                        print('\n❗Cashier not found.')  # selected cashier not found

                except ValueError:
                    print('\n+-----------------------------------------+')
                    print('|⚠️ Invalid input. Please enter a number. |')
                    print('+-----------------------------------------+')

        elif manage_cashier == '4':  # return back to the previous page
            print('\nExiting to Role Management......')
            system_administration.system_administration()
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

