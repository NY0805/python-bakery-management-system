import json  # import json text file to record data
import re
from datetime import datetime, timedelta


# Define the function that loads data from the file
def load_data_from_inventory_product():
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


# Define the function that saves information to the file
def save_info(product_data):
    file = open('baker_product_keeping.txt', 'w')  # open the file to write
    json.dump(product_data, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('\n❗Please enter something...\n')
        return False


def validation_alphanum_only(info):
    if info.isalnum():
        return True
    else:
        return False


def validation_alphabet_only(info):
    if re.fullmatch(r'[A-Za-z ]+', info):
        return True
    else:
        return False


def validation_list_alphabet_only(info):
    for item in info:
        if re.search(r'[A-Za-z ]+', item):
            return True
        else:
            return False


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
                update_product()
                break
            elif option_product_management == '3':
                pass
            elif option_product_management == '4':
                print('\nExiting to the previous page......')
                break


def product_categories():
    print('\n-----------------------------------------------')
    print('\t\tMAIN TYPES OF BAKERY PRODUCTS')
    print('-----------------------------------------------')
    print('1. Breads')
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
            print('\n+--------------------------------+')
            print('|⚠️ Please enter a valid number. |')
            print('+--------------------------------+')
            continue
        else:
            if option_product_categories == '7':
                print('\nGoing back to the Product Management page......')
                product_management()
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
            elif option_product_categories == '6':
                category = 'Others'
                break
    return category


def product_details():
    category = product_categories()

    product_data = load_data_from_inventory_product()

    product_info = ['Product Name', 'Product Code', 'Batch Number', 'Date of Production', 'Shelf Life (__ days)',
                    'Expiry Date (DD-MM-YYYY)', 'Recipe', 'Quantity Produced', 'Baker\'s Name', 'Allergens']

    max_length = 0
    for item in product_info:
        if len(item) > max_length:
            max_length = len(item)

    print('\n+------------------------------------------------------------------------+')
    print('|💡 Fill out the following fields to add a new product to the inventory. |')
    print('+------------------------------------------------------------------------+')

    while True:
        quantity_produced = input(f'1. {product_info[7].ljust(max_length + 2)}: ')
        if validation_empty_entries(quantity_produced):
            if validation_digit_only(quantity_produced):
                quantity = int(quantity_produced)
                break
            else:
                print('\n+--------------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid quantity produced. (Cannot contain any alphabets and special characters.) |')
                print('+--------------------------------------------------------------------------------------------------+\n')

    while True:
        product_name = input(f'2. {product_info[0].ljust(max_length + 2)}: ')
        if validation_empty_entries(product_name):
            if validation_alphabet_only(product_name):
                break
            else:
                print('\n+------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid product name. (Cannot contain any digits and special characters.) |')
                print('+------------------------------------------------------------------------------------------+\n')

    while True:
        product_code = input(f'3. {product_info[1].ljust(max_length + 2)}: ')
        if validation_empty_entries(product_code):
            if validation_alphanum_only(product_code):
                if product_code in product_data:
                    print('\n+---------------------------------------------------------------------------+')
                    print('|⚠️ Duplicate product code detected. Please input the correct product code. |')
                    print('+---------------------------------------------------------------------------+\n')
                else:
                    break
            else:
                print('\n+--------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid product code. (Cannot contain any special characters and spacings.) |')
                print('+--------------------------------------------------------------------------------------------+\n')

    while True:
        batch_number = input(f'3. {product_info[2].ljust(max_length + 2)}: ')
        if validation_empty_entries(batch_number):
            if validation_alphanum_only(batch_number):
                if batch_number in product_data:
                    print('\n+---------------------------------------------------------------------------+')
                    print('|⚠️ Duplicate batch number detected. Please input the correct batch number. |')
                    print('+---------------------------------------------------------------------------+\n')
                else:
                    break
            else:
                print('\n+-------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid batch number. (Cannot contain any special characters.) |')
                print('+-------------------------------------------------------------------------------+\n')

    while True:
        date_of_production = input(f'4. {product_info[3].ljust(max_length + 2)}: ')
        if validation_empty_entries(date_of_production):
            if validation_date(date_of_production):
                break
            else:
                print('\n+---------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid date of production. (With format of "day-month-year", "xx-xx-xxxx".) |')
                print('+---------------------------------------------------------------------------------------+\n')

    while True:
        shelf_life = input(f'5. {product_info[4].ljust(max_length + 2)}: ')
        if validation_empty_entries(shelf_life):
            match = re.match(r'^(\d+)\s*days$', shelf_life.strip())
            if match:
                number = int(match.group(1))
                if category in ['Breads', 'Muffins']:
                    if number <= 5:
                        break
                    else:
                        print('\n+------------------------------------------------------------------+')
                        print('|⚠️ Please enter a valid shelf life. (Cannot be more than 5 days.) |')
                        print('+------------------------------------------------------------------+\n')
                elif category in ['Cakes', 'Pastries']:
                    if number <= 7:
                        break
                    else:
                        print('\n+------------------------------------------------------------------+')
                        print('|⚠️ Please enter a valid shelf life. (Cannot be more than 7 days.) |')
                        print('+------------------------------------------------------------------+\n')
                elif category in ['Biscuits', 'Others']:
                    if number <= 14:
                        break
                    else:
                        print('\n+------------------------------------------------------------------+')
                        print('|⚠️ Please enter a valid shelf life. (Cannot be more than 14 days.) |')
                        print('+------------------------------------------------------------------+\n')
            else:
                print("\n")
                print('\n+---------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a number followed by "days". (Case sensitive & no special characters.) |')
                print('+---------------------------------------------------------------------------------------+\n')

    while True:
        expiry_date_str = input(f'6. {product_info[5].ljust(max_length + 2)}: ')
        if validation_empty_entries(expiry_date_str):
            if validation_date(expiry_date_str):
                # convert expiry_date_str from string to datetime format
                expiry_date = datetime.strptime(expiry_date_str, '%d-%m-%Y')
                # convert date_of _production from string to datetime format
                date_of_production_new = datetime.strptime(date_of_production, '%d-%m-%Y')

                max_expiry = date_of_production_new + timedelta(days=number + 1)

                if max_expiry >= expiry_date >= date_of_production_new:
                    break
                else:
                    print('\n+---------------------------------------------------------------------------------------------------------+')
                    print('|⚠️ The expired date does not fall within the allowable period.                                           |')
                    print('|   The allowable period must between the date of production and date of production + shelf life + 1 day. |')
                    print('|                                                                                                         |')
                    print(f'| * Allowable period: {date_of_production} to {max_expiry.strftime("%d-%m-%Y")}.                          |')
                    print('+---------------------------------------------------------------------------------------------------------+\n')
            else:
                print('\n+--------------------------------------------------------------------+')
                print('|⚠️ Invalid date format. Please enter the date in DD-MM-YYYY format. |')
                print('+--------------------------------------------------------------------+\n')

    while True:
        recipe = input(f'7. {product_info[6].ljust(max_length + 2)}: ')
        if validation_empty_entries(recipe):
            if validation_alphabet_only(recipe):
                break
            else:
                print('\n+------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid recipe. (Cannot contain any digits and special characters.) |')
                print('+------------------------------------------------------------------------------------+\n')

    while True:
        baker_name = input(f'8. {product_info[8].ljust(max_length + 2)}: ')
        if validation_empty_entries(baker_name):
            if validation_alphabet_only(baker_name):
                break
            else:
                print('\n+-----------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid baker name. (Cannot contain any special characters.) |')
                print('+-----------------------------------------------------------------------------+\n')

    while True:
        print('\n+---------------------------------------------------------------------------------------------------------+')
        print('|💡 If there is more than one data item, separate them with a space.                                      |')
        print('|💡 If a name consists of more than one words, use underscore (_) to represent the space, e.g. tree_nuts. |')
        print('+---------------------------------------------------------------------------------------------------------+\n')
        allergens = input(f'9. {product_info[9].ljust(max_length + 2)}: ').split()
        if validation_empty_entries(allergens):
            if validation_list_alphabet_only(allergens):
                break
            else:
                print('\n+--------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid allergen. (Cannot contain any digits and special characters.) |')
                print('+--------------------------------------------------------------------------------------+\n')

    serial_numbers = []

    for i in range(quantity):
        while True:
            serial_number = input(f'Enter serial number for item {i + 1}: ')
            if validation_empty_entries(serial_number):
                if not validation_alphanum_only(serial_number):
                    print('\n+---------------------------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid serial number. (Cannot contain any special characters and spacings.) |')
                    print('+---------------------------------------------------------------------------------------------+\n')
                else:
                    serial_numbers.append(serial_number)
                break

    product_data[batch_number] = {
        'category': category,
        'product_name': product_name,
        'product_code': product_code,
        'serial_number': serial_numbers,
        'quantity_produced': quantity_produced,
        'batch_number': batch_number,
        'date_of_production': date_of_production,
        'shelf_life': shelf_life,
        'expiry_date': expiry_date_str,
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
                print('\nStop adding. Exiting to Product Management page......')
                product_management()
                break
            else:
                print('\n+-------------------------------------------+')
                print('|⚠️ Invalid input. Please enter "y" or "n". |')
                print('+-------------------------------------------+')
        except ValueError:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


def update_product():
    product_data = load_data_from_inventory_product()

    while True:
        print('\n------------------------------------------------')
        print('\t\t\t\t', 'PRODUCT LIST')
        print('------------------------------------------------')
        for index, key in enumerate(product_data, start=1):
            print(f'{index}. {key}')
        print(f'{len(product_data) + 1}. cancel')

        try:
            index_of_product_to_edit = int(
                input(f'\nWhich product do you want to update? (or enter {len(product_data) + 1} to cancel)\n>>> '))
            if index_of_product_to_edit == len(product_data) + 1:
                print('\nCancelling. Exiting to Product Management page......')
                product_management()
                break

            elif 1 <= index_of_product_to_edit <= len(product_data):
                selected_product = list(product_data.keys())[index_of_product_to_edit - 1]
                while True:
                    print('\n-----------------------------------------------')
                    print(f'\t\t\t\t {selected_product.upper()}\'S DATA')
                    print('-----------------------------------------------')

                    for product_data_key, product_data_value in (product_data[selected_product].items()):
                        print(f'{product_data_key}: {product_data_value}')

                    attribute_of_product_data = input('\nWhich information do you want to update? (or enter \"cancel\")\n>>> ')
                    if attribute_of_product_data in product_data[selected_product]:
                        while True:
                            new_value = input(f'\nEnter new {attribute_of_product_data}: ')
                            if attribute_of_product_data == 'category':
                                if not validation_empty_entries(new_value):
                                    continue
                                if new_value not in ['Breads', 'Cakes', 'Pastries', 'Biscuits', 'Muffins', 'Others']:
                                    print('\n+-------------------------------------------------------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter Breads, Cakes, Pastries, Biscuits, Muffins or Others. |')
                                    print('+-------------------------------------------------------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'product_name':
                                if not validation_empty_entries(new_value):
                                    continue
                                if not validation_alphabet_only(new_value):
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter again. |')
                                    print('+--------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'serial_number':
                                if not validation_empty_entries(new_value):
                                    continue

                                if new_value in (product_data[batch_number]['serial_number'] for batch_number in
                                                 product_data):
                                    print('\n+----------------------------------------------------+')
                                    print('|⚠️ Duplication of serial number. Please enter again. |')
                                    print('+----------------------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'product_code':
                                if not validation_empty_entries(new_value):
                                    continue

                                if new_value in (product_data[batch_number]['product_code'] for batch_number in
                                                 product_data):
                                    print('\n+----------------------------------------------------+')
                                    print('|⚠️ Duplication of product code. Please enter again. |')
                                    print('+----------------------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'quantity_produced':
                                if not validation_empty_entries(new_value):
                                    continue
                                if not validation_digit_only(new_value):
                                    print('\n+---------------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter numbers only. |')
                                    print('+---------------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'batch_number':
                                if not validation_empty_entries(new_value):
                                    continue
                                if not validation_alphanum_only(new_value):
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter again. |')
                                    print('+--------------------------------------+')
                                    continue
                                if new_value in product_data:
                                    print('\n+--------------------------------------------------------+')
                                    print('|⚠️ Duplicate batch number detected. Please enter again. |')
                                    print('+--------------------------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'date_of_production':
                                if not validation_empty_entries(new_value):
                                    continue
                                if not validation_date(new_value):
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter again. |')
                                    print('+--------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'shelf_life':
                                if validation_empty_entries(attribute_of_product_data):
                                    match = re.match(r'^(\d+)\s*days$', attribute_of_product_data.strip())

                                    if match:
                                        number = int(match.group(1))
                                        if product_data[selected_product]['category'] in ['Breads', 'Muffins']:
                                            if number <= 5:
                                                break
                                            else:
                                                print('Please enter a valid shelf life. (Cannot be more than 5 days.)\n')
                                        elif product_data[selected_product]['category'] in ['Cakes', 'Pastries']:
                                            if number <= 7:
                                                break
                                            else:
                                                print('Please enter a valid shelf life. (Cannot be more than 7 days.)\n')
                                        elif product_data[selected_product]['category'] in ['Biscuits', 'Others']:
                                            if number <= 14:
                                                break
                                            else:
                                                print('Please enter a valid shelf life. (Cannot be more than 14 days.)\n')
                                    else:
                                        print("Please enter a number followed by 'days'. (Case sensitive & no special characters.)\n")

                                else:
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter again. |')
                                    print('+--------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'expiry_date':
                                if not validation_empty_entries(new_value):
                                    continue
                                if not validation_date(new_value):
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter again. |')
                                    print('+--------------------------------------+')
                                    continue
                                # convert new value from string to datetime format
                                expiry_date = datetime.strptime(new_value, '%d-%m-%Y')
                                # convert date_of _production from string to datetime format
                                date_of_production_new = datetime.strptime(product_data[selected_product]['date_of_production'], '%d-%m-%Y')

                                max_expiry = date_of_production_new + timedelta(days=product_data[selected_product]['shelf_life'] + 1)

                                if not max_expiry >= expiry_date >= date_of_production_new:
                                    print('\n+------------------------------------------------------------------------------------------------------------------------------------+')
                                    print(f'|⚠️ Invalid input. * Allowable period: {product_data[selected_product]["date_of_production"]} to {max_expiry.strftime("%d-%m-%Y")}. |')
                                    print('+------------------------------------------------------------------------------------------------------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'baker_name':
                                if not validation_empty_entries(new_value):
                                    continue
                                if not validation_alphabet_only(new_value):
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter again. |')
                                    print('+--------------------------------------+')
                                    continue

                            elif attribute_of_product_data == 'allergens':
                                if not validation_empty_entries(new_value):
                                    continue
                                if not validation_list_alphabet_only(new_value):
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter again. |')
                                    print('+--------------------------------------+')
                                    continue

                            product_data[selected_product][attribute_of_product_data] = new_value
                            print(f'\n{attribute_of_product_data} of {selected_product} is updated.')
                            save_info(product_data)
                            break

                    elif attribute_of_product_data == 'cancel':
                        print('\nCancelling. Exiting to the Product List......')
                        break

                    else:
                        print('\n❗Data not found.')
            else:
                print('\n❗Product not found.')

        except ValueError:
            print('\n+-----------------------------------------+')
            print('|⚠️ Invalid input. Please enter a number. |')
            print('+-----------------------------------------+')


product_management()
