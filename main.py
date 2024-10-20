# import relevant modules for function call later
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

# print the bakery illustration and bakery name
print(bakery)

print('***************************************************')
print('\t\tWELCOME TO 《MORNING GLORY BAKERY》')
print('***************************************************')

# provide the options for different roles
while True:
    print('\nRole Options: ')
    print('1. Manager👨‍💼👩‍💼')
    print('2. Baker🧑‍🍳🍞')
    print('3. Cashier🖥️💰')
    print('4. Customer👦👧')
    print('5. Exit the program⛔🔙')

    # identify the role and run each role's function
    try:
        role = int(input('\nWho are you? (1, 2, 3, 4):\n>>> '))

        if role == 1:
            manager.manager()

        elif role == 2:
            baker.baker_accounts()

        elif role == 3:
            cashier.cashier_accounts()

        elif role == 4:
            customer.customer()

        elif role == 5:
            print('\n--------------------YOU ARE EXIT--------------------')
            exit()

    # display error message if the input is invalid
        else:
            print('\n+------------------+')
            print('|⚠️ Invalid input. |')
            print('+------------------+')

    except ValueError:
        print('\n+------------------+')
        print('|⚠️ Invalid input. |')
        print('+------------------+')
