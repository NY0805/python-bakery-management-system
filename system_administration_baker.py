import json
import re
import system_administration


# Define the function that loads baker data from the file
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


# Define the function that saves baker data to the file
def save_info(baker):
    file = open('baker.txt', 'w')  # open the file to write
    json.dump(baker, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()


# define the function to register bakers
def baker_accounts():
    baker = load_data_from_baker()  # store the data that retrieved from file into baker

    baker_username = input('Username: ')  # ask for baker's username
    while baker_username in (baker[baker_name]['baker_username'] for baker_name in baker):  # continue looping if there is a duplication of username
        print('\n+----------------------------------------------------------+')
        print('|⚠️ Username has been used. Please enter another username. |')
        print('+----------------------------------------------------------+')
        baker_username = input('\nUsername: ')

    while True:
        baker_password = input('Password: ')  # set the password for baker
        if baker_password == 'b@k3rm4st3r!':
            while True:
                try:
                    age = int(input('Age: '))  # ask for baker's age
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
                gender = input('Gender(m=male, f=female): ')  # ask for baker's gender
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
                contact_no = input('Contact number(xxx-xxxxxxx): ')  # ask for baker's contact number
                if not re.fullmatch(r'^\d{3}-\d{7}$', contact_no):  # check if the contact number match the specific pattern
                    print('\n+-----------------------------------------------+')
                    print('|⚠️ Invalid contact number. Please enter again. |')
                    print('+-----------------------------------------------+\n')
                else:
                    break

            while True:
                email = input('Email: ') # ask for baker's email
                if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):  # check if the email match the specific pattern
                    print('\n+--------------------------------------+')
                    print('|⚠️ Invalid email. Please enter again. |')
                    print('+--------------------------------------+\n')
                else:
                    break

            # update the dictionary with user input
            baker[baker_username] = {
                'baker_username': baker_username,
                'baker_password': baker_password,
                'age': age,
                'gender': gender,
                'contact_no': contact_no,
                'email': email
            }
            save_info(baker)

            print(f'\n{baker_username} is added.\n')  # inform user that the information is saved
            return False

        else:
            print('\n+-------------------------------------------+')
            print('|⚠️ Incorrect password. Please enter again. |')
            print('+-------------------------------------------+\n')


