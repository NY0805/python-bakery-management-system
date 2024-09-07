import json


def order_management():

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\tORDER MANAGEMENT')
        print('-----------------------------------------------')
        print('1. View order details\n2. Update order status\n3. Exit⛔🔙')

        order_management_choice = input('\nWhich action do you want to perform regarding orders? (1, 2, 3):\n>>> ')

        if order_management_choice == '1':
            print('in progress 1')

        elif order_management_choice == '2':
            print('\n-----------------------------------------------')
            print('\t\t\t\tUPDATE ORDER STATUS')
            print('-----------------------------------------------')
            print('1. View order details\n2. Update order status\n3. Exit⛔🔙')

        elif order_management_choice == '3':
            print('in progress 3')

        else:
            break
        break
