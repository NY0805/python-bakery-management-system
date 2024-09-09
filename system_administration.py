import json

import system_administration_baker, system_administration_cashier, system_administration_customer


def system_administration():

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\tROLE MANAGEMENT')
        print('-----------------------------------------------')
        print('1. Baker🧑‍🍳🍞\n2. Cashier🖥️💰\n3. Customer👦👧\n4. Exit⛔🔙')

        role = input('\nWhich role do you want to manage(1, 2, 3, 4):\n>>> ')

        if role not in ['1', '2', '3', '4']:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

        elif role == '1':
            system_administration_baker.system_administration_baker()

        elif role == '2':
            system_administration_cashier.system_administration_cashier()

        elif role == '3':
            system_administration_customer.system_administration_customer()

        elif role == '4':
            print('\nExiting to manager privilege......')
            break
        break











