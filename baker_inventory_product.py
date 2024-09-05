import json  # import json text file to record data


# Define the function that loads data from the file
def load_data_from_inventory_product():
    try:
        file = open('inventory_product.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


# Define the function that saves information to the file
def save_info(product_info):

    file = open('inventory_product.txt', 'w')  # open the file to write
    json.dump(product_info, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def product_management():
    print('\n-------------------------------------------------------')
    print('\t\t\t\t', '', 'PRODUCT MANAGEMENT')
    print('-------------------------------------------------------')
    print('\n1. Add Product')
    print('2. Update Product')
    print('3. Remove Product')
    print('4. Back to Previous Page')

    while True:
        try:
            option_product_management = input('\nPlease choose a service:'
                                              '\n>>> ')
            if option_product_management not in ['1', '2', '3', '4']:
                print('Please enter a valid number.')
            else:
                if option_product_management == '1':
                    product_categories()
                elif option_product_management == '2':
                    pass
                elif option_product_management == '3':
                    pass
                elif option_product_management == '4':
                    print('Exiting to previous page...')
                    break
        except ValueError:
            print('Please enter a valid number.')


def product_categories():
    print('\nHere are the main types of bakery products:')
    print('\n1. Breads')
    print('2. Cakes')
    print('3. Pastries')
    print('4. Biscuits')
    print('5. Muffins')
    print('6. Others')
    print('7. Back to Previous Page')
    while True:
        try:
            option_product_categories = input('\nPlease input the category:'
                                              '\n>>> ')
            if option_product_categories not in ['1', '2', '3', '4', '5', '6', '7']:
                print('Please enter a valid number.')
            else:
                product_details()
                while True:
                    try:
                        add_more = input('\nInformation saved. Continue adding? (y=yes, n=no)'
                                         '\n>>> ')
                        if add_more == 'y':
                            product_categories()
                            break
                        elif add_more == 'n':
                            print('Stop adding... Existing to Product Management page.')
                            product_management()
                            break
                        else:
                            print("Invalid input. Please enter 'y' or 'n'.")
                    except ValueError:
                        print('Invalid input. Please enter again.')
        except ValueError:
            print('Please enter a valid number.')


def product_details():

    product_data = {}

    product_info = ['Product Name', 'Product Code', 'Batch Number', 'Date of Production', 'Shelf Life',
                    'Expiry Date', 'Recipe', 'Quantity Produced', 'Baker\'s Name', 'Allergens']

    max_length = 0
    for item in product_info:
        if len(item) > max_length:
            max_length = len(item)

    print('\nPlease fill out the following fields to add a new product to the inventory:\n')

    product_name = input(f'1. {product_info[0].ljust(max_length + 2)}: ')
    product_code = input(f'2. {product_info[1].ljust(max_length + 2)}: ')
    batch_number = input(f'3. {product_info[2].ljust(max_length + 2)}: ')
    date_of_production = input(f'4. {product_info[3].ljust(max_length + 2)}: ')
    shelf_life = input(f'5. {product_info[4].ljust(max_length + 2)}: ')
    expiry_date = input(f'6. {product_info[5].ljust(max_length + 2)}: ')
    recipe = input(f'7. {product_info[6].ljust(max_length + 2)}: ')
    quantity_produced = input(f'8. {product_info[7].ljust(max_length + 2)}: ')
    baker_name = input(f'9. {product_info[8].ljust(max_length + 2)}: ')
    allergens = input(f'10. {product_info[9].ljust(max_length + 2)}: ')

    product_data[product_code] = {
        'product_name': product_name,
        'product_code': product_code,
        'batch_number': batch_number,
        'date_of_production': date_of_production,
        'shelf_life': shelf_life,
        'expiry_date': expiry_date,
        'recipe': recipe,
        'quantity_produced': quantity_produced,
        'baker_name': baker_name,
        'allergens': allergens
    }
    save_info(product_data)


'''    for index, item in enumerate(product_info, start=1):
        user_input = input(f'{index}. {item.ljust(max_length + 2)}: ')
        product_data[item] = user_input

    unique_key = product_data['Product Code'] if product_data['Product Code'] else str(uuid.uuid4())

    product_info[unique_key] = product_data

    save_info(product_info)'''


def continue_adding():
    pass
