import json  # import json text file to record data
import re
from datetime import datetime


# Define the function that loads data from the file
def load_data_from_inventory_product():
    try:
        file = open('inventory_product.txt', 'r')  # open the file and read
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


# Define the function that saves information to the file
def save_info(product_data):
    file = open('inventory_product.txt', 'w')  # open the file to write
    json.dump(product_data, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


product_data = {}


def product_management():
    print('\n-------------------------------------------------------')
    print('\t\t\t\t', '', 'PRODUCT MANAGEMENT')
    print('-------------------------------------------------------')
    print('\n1. Add Product')
    print('2. Update Product')
    print('3. Remove Product')
    print('4. Back to Previous Page')

    while True:
        option_product_management = input('\nPlease choose a service:'
                                          '\n>>> ')
        if option_product_management not in ['1', '2', '3', '4']:
            print('Please enter a valid number.')
        else:
            if option_product_management == '1':
                product_details()
                break
            elif option_product_management == '2':
                pass
            elif option_product_management == '3':
                pass
            elif option_product_management == '4':
                print('Exiting to previous page...')
                break


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
        option_product_categories = input('\nPlease input the category:'
                                          '\n>>> ')
        if option_product_categories not in ['1', '2', '3', '4', '5', '6', '7']:
            print('Please enter a valid number.')
            continue
        else:
            if option_product_categories == '7':
                print('Going back to the previous page.')
                product_management()
                break
            elif option_product_categories == '6':
                while True:
                    category = input(f'\nCategory: ')
                    if validation_empty_entries(category):
                        if not validation_alphabet_only(category):
                            print('Please enter a valid category name. (Cannot contain any special characters.)\n.')
                        else:
                            return category
                    break
                break
            elif option_product_categories == '1':
                category = 'Breads'
                break
            elif option_product_categories == '2':
                category = 'Cakes'
                break
            elif option_product_categories == '3':
                category = 'Pastries'
                break
            elif option_product_categories == '4':
                category = 'Biscuits'
                break
            elif option_product_categories == '5':
                category = 'Muffins'
                break

    return category


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('Please enter something...\n')
        return False


def validation_alphanum_only(info):
    if info.isalnum():
        return True
    else:
        return False


def validation_alphanum_space_only(info):
    if re.fullmatch(r'[A-Za-z0-9 ]+', info):
        return True
    else:
        return False


def validation_alphabet_only(info):
    if re.search(r'[A-Za-z ]+', info):
        return True
    else:
        return False


def validation_list_alphabet_only(info):
    for item in info:
        if not item.isalpha():
            return False
        else:
            return True


def validation_digit_only(info):
    if info.isdigit():
        return True
    else:
        return False


def validation_date(info, date_format='%d-%m-%Y'):
    try:
        datetime.strptime(info, date_format)
        return True
    except ValueError:
        return False


def product_details():

    category = product_categories()

    product_data = load_data_from_inventory_product()

    product_info = ['Product Name', 'Product Code', 'Batch Number', 'Date of Production', 'Shelf Life',
                    'Expiry Date', 'Recipe', 'Quantity Produced', 'Baker\'s Name', 'Allergens']

    max_length = 0
    for item in product_info:
        if len(item) > max_length:
            max_length = len(item)

    print('\nPlease fill out the following fields to add a new product to the inventory:\n')

    while True:
        quantity_produced = input(f'1. {product_info[7].ljust(max_length + 2)}: ')
        if validation_empty_entries(quantity_produced):
            if not validation_digit_only(quantity_produced):
                print('Please enter a valid quantity produced. (Cannot contain any special characters.)\n.')
            else:
                quantity = int(quantity_produced)
                break

    while True:
        product_name = input(f'1. {product_info[0].ljust(max_length + 2)}: ')
        if validation_empty_entries(product_name):
            if not validation_alphabet_only(product_name):
                print('Please enter a valid product name. (Cannot contain any digits and special characters.)\n.')
            else:
                break

    while True:
        batch_number = input(f'3. {product_info[2].ljust(max_length + 2)}: ')
        if validation_empty_entries(batch_number):
            if not validation_alphanum_only(batch_number):
                print('Please enter a valid batch number. (Cannot contain any special characters.)\n.')
            else:
                break

    while True:
        date_of_production = input(f'4. {product_info[3].ljust(max_length + 2)}: ')
        if validation_empty_entries(date_of_production):
            if not validation_date(date_of_production):
                print("Please enter a date of production. (With format of 'day-month-year', 'xx-xx-xxxx'.)\n")
            else:
                break

    while True:
        shelf_life = input(f'5. {product_info[4].ljust(max_length + 2)}: ')
        if validation_empty_entries(shelf_life):
            if not validation_alphanum_space_only(shelf_life):
                print('Please enter a valid shelf life. (Cannot contain any special characters.)\n.')
            else:
                break

    while True:
        expiry_date = input(f'6. {product_info[5].ljust(max_length + 2)}: ')
        if validation_empty_entries(expiry_date):
            if not validation_date(expiry_date):
                print("Please enter a expiry date. (With format of 'day-month-year', 'xx-xx-xxxx'.)\n")
            else:
                break

    while True:
        recipe = input(f'7. {product_info[6].ljust(max_length + 2)}: ')
        if validation_empty_entries(recipe):
            if not validation_alphabet_only(recipe):
                print('Please enter a valid recipe. (Cannot contain any digits and special characters.)\n.')
            else:
                break

    while True:
        baker_name = input(f'9. {product_info[8].ljust(max_length + 2)}: ')
        if validation_empty_entries(baker_name):
            if not validation_alphanum_only(baker_name):
                print('Please enter a valid baker name. (Cannot contain any special characters.)\n.')
            else:
                break

    while True:
        allergens = input(f'10. {product_info[9].ljust(max_length + 2)}: ').split()
        if validation_empty_entries(allergens):
            if not validation_list_alphabet_only(allergens):
                print('Please enter a valid product name. (Cannot contain any digits and special characters.)\n.')
            else:
                break

    product_codes = []

    for i in range(quantity):
        while True:
            product_code = input(f'2. Enter product code for item {i + 1}: ')
            if validation_empty_entries(product_code):
                if not validation_alphanum_only(product_code):
                    print('Please enter a valid product code. (Cannot contain any special characters.)\n.')
                else:
                    product_codes.append(product_code)
                break

    product_data[batch_number] = {
        'category': category,
        'product_name': product_name,
        'product_code': product_codes,
        'quantity_produced': quantity_produced,
        'batch_number': batch_number,
        'date_of_production': date_of_production,
        'shelf_life': shelf_life,
        'expiry_date': expiry_date,
        'recipe': recipe,
        'baker_name': baker_name,
        'allergens': allergens
    }

    save_info(product_data)

    continue_adding()


def continue_adding():
    while True:
        try:
            add_more = input('\nInformation saved. Continue adding? (y=yes, n=no)'
                             '\n>>> ')
            if add_more == 'y':
                product_details()
                break
            elif add_more == 'n':
                print('Stop adding... Existing to Product Management page.')
                product_management()
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        except ValueError:
            print('Invalid input. Please enter again.')


def update_product():
    product = load_data_from_inventory_product()

    print('\n------------------------------------------------')
    print('\t\t\t\t', 'PRODUCT LIST')
    print('------------------------------------------------')
    for index, key in enumerate(product, start=1):
        print(f'{index}. {key}')
