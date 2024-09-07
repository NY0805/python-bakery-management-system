import json
import re
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
    file = open('customer.txt', 'w')  # open the file to write
    json.dump(customer, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()


customer = load_data_from_customer()


def activate_customer():
    while True:
        inactive_acc = []
        for customer_name in customer:
            if customer[customer_name]['account_status'] == 'inactive':
                inactive_acc.append(customer_name)

        if len(inactive_acc) == 0:
            print('\nNo account to activate.')
            print('Back to service page......')
            break
        else:
            print('\n-----------------------------------------------')
            print('\t\t\t\tINACTIVE ACCOUNT')
            print('-----------------------------------------------')

        index = 1
        for name in inactive_acc:
            print(f'{index}. {name}')
            index = index + 1

        index_cancel = index
        print(f'{index_cancel}. cancel')

        try:
            activate = int(input('\nWhich account do you want to activate?\n>>> '))

            if activate == index_cancel:
                print('Exiting to service page......')
                break

            elif 1 <= activate <= len(inactive_acc):
                selected_activate_acc = inactive_acc[activate - 1]
                customer[selected_activate_acc]['account_status'] = 'active'
                save_info(customer)

                print(f'\n{selected_activate_acc}\'s account has been activated.')
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

        except (ValueError, IndexError):
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


def deactivate_customer():
    while True:
        active_acc = []
        for customer_name in customer:
            if customer[customer_name]['account_status'] == 'active':
                active_acc.append(customer_name)

        if len(active_acc) == 0:
            print('\nNo account to deactivate.')
            print('Back to service page......')
            break
        else:
            print('\n-----------------------------------------------')
            print('\t\t\t\tINACTIVE ACCOUNT')
            print('-----------------------------------------------')

        index = 1
        for name in active_acc:
            print(f'{index}. {name}')
            index = index + 1

        index_cancel = index
        print(f'{index_cancel}. cancel')

        try:
            deactivate = int(input('\nWhich account do you want to deactivate?\n>>> '))

            if deactivate == index_cancel:
                print('Exiting to service page......')
                break

            elif 1 <= deactivate <= len(active_acc):
                selected_deactivate_acc = active_acc[deactivate - 1]
                customer[selected_deactivate_acc]['account_status'] = 'inactive'
                save_info(customer)

                print(f'\n{selected_deactivate_acc}\'s account has been deactivated.')
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

        except (ValueError, IndexError):
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


def edit_customer():

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'Customer list')
        print('-----------------------------------------------')
        for customer_list_index, customer_list in enumerate(customer, start=1):
            print(f'{customer_list_index}. {customer_list}')
        print(f'{len(customer) + 1}. cancel')

        try:
            index_of_customer_to_edit = int(
                input(f'\nWhich customer do you want to edit? (or enter {len(customer) + 1} to cancel)\n>>> '))
            if index_of_customer_to_edit == len(customer) + 1:
                print('\nCancelling. Exiting to the service page......')
                break

            elif 1 <= index_of_customer_to_edit <= len(customer):

                selected_customer = list(customer.keys())[index_of_customer_to_edit - 1]
                while True:
                    print('\n-----------------------------------------------')
                    print(f'\t\t\t\t {selected_customer}\'s data')
                    print('-----------------------------------------------')

                    for customer_data_key, customer_data_value in (customer[selected_customer].items()):
                        if customer_data_key != 'account_status':
                            print(f'{customer_data_key}: {customer_data_value}')

                    attribute_of_customer_data = input(
                        '\nWhich information do you want to modify? (or enter \"cancel\")\n>>> ')
                    if attribute_of_customer_data in customer[selected_customer]:
                        if attribute_of_customer_data != 'account_status':

                            while True:
                                try:
                                    new_value = input(f'\nEnter new {attribute_of_customer_data}: ')

                                    if attribute_of_customer_data == 'customer_username':
                                        if new_value in (customer[customer_name]['customer_username'] for customer_name in customer):
                                            print('\n+----------------------------------------------------------+')
                                            print('|⚠️ Username has been used. Please enter another username. |')
                                            print('+----------------------------------------------------------+')
                                            continue

                                    elif attribute_of_customer_data == 'customer_password':
                                        if new_value != 'b@k3rm4st3r!':
                                            print('\n+-----------------------------------------+')
                                            print('|⚠️ Password incorrect. Please try again. |')
                                            print('+-----------------------------------------+')
                                            continue

                                    elif attribute_of_customer_data == 'age':
                                        if int(new_value) < 18 or int(new_value) > 60:
                                            print(
                                                '\n+--------------------------------------------------------------------+')
                                            print('|⚠️ The required age is between 18 and 60. Please enter a valid age. |')
                                            print('+--------------------------------------------------------------------+')
                                            continue

                                    elif attribute_of_customer_data == 'gender':
                                        if new_value not in ['f', 'm']:
                                            print('\n+--------------------------------------+')
                                            print('|⚠️ Invalid input. Please enter again. |')
                                            print('+--------------------------------------+')
                                            continue
                                        elif new_value == 'f':
                                            new_value = 'female'

                                        else:
                                            new_value = 'male'

                                    elif attribute_of_customer_data == 'contact_no':
                                        if not re.fullmatch(r'^\d{3}-\d{7}$', new_value):
                                            print('\n+-----------------------------------------------+')
                                            print('|⚠️ Invalid contact number. Please enter again. |')
                                            print('+-----------------------------------------------+')
                                            continue

                                    elif attribute_of_customer_data == 'email':  # define the format of email
                                        if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', new_value):
                                            print('\n+--------------------------------------+')
                                            print('|⚠️ Invalid email. Please enter again. |')
                                            print('+--------------------------------------+')
                                            continue

                                    customer[selected_customer][attribute_of_customer_data] = new_value
                                    print(f'\n{attribute_of_customer_data} of {selected_customer} is updated.')
                                    save_info(customer)
                                    break

                                except ValueError:
                                    print('\n+-----------------------------+')
                                    print('|⚠️ Please enter a valid age. |')
                                    print('+-----------------------------+')

                        else:
                            print('\nData not found.')

                    elif attribute_of_customer_data == 'cancel':
                        print('\nCancelling. Exiting to the customer list......')
                        break

                    else:
                        print('\nData not found.')

            else:
                print('\nCustomer not found.')

        except ValueError:
            print('\n+-----------------------------------------+')
            print('|⚠️ Invalid input. Please enter a number. |')
            print('+-----------------------------------------+')


