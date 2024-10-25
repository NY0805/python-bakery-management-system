import json
import re
import system_administration


# Define the function that loads customer data from the file
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


# Define the function that saves customer data to the file
def save_info(customer):
    file = open('customer.txt', 'w')  # open the file to write
    json.dump(customer, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()

def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


customer = load_data_from_customer()  # store the data that retrieved from file into customer


# define the function to activate customer
def activate_customer():
    while True:
        inactive_acc = []  # create a list to store the names of inactive customers
        for customer_name in customer:
            if customer[customer_name]['account_status'] == 'inactive':  # check if the account_status of customer is inactive
                inactive_acc.append(customer_name)  # append inactive customers into the list

        if len(inactive_acc) == 0:  # if the inactive_acc list is empty
            print('\n💡 No account to activate.')
            print('Back to Services page......')
            break
        else:
            print('')
            printed_centered('INACTIVE ACCOUNT')

        index = 1
        for name in inactive_acc:
            print(f'{index}. {name}')
            index = index + 1

        index_cancel = index
        print(f'{index_cancel}. cancel')

        try:
            activate = int(input('\nWhich account do you want to activate?\n>>> '))  # choose which customer to activate

            if activate == index_cancel:  # cancel the process
                print('\nExiting to Services page......')
                break

            elif 1 <= activate <= len(inactive_acc):
                selected_activate_acc = inactive_acc[activate - 1]  # determine the selected customer names from the list by indexing
                customer[selected_activate_acc]['account_status'] = 'active'  # update the status into active
                save_info(customer)

                print(f'\n{selected_activate_acc}\'s account has been activated.')  # inform user that the account status has been activated
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

        except (ValueError, IndexError):
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


# define the function to deactivate customers
def deactivate_customer():
    while True:
        active_acc = []  # create a list to store deactivate customer names
        for customer_name in customer:
            if customer[customer_name]['account_status'] == 'active':  # check if the account_status of customer is active
                active_acc.append(customer_name)  # append active customers into the list

        if len(active_acc) == 0:  # if the active_acc list is empty
            print('\n💡No account to deactivate.')
            print('Back to Services page......')
            break
        else:
            print('')
            printed_centered('ACTIVE ACCOUNT')

        index = 1
        for name in active_acc:
            print(f'{index}. {name}')
            index = index + 1

        index_cancel = index
        print(f'{index_cancel}. cancel')

        try:
            deactivate = int(input('\nWhich account do you want to deactivate?\n>>> '))  # choose which customer to deactivate

            if deactivate == index_cancel:
                print('\nExiting to Services page......')
                break

            elif 1 <= deactivate <= len(active_acc):
                selected_deactivate_acc = active_acc[deactivate - 1]  # determine the selected customer names from the list by indexing
                customer[selected_deactivate_acc]['account_status'] = 'inactive'  # update the status into inactive
                save_info(customer)

                print(f'\n{selected_deactivate_acc}\'s account has been deactivated.')  # inform user that the account status has been deactivated
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

        except (ValueError, IndexError):
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


# define the function to update customers' details
def update_customer():

    while True:
        print('')
        printed_centered('CUSTOMER LIST')
        index = 1
        for customer_list in customer:
            print(f'{index}. {customer_list}')
            index += 1
        print(f'{len(customer) + 1}. cancel')

        try:
            index_of_customer_to_edit = int(
                input(f'\nWhich customer do you want to edit? (or enter {len(customer) + 1} to cancel)\n>>> '))
            if index_of_customer_to_edit == len(customer) + 1:  # cancel the process
                print('\nCancelling. Exiting to Services page......')
                break

            elif 1 <= index_of_customer_to_edit <= len(customer):

                selected_customer = list(customer.keys())[index_of_customer_to_edit - 1]  # determine the selected customer names from the list by indexing
                while True:
                    print('')
                    printed_centered(f'{selected_customer.upper()}\'S DATA')

                    for customer_data_key, customer_data_value in (customer[selected_customer].items()):
                        # display all the details of customers except their account status
                        if customer_data_key != 'account_status' and customer_data_key != 'loyalty_points':
                            print(f'{customer_data_key}: {customer_data_value}')

                    attribute_of_customer_data = input('\nWhich information do you want to update? (or enter \"cancel\")\n>>> ')
                    if attribute_of_customer_data in customer[selected_customer]:
                        if attribute_of_customer_data != 'account_status' and attribute_of_customer_data != 'loyalty_points':

                            while True:
                                try:
                                    new_value = input(f'\nEnter new {attribute_of_customer_data}: ')

                                    if attribute_of_customer_data == 'customer_username':
                                        if new_value in (customer[customer_name]['customer_username'] for customer_name in customer):  # check if there is a duplication of username
                                            print('\n+----------------------------------------------------------+')
                                            print('|⚠️ Username has been used. Please enter another username. |')
                                            print('+----------------------------------------------------------+')
                                            continue

                                    elif attribute_of_customer_data == 'customer_password':
                                        if len(new_value) < 8 or len(new_value) > 12:  # check if the password is between 8 - 12 digits
                                            print('\n+---------------------------------------------------------------------------+')
                                            print('|⚠️ Invalid password length. Please make sure it is between 8 to 12 digits! |')
                                            print('+---------------------------------------------------------------------------+\n')
                                            continue

                                    elif attribute_of_customer_data == 'age':
                                        if int(new_value) < 18 or int(new_value) > 60:  # check if the age is between 18 - 60
                                            print('\n+--------------------------------------------------------------------+')
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
                                        if not re.fullmatch(r'^\d{3}-\d{7}$', new_value):  # check if the contact number match the specific pattern
                                            print('\n+-----------------------------------------------+')
                                            print('|⚠️ Invalid contact number. Please enter again. |')
                                            print('+-----------------------------------------------+')
                                            continue

                                    elif attribute_of_customer_data == 'email':  # define the format of email
                                        if not re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', new_value):  # check if the email match with the specific pattern
                                            print('\n+--------------------------------------+')
                                            print('|⚠️ Invalid email. Please enter again. |')
                                            print('+--------------------------------------+')
                                            continue

                                    customer[selected_customer][attribute_of_customer_data] = new_value  # update the value of attributes
                                    print(f'\n{attribute_of_customer_data} of {selected_customer} is updated.')  # inform user that the information is updated
                                    save_info(customer)
                                    break

                                except ValueError:
                                    print('\n+-----------------------------+')
                                    print('|⚠️ Please enter a valid age. |')
                                    print('+-----------------------------+')

                        else:
                            print('\n❗Data not found.')  # selected attribute not found

                    elif attribute_of_customer_data == 'cancel':
                        print('\nCancelling. Exiting to Customer List......')
                        break

                    else:
                        print('\n❗Data not found.')

            else:
                print('\n❗Customer not found.')  # selected customer not found

        except ValueError:
            print('\n+-----------------------------------------+')
            print('|⚠️ Invalid input. Please enter a number. |')
            print('+-----------------------------------------+')


# define the function to terminate customers
def terminate_customer():

    while True:
        print('')
        index = 1
        printed_centered('CUSTOMER LIST')
        for key in customer:
            print(f'{index}. {key}')
            index += 1
        print(f'{len(customer) + 1}. cancel')

        try:
            index_of_customer_to_terminate = int(input(f'\nWhich customer do you want to terminate? (or enter {len(customer) + 1} to cancel)\n>>> '))
            if index_of_customer_to_terminate == len(customer) + 1:
                print('\nCancelling. Exiting to Services page......')
                break

            elif 1 <= index_of_customer_to_terminate <= len(customer):
                customer_to_terminate = list(customer.keys())[index_of_customer_to_terminate - 1]  # identify the selected customer to update
                del customer[customer_to_terminate]  # delete the selected customer
                save_info(customer)
                print(f'\n{customer_to_terminate} terminated.\n')  # inform user about the customers has been terminated

                while True:
                    terminate_more = input('Continue to terminate? (y=yes, n=no)\n>>> ')
                    if terminate_more not in ['y', 'n']:
                        print('\n+--------------------------------------+')
                        print('|⚠️ Invalid input. Please enter again. |')
                        print('+--------------------------------------+\n')

                    else:
                        if terminate_more == 'y':  # exit the inner loop to access the outer loop and repeat the termination process
                            break

                        else:
                            print('\nStop terminating. Exiting to Services page......')
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


#define the function to manage customer
def system_administration_customer():

    while True:
        print('')
        printed_centered('SERVICES')
        print(
            '1. Activate Customer(s)\n2. Deactivate Customer(s)\n3. Update Customer(s)\n4. Terminate/Remove Customer Account(s)\n5. Back to Role Management')  # provide the option for customer management

        manage_customer = input('\nPlease choose a service:\n>>> ')

        if manage_customer == '1':  # activate customer
            activate_customer()

        elif manage_customer == '2':  # deactivate customer
            deactivate_customer()

        elif manage_customer == '3':  # update customer
            update_customer()

        elif manage_customer == '4':  # terminate/remove customer
            terminate_customer()

        elif manage_customer == '5':  # return to the previous page
            print('\nExiting to Role Management......')
            system_administration.system_administration()
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

#system_administration_customer()