# define the function to manage baker
def system_administration_baker():
    baker = load_data_from_baker()  # store the data that retrieved from file into baker

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'SERVICES')
        print('-----------------------------------------------')
        print('1. Add Baker(s)\n2. Remove Baker(s)\n3. Update Baker(s)\n4. Back to Role Management')  # provide the option for baker management

        manage_baker = input('\nPlease choose a service:\n>>> ')

        if manage_baker == '1':  # add baker
            if len(baker) == 2:
                print('\nThe baker position is currently full.')
            else:
                while True:
                    print('\n-----------------------------------------------')
                    print('\t\t\tNEW BAKER ENTRY FORM')
                    print('-----------------------------------------------')
                    baker_accounts()  # fill up the details of baker to complete the registration
                    baker = load_data_from_baker()  # read the information of baker again from file (if don't put, the data will not save into dictionary)

                    while True:
                        add_more = input('Continue to add? (y=yes, n=no)\n>>> ')  # after one baker has been added, ask user if they want continue adding
                        if add_more == 'y':
                            if len(baker) == 2:
                                print('\nThe baker position is currently full.')
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
                    elif add_more == 'y':
                        break

        elif manage_baker == '2':  # remove baker
            while True:
                if len(baker) <= 1:  # if the current baker is 1, prevent user from removing the last baker to ensure the daily operation of the bakery
                    print('\n+---------------------------------------------------------------------------------------+')
                    print('|💡 To ensure the daily normal operation, you cannot remove the last baker in the list. |')
                    print('+---------------------------------------------------------------------------------------+\n')
                    break

                else:  # if baker more than 1
                    print('\n-----------------------------------------------')
                    print('\t\t\t\t', '', 'BAKER LIST')
                    print('-----------------------------------------------')
                    index = 1
                    for key in baker:
                        print(f'{index}. {key}')
                        index += 1
                    print(f'{len(baker) + 1}. cancel')

                    try:
                        index_of_baker_to_remove = int(
                            input(f'\nWhich baker do you want to remove? (or enter {len(baker) + 1} to cancel)\n>>> '))
                        if index_of_baker_to_remove == len(baker) + 1:  # cancel the process
                            print('\nCancelling. Exiting to Services page......')
                            break

                        elif 1 <= index_of_baker_to_remove <= len(baker):
                            baker_to_remove = list(baker.keys())[index_of_baker_to_remove - 1]  # identify baker to remove by accesing the index of key of baker
                            del baker[baker_to_remove]  # delete the selected baker
                            save_info(baker)
                            print(f'\n{baker_to_remove} is removed.\n')  # inform user that the selected baker is removed successfully

                            while True:
                                remove_more = input('Continue to remove? (y=yes, n=no)\n>>> ')  # ask user if they want to continue removing
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

        elif manage_baker == '3':  # update baker
            while True:
                print('\n-----------------------------------------------')
                print('\t\t\t\t', '', 'BAKER LIST')
                print('-----------------------------------------------')
                index = 1
                for baker_list_key in baker:
                    print(f'{index}. {baker_list_key}')
                    index += 1
                print(f'{len(baker) + 1}. cancel')

                try:
                    index_of_baker_to_edit = int(input(f'\nWhich baker do you want to edit? (or enter {len(baker) + 1} to cancel)\n>>> '))
                    if index_of_baker_to_edit == len(baker) + 1:
                        print('\nCancelling. Exiting to services page......')
                        break

                    elif 1 <= index_of_baker_to_edit <= len(baker):
                        selected_baker = list(baker.keys())[index_of_baker_to_edit - 1]  # identify the selected baker to update
                        while True:
                            print('\n-----------------------------------------------')
                            print(f'\t\t\t\t {selected_baker.upper()}\'S DATA')
                            print('-----------------------------------------------')

                            for baker_data_key, baker_data_value in (baker[selected_baker].items()):
                                print(f'{baker_data_key}: {baker_data_value}')  # print the details of baker and replace the underscore with a space

                            attribute_of_baker_data = input('\nWhich information do you want to update? (or enter \"cancel\")\n>>> ')
                            if attribute_of_baker_data in baker[selected_baker]:  # check if the attribute inputted found in baker's data

                                while True:
                                    if attribute_of_baker_data == 'baker_password':
                                        print('\n+------------------------------------------------------------------------+')
                                        print('|⚠️ This password is created by manager. You are not allow to change it. |')
                                        print('+------------------------------------------------------------------------+')
                                        break
                                    else:
                                        try:
                                            new_value = input(f'\nEnter new {attribute_of_baker_data}: ')

                                            if attribute_of_baker_data == 'baker_username':
                                                if new_value in (baker[baker_name]['baker_username'] for baker_name in baker):  # if new value same with the current username in file, duplication occurs
                                                    print('\n+----------------------------------------------------------+')
                                                    print('|⚠️ Username has been used. Please enter another username. |')
                                                    print('+----------------------------------------------------------+')
                                                    continue

                                            elif attribute_of_baker_data == 'age':
                                                if int(new_value) < 18 or int(new_value) > 60:  # check if the age is between 18 - 60
                                                    print('\n+--------------------------------------------------------------------+')
                                                    print('|⚠️ The required age is between 18 and 60. Please enter a valid age. |')
                                                    print('+--------------------------------------------------------------------+')
                                                    continue

                                            elif attribute_of_baker_data == 'gender':
                                                if new_value not in ['f', 'm']:
                                                    print('\n+--------------------------------------+')
                                                    print('|⚠️ Invalid input. Please enter again. |')
                                                    print('+--------------------------------------+')
                                                    continue
                                                elif new_value == 'f':
                                                    new_value = 'female'

                                                else:
                                                    new_value = 'male'

                                            elif attribute_of_baker_data == 'contact_no':
                                                if not re.fullmatch(r'^\d{3}-\d{7}$', new_value):  # check if the contact number match the specific pattern
                                                    print('\n+-----------------------------------------------+')
                                                    print('|⚠️ Invalid contact number. Please enter again. |')
                                                    print('+-----------------------------------------------+')
                                                    continue

                                            elif attribute_of_baker_data == 'email':
                                                if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', new_value):  # check if the email match the specific pattern
                                                    print('\n+--------------------------------------+')
                                                    print('|⚠️ Invalid email. Please enter again. |')
                                                    print('+--------------------------------------+')
                                                    continue

                                            baker[selected_baker][attribute_of_baker_data] = new_value  # update the value of attributes
                                            print(f'\n{attribute_of_baker_data} of {selected_baker} is updated.')  # inform user that the information is updated
                                            save_info(baker)
                                            break

                                        except ValueError:
                                            print('\n+-----------------------------+')
                                            print('|⚠️ Please enter a valid age. |')
                                            print('+-----------------------------+')

                            elif attribute_of_baker_data == 'cancel':
                                print('\nCancelling. Exiting to Baker List......')
                                break

                            else:
                                print('\n❗Data not found.')  # selected attribute not found

                    else:
                        print('\n❗Baker not found.')  # selected baker not found

                except ValueError:
                    print('\n+-----------------------------------------+')
                    print('|⚠️ Invalid input. Please enter a number. |')
                    print('+-----------------------------------------+')

        elif manage_baker == '4':  # return back to the previous page
            print('\nExiting to Role Management......')
            system_administration.system_administration()
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

