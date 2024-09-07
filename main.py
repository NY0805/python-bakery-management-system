import json

import manager
import customer
import cashier
import baker

# illustrate a bakery store
bakery = '''
   __________________________________________________
  |                                                  |
  |               MORNING GLORY BAKERY               |
  |__________________________________________________|
      |       ____  ____  ____  ____  ____       |
      |      |    ||    ||    ||    ||    |      |
      |      |____||____||____||____||____|      |
      |                                          |
      |       __________        __________       |
      |      |          |      |          |      |
      |      |          |      |          |      |
      |      |          |      |          |      |
      |      |__________|      |__________|      |
      |__________________________________________|
      
'''


#  print(baker_file_content.keys())

print(bakery)

print('***************************************************')
print('\t\tWELCOME TO《MORNING GLORY BAKERY》')
print('***************************************************')

while True:
    print('\nRole: ')
    print('1. Manager👨‍💼👩‍💼')
    print('2. Baker🧑‍🍳🍞')
    print('3. Cashier🖥️💰')
    print('4. Customer👦👧')
    print('5. Exit the program⛔🔙')
    try:
        role = int(input('\nWho are you? (1, 2, 3, 4):\n>>> '))

        if role == 1:
            manager.manager()

        elif role == 2:
            baker.baker_accounts()

        elif role == 3:
            cashier.cashier_accounts()

        elif role == 4:
            print('\n---------------------------------------------------\n'
                  '\t\t\t\tCUSTOMER is selected.\n'
                  '---------------------------------------------------')
            customer.customer()

        elif role == 5:
            print('\n--------------------YOU ARE EXIT--------------------')
            exit()

        else:
            print('\n+------------------+')
            print('|⚠️ Invalid input. |')
            print('+------------------+')

    except ValueError:
        print('\n+------------------+')
        print('|⚠️ Invalid input. |')
        print('+------------------+')


