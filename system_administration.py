import json

import system_administration_baker
import system_administration_cashier
import system_administration_customer


# define a function to manage roles
def system_administration():

    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\tROLE MANAGEMENT')
        print('-----------------------------------------------')
        print('1. Baker🧑‍🍳🍞\n2. Cashier🖥️💰\n3. Customer👦👧\n4. Back to Manager Privilege⛔🔙')  # provide role selection

        role = input('\nWhich role do you want to manage(1, 2, 3, 4):\n>>> ')  # identify which role to manage

        if role not in ['1', '2', '3', '4']:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

        elif role == '1':  # manage baker
            system_administration_baker.system_administration_baker()

        elif role == '2':  # manage cashier
            system_administration_cashier.system_administration_cashier()

        elif role == '3':  # manage customer
            system_administration_customer.system_administration_customer()

        elif role == '4':  # return to the previous page
            print('\nExiting to Manager Privilege......')
            break
        return False











