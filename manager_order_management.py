import json


def load_data_from_customer_order_list():
    try:
        file = open('customer_order_list.txt', 'r')  # open the file and read
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


order_list = load_data_from_customer_order_list()


def order_management():
    print('\n-----------------------------------------------')
    print('\t\t\t\tORDER DETAILS')
    print('-----------------------------------------------')
    for key, value in order_list.items():
        print(f'{key}: {value}')


order_management()

'''while True:
    print('\n-----------------------------------------------')
    print('\t\t\t\tORDER MANAGEMENT')
    print('-----------------------------------------------')
    print('1. View order details\n2. Update order status\n3. Exit⛔🔙')

    order_management_choice = input('\nWhich action do you want to perform regarding orders? (1, 2, 3):\n>>> ')

    if order_management_choice == '1':
        print('in progress 1')

    elif order_management_choice == '2':
        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'UPDATE ORDER STATUS')
        print('-----------------------------------------------')


    elif order_management_choice == '3':
        print('in progress 3')

    else:
        break
    break'''


