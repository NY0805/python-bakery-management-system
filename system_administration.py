import json

import system_administration_baker, system_administration_cashier, system_administration_customer


def system_administration():

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\tROLE OPTIONS')
        print('-----------------------------------------------')
        print('1. Baker🧑‍🍳🍞\n2. Cashier🖥️💰\n3. Customer👦👧\n4. Exit⛔🔙')

        role = input('\nWhich role do you want to manage(1, 2, 3, 4): ')

        if (role != '1') and (role != '2') and (role != '3') and (role != '4'):
            print('invalid input.')
            continue

        elif role == '1':
            system_administration_baker.system_administration_baker()

        elif role == '2':
            system_administration_cashier.system_administration_cashier()

        elif role == '3':
            system_administration_customer.system_administration_customer()

        elif role == '4':
            print('Exiting to manager privilege......')
            break
        break