def terminate_customer():

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'Customer list')
        print('-----------------------------------------------')
        for index, key in enumerate(customer, start=1):
            print(f'{index}. {key}')
        print(f'{len(customer) + 1}. cancel')

        try:
            index_of_customer_to_terminate = int(input(f'\nWhich customer do you want to terminate? (or enter {len(customer) + 1} to cancel)\n>>> '))
            if index_of_customer_to_terminate == len(customer) + 1:
                print('\nCancelling. Exiting to the service page......')
                break

            elif 1 <= index_of_customer_to_terminate <= len(customer):
                customer_to_terminate = list(customer.keys())[index_of_customer_to_terminate - 1]
                del customer[customer_to_terminate]
                save_info(customer)
                print(f'\n{customer_to_terminate} terminated.\n')

                while True:
                    terminate_more = input('Continue to terminate? (y=yes, n=no)\n>>> ')
                    if terminate_more not in ['y', 'n']:
                        print('\n+--------------------------------------+')
                        print('|⚠️ Invalid input. Please enter again. |')
                        print('+--------------------------------------+\n')

                    else:
                        if terminate_more == 'y':
                            break

                        else:
                            print('\nStop terminating. Exiting to the service page......')
                            break
                break

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+\n')

        except ValueError:
            print('\n+-----------------------------------------+')
            print('|⚠️ Invalid input. Please enter a number. |')
            print('+-----------------------------------------+\n')


def system_administration_customer():

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'SERVICES')
        print('-----------------------------------------------')
        print(
            '1. activate customer(s)\n2. deactivate customer(s)\n3. edit customer(s)\n4. terminate/remove customer account(s)\n5. exit')

        manage_customer = input('\nPlease choose a service:\n>>> ')

        if manage_customer == '1':
            activate_customer()

        elif manage_customer == '2':
            deactivate_customer()

        elif manage_customer == '3':
            edit_customer()

        elif manage_customer == '4':
            terminate_customer()

        elif manage_customer == '5':
            print('\nExiting to role management......')
            system_administration.system_administration()
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

