import json  # import json text file to record data
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


def load_data_from_inventory_check():
    try:
        file = open('baker_inventory_check.txt', 'r')  # open the file and read
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


def load_data_from_baker_file():
    try:
        file = open('baker.txt', 'r')  # open the file and read
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
def save_info(product_info):
    file = open('baker_product_keeping.txt', 'w')  # open the file to write
    json.dump(product_info, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def save_info_recorded_product(inventory_check):
    file = open('baker_inventory_check.txt', 'w')  # open the file to write
    json.dump(inventory_check, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('\n❗Please enter something...\n')
        return False


def validation_list_alphabet_only(info):
    for item in info:
        if item.replace(" ", "").isalpha():
            return True
        else:
            return False


def validation_date(info, date_format='%d-%m-%Y'):
    try:
        datetime.strptime(info, date_format)
        return True
    except ValueError:
        return False


def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


unsaved_product_list = load_data_from_inventory_check()
baker_list = load_data_from_baker_file()
product_data = load_data_from_inventory_product()


def product_management():
    print('\n-------------------------------------------------------')
    print('\t\t\t\t', '', 'PRODUCT MANAGEMENT')
    print('-------------------------------------------------------')
    while True:
        # initialize the number of unsaved product to 0
        unsaved_product = 0

        # if there is any malfunction equipments or equipments that need maintenance
        for product in unsaved_product_list.values():
            unsaved_product += 1  # add the number of equipments that are malfunction to the report

        # display how many reports if the report is not empty
        if unsaved_product != 0:
            print(
                f"\n🔔 Notification: {unsaved_product} product(s) pending for record.")
            break
        else:
            pass

    print('\n1. Add Product')
    print('2. Update Product')
    print('3. Remove Product')
    print('4. Back to Previous Page')
    print('')

    while True:
        option_product_management = input('Please choose a service:'
                                          '\n>>> ')
        if validation_empty_entries(option_product_management):
            if option_product_management not in ['1', '2', '3', '4']:
                print('\n+-------------------------------+')
                print('|⚠️ Please enter a valid number.|')
                print('+-------------------------------+\n')
            else:
                if option_product_management == '1':
                    product_details()
                    break
                elif option_product_management == '2':
                    update_product()
                    break
                elif option_product_management == '3':
                    delete_product()
                elif option_product_management == '4':
                    print('\nExiting to the previous page......')
                    break


def product_categories():
    while True:
        index = 1
        print('')
        printed_centered('UNSAVED PRODUCT LIST')
        for key, value in unsaved_product_list.items():
            print(f'\n{index}.')
            for title, details in value.items():
                print(f'{title.replace("_", ' '):<20}: {details}')
            index += 1

        try:
            index_of_product_to_edit = int(
                input(
                    f'\nEnter index number to record the product to system (or enter {len(unsaved_product_list) + 1} to cancel):\n>>> '))
            if index_of_product_to_edit == len(unsaved_product_list) + 1:  # if "Cancel" is selected
                print('\nCancelling. Exiting to Product Management page......')  # return to the previous page
                product_management()
                break

            elif 1 <= index_of_product_to_edit <= len(unsaved_product_list):

                while True:
                    selected_unsaved_product = list(unsaved_product_list.keys())[
                        index_of_product_to_edit - 1]  # append all the keys into a list and identify the selected ingredient by indexing
                    print('')
                    print(
                        f'❗You are now recording {unsaved_product_list[selected_unsaved_product]["recipe_name"].title()}\'s data.')
                    break
            break

        except ValueError:
            print('\n+-------------------------------+')
            print('|⚠️ Please enter a valid number.|')
            print('+-------------------------------+\n')

    print('')
    printed_centered('MAIN TYPES OF BAKERY PRODUCTS')
    print('1. Breads')
    print('2. Cakes')
    print('3. Pastries')
    print('4. Biscuits')
    print('5. Muffins')
    print('6. Others')
    print('7. Back to Previous Page')

    while True:
        category = None
        option_product_categories = input('\nPlease choose the name of category by enter index number:'
                                          '\n>>> ')
        if validation_empty_entries(option_product_categories):
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
                elif option_product_categories == '2':
                    category = 'Cakes'
                elif option_product_categories == '3':
                    category = 'Pastries'
                elif option_product_categories == '4':
                    category = 'Biscuits'
                elif option_product_categories == '5':
                    category = 'Muffins'
                elif option_product_categories == '6':
                    category = 'Others'

        selected_unsaved_product = list(unsaved_product_list.keys())[index_of_product_to_edit - 1]

        if category == unsaved_product_list[selected_unsaved_product]["recipe_category"]:
            break
        else:
            print('\n+------------------------------------------+')
            print('|⚠️ Category must same as recipe category. |')
            print('+------------------------------------------+')
            continue

    return category, index_of_product_to_edit


def product_details():
    category, index_of_product_to_edit = product_categories()
    selected_unsaved_product = list(unsaved_product_list.keys())[index_of_product_to_edit - 1]

    product_info = ['Product Name', 'Product Code', 'Batch Number', 'Date of Production', 'Shelf Life (__ days)',
                    'Expiry Date (DD-MM-YYYY)', 'Recipe', 'Quantity Produced', 'Baker\'s Username', 'Allergens']

    max_length = 0
    for item in product_info:
        if len(item) > max_length:
            max_length = len(item)

    print('\n+------------------------------------------------------------------------+')
    print('|💡 Fill out the following fields to add a new product to the inventory. |')
    print('+------------------------------------------------------------------------+')

    while True:
        quantity_produced = input(f'1. {product_info[7].ljust(max_length + 2)}: ').strip()
        if validation_empty_entries(quantity_produced):
            if quantity_produced.isdigit():
                if int(quantity_produced) == int(unsaved_product_list[selected_unsaved_product]["production_quantity"]):
                    quantity = int(quantity_produced)
                    break
                else:
                    print('\n+-------------------------------------------------------+')
                    print('|⚠️ Quantity produced must same as production quantity. |')
                    print('+-------------------------------------------------------+\n')
            else:
                print(
                    '\n+--------------------------------------------------------------------------------------------------+')
                print(
                    '|⚠️ Please enter a valid quantity produced. (Cannot contain any alphabets and special characters.) |')
                print(
                    '+--------------------------------------------------------------------------------------------------+\n')

    while True:
        product_name = input(f'2. {product_info[0].ljust(max_length + 2)}: ').lower().strip()
        if validation_empty_entries(product_name):
            if product_name.replace(" ", "").isalpha():
                break
            else:
                print('\n+------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid product name. (Cannot contain any digits and special characters.) |')
                print('+------------------------------------------------------------------------------------------+\n')

    while True:
        product_code = input(f'3. {product_info[1].ljust(max_length + 2)}: ').strip()
        if validation_empty_entries(product_code):
            if product_code.isalnum():
                if product_code in product_data:
                    print('\n+---------------------------------------------------------------------------+')
                    print('|⚠️ Duplicate product code detected. Please input the correct product code. |')
                    print('+---------------------------------------------------------------------------+\n')
                else:
                    break
            else:
                print(
                    '\n+--------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid product code. (Cannot contain any special characters and spacings.) |')
                print(
                    '+--------------------------------------------------------------------------------------------+\n')

    while True:
        batch_number = input(f'3. {product_info[2].ljust(max_length + 2)}: ').strip()
        if validation_empty_entries(batch_number):
            if batch_number.isalnum():
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
        date_of_production = input(f'4. {product_info[3].ljust(max_length + 2)}: ').strip()
        if validation_empty_entries(date_of_production):
            if validation_date(date_of_production):
                if date_of_production == unsaved_product_list[selected_unsaved_product]["date_of_production"]:
                    break
                else:
                    print('\n+--------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid date of production based on the date given above. |')
                    print('+--------------------------------------------------------------------------+\n')
            else:
                print(
                    '\n+---------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid date of production. (With format of "day-month-year", "xx-xx-xxxx".) |')
                print(
                    '+---------------------------------------------------------------------------------------------+\n')

    while True:
        shelf_life = input(f'5. {product_info[4].ljust(max_length + 2)}: ').strip()
        if validation_empty_entries(shelf_life):
            if shelf_life.isdigit():
                number = int(shelf_life)
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
                print('\n+---------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a number. (Cannot contain any alphabets and special characters.) |')
                print('+----------------------------------------------------------------------------------+\n')

    while True:
        expiry_date_str = input(f'6. {product_info[5].ljust(max_length + 2)}: ').strip()
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
                    print(
                        '\n+---------------------------------------------------------------------------------------------------------+')
                    print(
                        '|⚠️ The expired date does not fall within the allowable period.                                           |')
                    print(
                        '|   The allowable period must between the date of production and date of production + shelf life + 1 day. |')
                    print(
                        f'| * Allowable period: {date_of_production} to {max_expiry.strftime("%d-%m-%Y")}.                                                           |')
                    print(
                        '+---------------------------------------------------------------------------------------------------------+\n')
            else:
                print('\n+--------------------------------------------------------------------+')
                print('|⚠️ Invalid date format. Please enter the date in DD-MM-YYYY format. |')
                print('+--------------------------------------------------------------------+\n')

    while True:
        baker_name = input(f'8. {product_info[8].ljust(max_length + 2)}: ')
        if validation_empty_entries(baker_name):
            if baker_name.isalnum():
                if baker_name in baker_list.keys():
                    break
                else:
                    print('\n+----------------------------------------+')
                    print('|⚠️ Please enter a valid baker username. |')
                    print('+----------------------------------------+\n')
            else:
                print('\n+-----------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid baker username. (Cannot contain any special characters.) |')
                print('+-----------------------------------------------------------------------------+\n')

    while True:
        print(
            '\n+---------------------------------------------------------------------------------------------------------+')
        print(
            '|💡 If there is more than one data item, separate them with a space.                                      |')
        print(
            '|💡 If a name consists of more than one words, use underscore (_) to represent the space, e.g. tree_nuts. |')
        print(
            '+---------------------------------------------------------------------------------------------------------+\n')
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
                if serial_number.isalnum():
                    serial_numbers.append(serial_number)
                else:
                    print(
                        '\n+---------------------------------------------------------------------------------------------+')
                    print(
                        '|⚠️ Please enter a valid serial number. (Cannot contain any special characters and spacings.) |')
                    print(
                        '+---------------------------------------------------------------------------------------------+\n')
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
        'baker_name': baker_name,
        'allergens': allergens
    }

    save_info(product_data)

    del unsaved_product_list[selected_unsaved_product]  # delete the selected product
    save_info_recorded_product(unsaved_product_list)

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


# function to update product information
def update_product():
    while True:
        index = 1
        print('')
        printed_centered('PRODUCT LIST')
        for batch_number, product in product_data.items():
            print(f'{index}. {product["product_name"].title()}')
            index += 1
        print(f'{len(product_data) + 1}. Cancel')

        try:
            index_of_product_to_edit = int(input(
                f'\nEnter index number to update the information of the product (or enter {len(product_data) + 1} to cancel):\n>>> '))

            if index_of_product_to_edit == len(product_data) + 1:  # if "Cancel" is selected
                print('\nCancelling. Exiting to Product Management page......')  # return to the previous page
                product_management()
                break

            elif 1 <= index_of_product_to_edit <= len(product_data):
                for batch_number, product in product_data.items():
                    # append all the keys into a list and identify the selected ingredient by indexing
                    selected_product_key = list(product_data.keys())[index_of_product_to_edit - 1]

                    print('')
                    printed_centered(f'{product_data[selected_product_key]["product_name"].upper()}\'S DATA')

                    for key, value in product_data[selected_product_key].items():
                        print(f'{key}: {value}')  # list down the attributes of the selected product
                    break
            else:
                print('\n❗Product not found.')  # error displayed if selected product not found
                continue

        except ValueError:
            print('\n+-----------------------------------------+')
            print('|⚠️ Invalid input. Please enter a number. |')
            print('+-----------------------------------------+')
            continue

        while True:
            selected_product_key = list(product_data.keys())[index_of_product_to_edit - 1]

            print('\nTo change the information, please enter the exact matching name. Example: product_name.')
            print('* Note: category, date of production, and quantity produced cannot be changed.\n')

            attribute_of_product_data = input('Which information do you want to update? (or enter \"cancel\")\n>>> ')

            if attribute_of_product_data == 'cancel':
                print('\nCancelling. Exiting to the Product List......')
                update_product()
                break
            elif attribute_of_product_data == 'serial_number':
                while True:
                    index = 1
                    print('')
                    for number in product_data[selected_product_key]['serial_number']:
                        print(f'Serial number {index:<2}: {number}')
                        index += 1
                    print('')

                    edit_serial_number = input(
                        "Please enter the serial number you want to edit (or enter 'cancel')\n>>> ")
                    if edit_serial_number == 'cancel':
                        break
                    elif edit_serial_number not in product_data[selected_product_key]['serial_number']:
                        print('\n+---------------------------------------+')
                        print('|⚠️ Please enter a valid serial number. |')
                        print('+---------------------------------------+')
                        continue
                    else:
                        while True:
                            new_serial_number = input('\nEnter the new serial number: ').strip()
                            if validation_empty_entries(new_serial_number):
                                if new_serial_number.isalnum():
                                    if new_serial_number not in product_data[selected_product_key]['serial_number']:
                                        index_to_update = product_data[selected_product_key]['serial_number'].index(
                                            edit_serial_number)
                                        product_data[selected_product_key]['serial_number'][
                                            index_to_update] = new_serial_number
                                        save_info(product_data)
                                        print('\nInformation saved.')
                                        update_product()
                                        break
                                    else:
                                        print('\n+----------------------------------------------------+')
                                        print('|⚠️ Duplication of serial number. Please enter again. |')
                                        print('+----------------------------------------------------+')
                                        continue
                                else:
                                    print(
                                        '\n+---------------------------------------------------------------------------------------------+')
                                    print(
                                        '|⚠️ Please enter a valid serial number. (Cannot contain any spacings and special characters.) |')
                                    print(
                                        '+---------------------------------------------------------------------------------------------+')
                                    continue

            elif attribute_of_product_data == 'allergens':
                while True:
                    index = 1
                    print('')
                    for allergen in product_data[selected_product_key]['allergens']:
                        print(f'{index}. {allergen}')
                        index += 1
                    print('')

                    edit_choice = input("Add, edit or delete allergens? \nPlease enter 'add', 'edit' or 'delete' (or enter 'cancel' to stop): ")

                    if edit_choice == 'add':
                        new_allergen_list = []
                        while True:
                            new_allergen = input("\nEnter the new allergen (enter 'done' to stop): ").strip()
                            if validation_empty_entries(new_allergen):
                                if new_allergen == 'done':
                                    if new_allergen_list:
                                        product_data[selected_product_key]['allergens'].extend(new_allergen_list)
                                        save_info(product_data)
                                        print('\nInformation saved.')
                                        break
                                    else:
                                        print('\nNo new allergens added.')
                                        break
                                elif new_allergen.replace(" ", "").isalpha():
                                    new_allergen_list.append(new_allergen)
                                else:
                                    print(
                                        '\n+--------------------------------------------------------------------------------------+')
                                    print(
                                        '|⚠️ Please enter a valid allergen. (Cannot contain any digits and special characters.) |')
                                    print(
                                        '+--------------------------------------------------------------------------------------+')
                                    continue

                    elif edit_choice == 'edit':
                        while True:
                            try:
                                edit_allergen = input(
                                    "\nPlease enter the index number of allergen you want to edit (or enter 'cancel')\n>>> ")

                                if not validation_empty_entries(edit_allergen):
                                    continue

                                if edit_allergen == 'cancel':
                                    break

                                edit_allergen = int(edit_allergen)

                                if 1 <= edit_allergen <= len(product_data[selected_product_key]['allergens']):
                                    while True:
                                        new_allergen = input("\nEnter the new allergen: ").strip()
                                        if validation_empty_entries(new_allergen):
                                            if new_allergen.replace(" ", "").isalpha():
                                                product_data[selected_product_key]['allergens'][edit_allergen - 1] = new_allergen
                                                save_info(product_data)
                                                print('\nInformation saved.')
                                                break
                                            else:
                                                print(
                                                    '\n+--------------------------------------------------------------------------------------+')
                                                print(
                                                    '|⚠️ Please enter a valid allergen. (Cannot contain any digits and special characters.) |')
                                                print(
                                                    '+--------------------------------------------------------------------------------------+')
                                                continue
                                    break
                                else:
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Please enter a valid index number. |')
                                    print('+--------------------------------------+')
                                    continue
                            except ValueError:
                                print('\n+--------------------------------------+')
                                print('|⚠️ Please enter a valid index number. |')
                                print('+--------------------------------------+')
                                continue

                    elif edit_choice == 'delete':
                        while True:
                            try:
                                delete_allergen = input(
                                    "\nPlease enter the index number of allergen you want to delete (or enter 'cancel')\n>>> ").lower().strip()
                                if not validation_empty_entries(delete_allergen):
                                    continue

                                if delete_allergen == 'cancel':
                                    break

                                delete_allergen = int(delete_allergen)

                                if 1 <= delete_allergen <= len(product_data[selected_product_key]['allergens']):
                                    del product_data[selected_product_key]['allergens'][delete_allergen - 1]
                                    save_info(product_data)
                                    print('\nAllergen deleted.')
                                    break
                                else:
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Please enter a valid index number. |')
                                    print('+--------------------------------------+')
                                    continue
                            except ValueError:
                                print('\n+--------------------------------------+')
                                print('|⚠️ Please enter a valid index number. |')
                                print('+--------------------------------------+')
                                continue
                    elif edit_choice == 'cancel':
                        break

                    else:
                        print('\n+-----------------------------------------------------+')
                        print('|⚠️ Please enter "add", "edit", "delete" or "cancel". |')
                        print('+-----------------------------------------------------+')
                        continue

            elif attribute_of_product_data in product and attribute_of_product_data not in ['date_of_production', 'quantity_produced', 'category']:
                while True:
                    new_value = input(f'\nEnter new {attribute_of_product_data}: ').strip()
                    # continue to validate the value entered for each attribute

                    if attribute_of_product_data == 'product_name':
                        if not validation_empty_entries(new_value):
                            continue
                        if not new_value.replace(" ", "").isalpha():
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')
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

                    elif attribute_of_product_data == 'batch_number':
                        if not validation_empty_entries(new_value):
                            continue
                        if not new_value.isalnum():
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')
                            continue
                        if new_value in product_data:
                            print('\n+--------------------------------------------------------+')
                            print('|⚠️ Duplicate batch number detected. Please enter again. |')
                            print('+--------------------------------------------------------+')
                            continue

                    elif attribute_of_product_data == 'shelf_life':
                        if validation_empty_entries(new_value):
                            if new_value.isdigit():
                                number = int(new_value)
                                if product_data[selected_product_key]['category'] in ['Breads', 'Muffins']:
                                    if number <= 5:
                                        break
                                    else:
                                        print('\n+------------------------------------------------------------------+')
                                        print('|⚠️ Please enter a valid shelf life. (Cannot be more than 5 days.) |')
                                        print('+------------------------------------------------------------------+')
                                        continue
                                elif product_data[selected_product_key]['category'] in ['Cakes', 'Pastries']:
                                    if number <= 7:
                                        break
                                    else:
                                        print('\n+------------------------------------------------------------------+')
                                        print('|⚠️ Please enter a valid shelf life. (Cannot be more than 7 days.) |')
                                        print('+------------------------------------------------------------------+')
                                        continue
                                elif product_data[selected_product_key]['category'] in ['Biscuits', 'Others']:
                                    if number <= 14:
                                        break
                                    else:
                                        print('\n+-------------------------------------------------------------------+')
                                        print('|⚠️ Please enter a valid shelf life. (Cannot be more than 14 days.) |')
                                        print('+-------------------------------------------------------------------+')
                                        continue
                            else:
                                print(
                                    '\n+---------------------------------------------------------------------------------+')
                                print(
                                    '|⚠️ Please enter a number. (Cannot contain any alphabets and special characters.) |')
                                print(
                                    '+----------------------------------------------------------------------------------+')
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
                        date_of_production_new = datetime.strptime(
                            product_data[selected_product_key]['date_of_production'],
                            '%d-%m-%Y')

                        max_expiry = date_of_production_new + timedelta(days=int(product_data[selected_product_key]['shelf_life']) + 1)

                        if not (max_expiry >= expiry_date >= date_of_production_new):
                            print(
                                '\n+----------------------------------------------------------------+')
                            print(
                                f'|⚠️ Invalid input. * Allowable period: {product_data[selected_product_key]["date_of_production"]} to {max_expiry.strftime("%d-%m-%Y")}. |')
                            print(
                                '+----------------------------------------------------------------+')
                            continue

                    elif attribute_of_product_data == 'baker_name':
                        if not validation_empty_entries(new_value):
                            continue
                        if not new_value.isalnum():
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')
                            continue
                        if new_value not in baker_list.keys():
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')
                            continue

                    print(
                        f'\n{attribute_of_product_data} of {selected_product_key} is updated.')  # inform user about the data is updated
                    product_data[selected_product_key].update(
                        {attribute_of_product_data: new_value})  # assign the new value entered to the attributes
                    save_info(product_data)  # save the data
                    break

            else:
                print('\n❗Data not found.')


def delete_product():
    while True:
        index = 1
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'PRODUCT LIST')
        print('-----------------------------------------------')
        for name, info in product_data.items():
            print(f'{index}. {name.title()}')
            index += 1
        print(f'{len(product_data) + 1}. cancel')

        try:
            index_remove_product = int(
                input(f'\nWhich product do you want to remove? (or enter {len(product_data) + 1} to cancel)\n>>> '))
            if index_remove_product == len(product_data) + 1:  # cancel the process
                print('\nCancelling. Exiting to Services page......')
                product_management()
                break

            elif 1 <= index_remove_product <= len(product_data):
                product_to_remove = list(product_data.keys())[index_remove_product - 1]  # identify baker to remove by accesing the index of key of baker
                del product_data[product_to_remove]  # delete the selected baker
                save_info(product_data)
                print(
                    f'\n{product_to_remove.title()} is removed.\n')  # inform user that the selected baker is removed successfully

                while True:
                    remove_more = input(
                        'Continue to remove? (y=yes, n=no)\n>>> ')  # ask user if they want to continue removing
                    if remove_more == 'y':
                        break
                    elif remove_more == 'n':
                        print('\nStop removing. Exiting to Services page......')
                        product_management()
                        break
                    else:
                        print('\n+--------------------------------------+')
                        print('|⚠️ Invalid input. Please enter again. |')
                        print('+--------------------------------------+')
                    break
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

        except ValueError:
            print('\n+-----------------------------------------+')
            print('|⚠️ Invalid input. Please enter a number. |')
            print('+-----------------------------------------+')


#update_product()
#product_management()
