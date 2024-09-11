import json


def inventory_control_product():
    print('\n-----------------------------------------------')
    print('\t\t\t', '','PRODUCT MANAGEMENT')
    print('-----------------------------------------------')
    print('1. add products\n2. remove products\n3. update products\n4. exit⛔🔙\n')
    product_control = input('What action do you wish to perform? (1, 2, 3, 4)\n>>> ')
    if product_control == '1':
        print('\nHere are the products produced by bakers.')
        print('\n-----------------------------------------------')
        print('\t\t\t\tProduct list')
        print('-----------------------------------------------')

        with open('inventory_product.txt', 'r') as product:
            content = json.load(product)

            length = 0
            for key, value in content.items():
                if len(value["product_name"]) > length:
                    length = len(value["product_name"])

            for key, value in content.items():
                product_name = value["product_name"]
                product_code = value["product_code"]

                print(f'Product name: {product_name.ljust(length+4)} quantity: {len(product_code)}')

        chosen_product = input('\nWhich product do you want to increase stock?\n>>> ')
        for key, value in content.items():
            if chosen_product in value["product_name"]:
                try:
                    add_stock = int(input(f'\nHow many {chosen_product} do you want to add? '))
                    if add_stock != 0:
                        print('hi')
                        break
                except ValueError:
                    print('Please enter a number.')
                    break
        else:
            print('invalid input')



inventory_control_product()

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