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

print(bakery)

print('***************************************************')
print('\t\tWELCOME TO《MORNING GLORY BAKERY》')
print('***************************************************\n')

while True:
    print('Role: ')
    print('1. Manager👨‍💼👩‍💼')
    print('2. Customer👦👧')
    print('3. Cashier🖥️💰')
    print('4. Baker🧑‍🍳🍞')
    print('5. Exit the program⛔🔙')
    try:
        role = int(input('\nWho are you? (1, 2, 3, 4):\n>>> '))

        if role == 1:
            print('\n---------------------------------------------------\n'
                  '\t\t\t\tMANAGER is selected.\n'
                  '---------------------------------------------------')
            manager.manager()

        elif role == 2:
            print('\n---------------------------------------------------\n'
                  '\t\t\t\tCUSTOMER is selected.\n'
                  '---------------------------------------------------')
            break

        elif role == 3:
            print('\n---------------------------------------------------\n'
                  '\t\t\t\tCASHIER is selected.\n'
                  '---------------------------------------------------')
            break

        elif role == 4:
            print('\n---------------------------------------------------\n'
                  '\t\t\t\tBAKER is selected.\n'
                  '---------------------------------------------------')
            baker.baker_accounts()

        elif role == 5:
            print('\n--------------------YOU ARE EXIT--------------------')
            exit()

        else:
            print('\n+------------------+')
            print('|⚠️ Invalid input. |')
            print('+------------------+\n')

    except ValueError:
        print('\n+------------------+')
        print('|⚠️ Invalid input. |')
        print('+------------------+\n')


