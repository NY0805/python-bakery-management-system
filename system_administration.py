import json

import system_administration_baker, system_administration_cashier, system_administration_customer


def system_administration():

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\tROLE OPTIONS')
        print('-----------------------------------------------')
        print('1. Baker\n2. Cashier\n3. Customer\n4. Exit')

        role = input('Which role do you want to manage(1, 2, 3, 4): ')
        if role not in [1, 2, 3, 4]:
            print('invalid input.')

        while role == '1':
            system_administration_baker.system_administration_baker()

        while role == '2':
            system_administration_cashier.system_administration_cashier()

        while role == '3':
            system_administration_customer.system_administration_customer()

        while role == '4':
            print('still in progress ...')
            break





