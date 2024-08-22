import json
import system_administration


def load_data_from_customer():
    try:
        file = open('customer.txt', 'r')  # open the file and read
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
def save_info(customer):
    file = open('cashier.txt', 'w')  # open the file to write
    json.dump(customer, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()


def system_administration_customer():
    customer = load_data_from_customer()

    print('\n-----------------------------------------------')
    print('\t\t\t\t', '', 'SERVICES')
    print('-----------------------------------------------')
    print('1. add cashier(s)\n2. remove cashier(s)\n3. exit')
    manage_customer = input('Please choose a service:\n>>> ')
    if manage_customer == '1':
        while True:
            customer_username = input('\nUsername: ')
            if customer_username in customer:
                print('Account exists. Please enter another username.')

            else:
                customer_password = input('Password: ')
                customer[customer_username] = {
                    'cashier_username': customer_username,
                    'cashier_password': customer_password
                }
                print('information saved.\n')
                save_info(customer)

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

    elif manage_customer == '2':
        while True:
            print('\n-----------------------------------------------')
            print('\t\t\t\t', '', 'Customer list')
            print('-----------------------------------------------')
            for index, key in enumerate(customer, start=1):
                print(f'{index}. {key}')

            while True:
                try:
                    index_of_customer_to_remove = int(input('Which cashier do you want to remove? \n>>> '))
                    if 1 <= index_of_customer_to_remove <= len(customer):
                        key_to_remove = list(customer.keys())[index_of_customer_to_remove - 1]
                        del customer[key_to_remove]
                        save_info(customer)

                        print(f'{key_to_remove} removed.\n')
                        while True:
                            remove_more = input('Continue remove? (y=yes, n=no)\n>>> ')
                            if remove_more == 'y':
                                break
                            elif remove_more == 'n':
                                break
                            else:
                                print('\ninvalid input. Enter again.')
                                break
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

    elif manage_customer == '3':
        print('Exiting to role selection......')
        system_administration.system_administration()

    else:
        print('invalid input.')

