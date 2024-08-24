import json
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


def system_administration_cashier():
    cashier = load_data_from_cashier()

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'SERVICES')
        print('-----------------------------------------------')
        print('1. add cashier(s)\n2. remove cashier(s)\n3. exit')

        manage_cashier = input('Please choose a service:\n>>> ')

        if manage_cashier == '1':
            while True:
                cashier_username = input('\nUsername: ')
                if cashier_username in cashier:
                    print('Account exists. Please enter another username.')

                else:
                    cashier_password = input('Password: ')
                    cashier[cashier_username] = {
                        'cashier_username': cashier_username,
                        'cashier_password': cashier_password
                    }
                    print('information saved.\n')
                    save_info(cashier)

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
                if len(cashier) == 1:
                    print('To ensure the daily normal operation, you cannot remove the last cashier in the list. ')
                    break

                else:
                    print('\n-----------------------------------------------')
                    print('\t\t\t\t', '', 'Cashier list')
                    print('-----------------------------------------------')
                    for index, key in enumerate(cashier, start=1):
                        print(f'{index}. {key}')

                    while True:
                        try:
                            index_of_cashier_to_remove = int(input('Which cashier do you want to remove? \n>>> '))
                            if 1 <= index_of_cashier_to_remove <= len(cashier):
                                key_to_remove = list(cashier.keys())[index_of_cashier_to_remove - 1]
                                del cashier[key_to_remove]
                                save_info(cashier)

                                print(f'{key_to_remove} removed.\n')
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

        elif manage_cashier == '3':
            print('Exiting to role selection......')
            system_administration.system_administration()
            break

        else:
            print('invalid input.')


