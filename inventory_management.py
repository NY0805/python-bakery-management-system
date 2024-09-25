import baker_product_keeping, manager_inventory_ingredient


def inventory_services():
    print('\nEasily manage your bakery\'s inventory with our system!')
    print('With our system, you can effortlessly:\n'
          '\t- Add new ingredients and product\n'
          '\t- Update inventory details\n'
          '\t- Remove outdated or unused items\n'
          '\t- Check inventory levels')
    print('Stay on top of your supplies to ensure fresh and delicious baked goods every day!')
    print('\n-------------------------------------------------------')
    print('\t\t\t', '', 'INVENTORY MANAGEMENT MENU')
    print('-------------------------------------------------------\n')
    print('1. Ingredient Management')
    print('2. Product Management')
    print('3. Back to Homepage\n')

    while True:
        try:
            inventory_services_type = input('Please choose a service:\n'
                                            '>>> ')
            if inventory_services_type not in ['1', '2', '3']:
                print('Please enter a valid number.\n')
            else:
                if inventory_services_type == '1':
                    baker_inventory_ingredient.ingredient_management()
                elif inventory_services_type == '2':
                    baker_inventory_product.product_management()
                elif inventory_services_type == '3':
                    print('Exiting to baker privilege...')
                    break
        except ValueError:
            print('Please enter a valid number.\n')


inventory_services()
