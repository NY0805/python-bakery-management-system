import json


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


def inventory_control_product():
    while True:
        if len(product_inventory) == 0:
            print('\nThe product inventory is empty. Please restock in time.')

        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'PRODUCT MANAGEMENT')
        print('-----------------------------------------------')
        print('1. add products into inventory\n2. remove products from inventory\n3. update products in inventory\n4. exit⛔🔙\n')
        product_control = input('What action do you wish to perform? (1, 2, 3, 4)\n>>> ')

        while True:
            if product_control == '1':
                print('\nHere are the products produced by bakers.')
                print('\n-----------------------------------------------')
                print('\t\t\tCurrent product list')
                print('-----------------------------------------------')

                length = 0
                for key, value in product.items():
                    if len(value["product_name"]) > length:
                        length = len(value["product_name"])

                    product_name = value["product_name"]
                    serial_number = value["serial_number"]

                    print(f'Product name: {product_name.ljust(length + 4)} quantity: {len(serial_number)}')

                chosen_product = input('\nWhich product do you want to restock? (or enter "cancel" to cancel)\n>>> ')

                if chosen_product == 'cancel':
                    print('\nCancelling. Exiting to product management page......')
                    break

                elif chosen_product in (product[batch_number]['product_name'] for batch_number in product):
                    while True:
                        try:
                            add_stock = int(input(f'\nHow many {chosen_product} do you want to add? '))
                            if add_stock == 0:
                                print('invalid')

                            else:
                                for batch_number, value in product.items():
                                    if value['product_name'] == chosen_product:
                                        if len(value['serial_number']) == 0:
                                            serial_number = value['serial_number']

                                            if 0 < add_stock <= len(serial_number):
                                                product_inventory[batch_number] = {
                                                    'product_name': chosen_product,
                                                    'stock': add_stock
                                                }

                                            else:
                                                print(f'\nNot enough. The current number of {chosen_product}(s) is(are) {len(serial_number)}. ')
                                                still_add = input('Do you want to add? (y=yes. n=no)\n>>> ')
                                                while still_add not in ['y', 'n']:
                                                    print('\ninvalid, enter again.')
                                                    still_add = input('Do you want to add? (y=yes. n=no)\n>>> ')

                                                if still_add == 'y':
                                                    break

                                                    '''product_inventory[batch_number] = {
                                                        'product_name': chosen_product,
                                                        'stock': len(serial_number)
                                                    }
                                                    print(
                                                        f'\n{len(serial_number)} {chosen_product}(s) is(are) added to the inventory.')
                                                    number_of_product = len(serial_number)

                                                    del serial_number[0]
                                                    print(
                                                        f'\n{number_of_product} {chosen_product} from baker\'s record keeping has(have) been deleted.')
                                                    if len(serial_number) < 1:
                                                        del product[batch_number]'''
                                        else:
                                            product_inventory[batch_number] = {
                                                'product_name': chosen_product,
                                                'stock': value['stock'] + add_stock
                                            }
                                        print(f'\n{add_stock} {chosen_product}(s) is(are) added to the inventory.')

                                        del serial_number[0: add_stock]
                                        print(f'\n{add_stock} {chosen_product} from baker\'s record keeping has(have) been deleted.')
                                        if len(serial_number) < 1:
                                            del product[batch_number]

                                        save_info_product_inventory(product_inventory)
                                        save_info_product(product)
                                        break
                                break

                        except ValueError:
                            print('Please enter a number.')

                else:
                    print('\nenter again.')

            else:
                print('\ninvalid input')
                break


def main_control():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t', ' ', 'MAIN INVENTORY MANAGEMENT')
        print('-----------------------------------------------')
        print('1. ingredient inventory\n2. product inventory\n3. Exit⛔🔙')

        control = input('\nSelect the inventory that you want to manage(1, 2, 3, 4):\n>>> ')
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


main_control()
