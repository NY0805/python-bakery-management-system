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
    file = open('customer.txt', 'w')  # open the file to write
    json.dump(customer, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()

'''
def system_administration_customer():
    customer = load_data_from_customer()

    print('\n-----------------------------------------------')
    print('\t\t\t\t', '', 'SERVICES')
    print('-----------------------------------------------')
    print('1. account(s) recovery\n2. activate account(s)\n3. deactivate account(s)\n4. terminate and remove\n5. exit')
    manage_customer = input('Please choose a service (1, 2, 3, 4, 5):\n>>> ')
    if manage_customer == '1':
        print('hi')
'''

def activate_account():
    customer = load_data_from_customer()

    print('\n-----------------------------------------------')
    print('\t\t\t\tINACTIVE ACCOUNT')
    print('-----------------------------------------------')

    for index, (name, details) in enumerate(customer.items()):
        if details['account_status'] == 'inactive':
            print(f'{index}. {name}')

    activate = int(input('\nWhich account do you want to activate?\n>>> '))
    acc_to_activate = list(name)[activate - 1]
    print(f'Account {acc_to_activate} is activated.')



#activate_account()