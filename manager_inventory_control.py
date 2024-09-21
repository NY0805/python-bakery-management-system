import json

import manager_inventory_ingredient


def load_data_from_product():
    try:
        file = open('baker_product_keeping.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(
                    content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


def load_data_from_manager_product_inventory():
    try:
        file = open('manager_product_inventory.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(
                    content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


def save_info_product_inventory(product_inventory):
    file = open('manager_product_inventory.txt', 'w')  # open the file to write
    json.dump(product_inventory, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def save_info_product(product):
    file = open('baker_product_keeping.txt', 'w')  # open the file to write
    json.dump(product, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


product = load_data_from_product()
product_inventory = load_data_from_manager_product_inventory()


def inventory_control_product():
    while True:
        if len(product_inventory) == 0:
            print('\n❗The product inventory is empty. Please restock in time.')

        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'PRODUCT MANAGEMENT')
        print('-----------------------------------------------')
        print('1. Add products into inventory\n2. Remove products from inventory\n3. Update products in inventory\n4. Back to Main Inventory Management⛔🔙\n')
        product_control = input('\nWhat action do you wish to perform? (1, 2, 3, 4)\n>>> ')

        while True:

            if product_control == '1':
                print('\n-----------------------------------------------')
                print('\t', '', 'CURRENT PRODUCTS PRODUCED BY BAKERS')
                print('-----------------------------------------------')

                for key, value in product.items():
                    product_name = value['product_name']
                    quantity = len(value['serial_number'])

                    print(f'Product name: {product_name:<15} quantity: {quantity}')

                chosen_product = input('\nWhich product do you want to restock? (or enter "cancel" to cancel)\n>>> ')

                if chosen_product == 'cancel':
                    print('\nCancelling. Exiting to Product Management page......')
                    break

                elif chosen_product in (product[batch_number]['product_name'] for batch_number in product):
                    while True:
                        try:
                            add_stock = int(input(f'\nNumber of {chosen_product} to add: '))
                            if add_stock < 0:
                                print('\n+-------------------------------+')
                                print('|⚠️ Please enter a valid input. |')
                                print('+-------------------------------+')

                            elif add_stock == 0:
                                print('💡 No product is added.')
                                break

                            else:
                                for batch_number, value in product.items():
                                    if chosen_product == value['product_name']:
                                        serial_number = value['serial_number']

                                        if add_stock > len(serial_number):
                                            print('\n+---------------------------------------------------------------------------------------+')
                                            print(f'|⚠️ Not enough. The current number of {chosen_product}(s) is(are) {len(serial_number)}. |')
                                            print('+---------------------------------------------------------------------------------------+')
                                            add_stock = 0
                                            break

                                        if batch_number in product_inventory:
                                            stock = product_inventory[batch_number]['stock'] + add_stock
                                        else:
                                            stock = add_stock

                                        product_description = input('\nAdd product description for menu display:\n>>> ')

                                        product_inventory[batch_number] = {
                                            'product_name': chosen_product,
                                            'stock': stock,
                                            'description': product_description
                                        }

                                        quantity = len(serial_number) - stock
                                        if quantity <= 0:
                                            del product[batch_number]
                                        else:
                                            del serial_number[0: stock]

                                        save_info_product(product)
                                        save_info_product_inventory(product_inventory)

                                        print(f'\n{add_stock} {chosen_product}(s) is(are) added into the inventory.')
                                        print(f'Current stock of {chosen_product} in product inventory: {stock}')
                                        break
                                break

                        except ValueError:
                            print('\n+--------------------------+')
                            print('|⚠️ Please enter a number. |')
                            print('+--------------------------+')
                else:
                    print('\n❗Product not found, enter again.')

            elif product_control == '2':
                if len(product_inventory) == 0:
                    print('\n❗Out of stock!')
                    break

                else:
                    print('\n-----------------------------------------------')
                    print('\t\t\t', ' ', 'PRODUCT INVENTORY')
                    print('-----------------------------------------------')
                    for batch_number, value in product_inventory.items():
                        product_name = value['product_name']
                        available_quantity = value['stock']

                        print(f'{product_name:<15}: {available_quantity}')

                    product_stock = input('\nWhich products do you want to reduce? (or enter "cancel" to cancel)\n>>> ')

                    if product_stock == 'cancel':
                        print('\nCancelling. Exiting to Product Management page......')
                        break

                    elif product_stock in (product_inventory[batch_number]['product_name'] for batch_number in product_inventory):
                        while True:
                            try:
                                quantity_to_reduce = int(input(f'\nNumber of {product_stock} to reduce: '))
                                if quantity_to_reduce < 0:
                                    print('\n+-------------------------------+')
                                    print('|⚠️ Please enter a valid input. |')
                                    print('+-------------------------------+')

                                elif quantity_to_reduce == 0:
                                    print('\n💡 No product is reduced.')
                                    break

                                else:
                                    for batch_number, value in product_inventory.items():
                                        if product_stock == value['product_name']:
                                            available_stock = value['stock']

                                            if quantity_to_reduce > available_stock:
                                                print('\n+------------------------------------------------------------------------------------+')
                                                print(f'|⚠️ Out of range. The current stock of {product_stock}(s) is(are) {available_stock}. |')
                                                print('+------------------------------------------------------------------------------------+')
                                                break

                                            else:
                                                stock_left = available_stock - quantity_to_reduce
                                                print(f'\n{quantity_to_reduce} {product_stock}(s) is(are) reduced.')

                                            product_inventory[batch_number] = {
                                                'product_name': product_stock,
                                                'stock': stock_left
                                            }

                                            if stock_left <= 0:
                                                del product_inventory[batch_number]
                                                print('\n+-------------------------------------------------------------------------------+')
                                                print(f'|⚠️ Last {product_stock} has finished. Ask bakers to bake more {product_stock}. |')
                                                print('+-------------------------------------------------------------------------------+')

                                            save_info_product_inventory(product_inventory)
                                            break
                                    break

                            except ValueError:
                                print('\n+--------------------------+')
                                print('|⚠️ Please enter a number. |')
                                print('+--------------------------+')
                    else:
                        print('\n❗Product not found, enter again.')

            elif product_control == '3':
                if len(product_inventory) == 0:
                    print('\n❗Out of stock!')
                    break

                while True:
                    print('\n-----------------------------------------------')
                    print('\t\t\t\tPRODUCT LIST')
                    print('-----------------------------------------------')
                    for index, (key, value) in enumerate(product_inventory.items(), start=1):
                        print(f'{index}. {value["product_name"]}')
                    print(f'{len(product_inventory) + 1}. cancel')

                    try:
                        product_to_update = int(input('\nEnter the product\'s index number to update: '))
                        if product_to_update == len(product_inventory) + 1:
                            print('\nCancelling. Exiting to Product Management page......')
                            break

                        elif 1 <= product_to_update <= len(product_inventory):
                            selected_product = list(product_inventory.keys())[product_to_update - 1]
                            while True:
                                print('\n-----------------------------------------------')
                                print(f'\t\t\t\t {product_inventory[selected_product]["product_name"].upper()}')
                                print('-----------------------------------------------')

                                for product_inventory_key, product_inventory_value in (product_inventory[selected_product].items()):
                                    print(f'{product_inventory_key}: {product_inventory_value}')

                                attribute_of_product_inventory = input('\nWhich information do you want to update? (or enter \"cancel\")\n>>> ')
                                if attribute_of_product_inventory in product_inventory[selected_product]:

                                    while True:
                                        try:
                                            new_value = input(f'\nEnter new {attribute_of_product_inventory}: ')

                                            if attribute_of_product_inventory == 'product_name':
                                                if new_value in (product_inventory[batch_number]['product_name'] for batch_number in product_inventory):
                                                    print('\n+-----------------------------------------------------------------------+')
                                                    print('|⚠️ Duplicate product name detected. Please enter another product name. |')
                                                    print('+-----------------------------------------------------------------------+')
                                                    continue

                                            elif attribute_of_product_inventory == 'stock':
                                                with open('baker_product_keeping.txt', 'r') as product_keeping:
                                                    products = json.load(product_keeping)

                                                    serial_number = products[selected_product]['serial_number']
                                                    if int(new_value) > len(serial_number):
                                                        print('\n+-----------------------------------------------------------+')
                                                        print(f'|⚠️ The current stock of {products[selected_product]["product_name"]} is {len(serial_number)}. Please enter again. |')
                                                        print('+-----------------------------------------------------------+')
                                                        continue

                                            product_inventory[selected_product][attribute_of_product_inventory] = new_value
                                            print(f'\n{attribute_of_product_inventory} of {selected_product} is updated.')
                                            save_info_product_inventory(product_inventory)
                                            break

                                        except ValueError:
                                            print('\n+------------------------------+')
                                            print('|⚠️ Please enter numbers only. |')
                                            print('+------------------------------+')

                                elif attribute_of_product_inventory == 'cancel':
                                    print('\nCancelling. Exiting to Product List......')
                                    break

                                else:
                                    print('\n❗Data not found.')
                        else:
                            print('\n+------------------------------------------+')
                            print('|⚠️ Product not found. Please enter again. |')
                            print('+------------------------------------------+')

                    except ValueError:
                        print('\n+--------------------------+')
                        print('|⚠️ Please enter a number. |')
                        print('+--------------------------+')
                break

            elif product_control == '4':
                print('\nExiting to Main Inventory Management......')
                return False

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')
                break


def main_control():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t', ' ', 'MAIN INVENTORY MANAGEMENT')
        print('-----------------------------------------------')
        print('1. Ingredient Inventory\n2. Product Inventory\n3. Back to Manager Privilege⛔🔙')

        control = input('\nSelect the inventory that you want to manage(1, 2, 3, 4):\n>>> ')
        if control == '1':
            manager_inventory_ingredient.ingredient_management()

        elif control == '2':
            inventory_control_product()

        elif control == '3':
            print('\nExiting to Manager Privilege......')
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


#main_control()