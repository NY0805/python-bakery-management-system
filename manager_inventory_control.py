def inventory_control_product():
    print('\n-----------------------------------------------')
    print('\t\t\t\tPRODUCT MANAGEMENT')
    print('-----------------------------------------------')
    print('1. ingredients\n2. products\n3. Exit⛔🔙')


def inventory_control_ingredient():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'INGREDIENT MANAGEMENT')
        print('-----------------------------------------------')
        print('1. add ingredients\n2. remove ingredients\n3. update ingredients\n4. exit⛔🔙')

        ingredient_control = input('What action do you wish to perform? (1, 2, 3, 4)\n>>> ')
        if ingredient_control == '1':
            print('add')

        elif ingredient_control == '2':
            print('remove')

        elif ingredient_control == '3':
            print('update')

        elif ingredient_control == '4':
            print('\nExiting to the main inventory control page......')
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


def main_control():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t\tMAIN INVENTORY MANAGEMENT')
        print('-----------------------------------------------')
        print('1. ingredient management\n2. product management\n3. Exit⛔🔙')

        control = input('\nSelect the item that you want to manage(1, 2, 3, 4):\n>>> ')
        if control == '1':
            inventory_control_ingredient()

        elif control == '2':
            inventory_control_product()

        elif control == '3':
            print('\nExiting to manager privilege......')
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

#main_control()