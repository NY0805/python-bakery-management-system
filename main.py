import manager, customer, cashier, baker

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
print('***************************************************')

while True:
    print('Role: ')
    print('1. Manager')
    print('2. Customer')
    print('3. Cashier')
    print('4. Baker')
    print('5. Exit the program')
    try:
        role = int(input('What is your role (1, 2, 3, 4): '))

        if role == 1:
            print('\nMANAGER is selected.\n---------------------------------------------------')
            manager.manager()

        elif role == 2:
            print('\nCUSTOMER is selected.\n---------------------------------------------------')
            break

        elif role == 3:
            print('\nCASHIER is selected.\n---------------------------------------------------')
            break

        elif role == 4:
            print('\nBAKER is selected.\n---------------------------------------------------')
            break

        elif role == 5:
            print('--------------------YOU ARE EXIT--------------------')
            exit()

        else:
            print('Invalid input.\n')

    except ValueError:
        print('invalid input.\n')



