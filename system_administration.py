import json

import system_administration_baker


def system_administration():

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\tROLE OPTIONS')
        print('-----------------------------------------------')
        print('1. Baker\n2. Cashier\n3. Customer\n4. Exit')

        role = input('Which role do you want to manage(1, 2, 3, 4): ')
        while role == '1':
            system_administration_baker.system_administration_baker()


        else:
            print('invalid.')

