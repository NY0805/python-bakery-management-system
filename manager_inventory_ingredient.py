import json  # import json text file to record data
import re
from datetime import datetime


# Define the function that loads data from the file
def load_data_from_inventory_ingredient():
    try:
        file = open('inventory_ingredient.txt', 'r')  # open the file and read
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
def save_info(ingredient_info):
    file = open('inventory_ingredient.txt', 'w')  # open the file to write
    json.dump(ingredient_info, file,
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


def ingredient_management():
    print('\n-------------------------------------------------------')
    print('\t\t\t\tINGREDIENT MANAGEMENT')
    print('-------------------------------------------------------')
    print('\n1. Add Ingredient')
    print('2. Update Ingredient')
    print('3. Remove Ingredient')
    print('4. Back to Previous Page')

    while True:
        option_product_management = input('\nPlease choose a service:'
                                          '\n>>> ')
        if validation_empty_entries(option_product_management):
            if option_product_management not in ['1', '2', '3', '4']:
                print('\n+--------------------------------+')
                print('|⚠️ Please enter a valid number. |')
                print('+--------------------------------+\n')
            else:
                if option_product_management == '1':
                    ingredient_details()
                    break
                elif option_product_management == '2':
                    pass
                elif option_product_management == '3':
                    pass
                elif option_product_management == '4':
                    print('\nExiting to the previous page...')
                    break


def ingredient_categories():
    print('\n-----------------------------------------------')
    print('\t\tMAIN CATEGORIES OF INGREDIENTS')
    print('-----------------------------------------------')
    print('1. Flours and Grains')
    print('2. Sweeteners')
    print('3. Fats and Oils')
    print('4. Dairy and Non-Dairy Products')
    print('5. Leavening Agents')
    print('6. Spices and Flavourings')
    print('6. Fillings and Toppings')
    print('7. Fruits and Vegetables')
    print('8. Preservatives and Stabilizers')
    print('9. Others')
    print('10. Back to Previous Page')

    while True:
        option_product_categories = input('\nPlease input the category:'
                                          '\n>>> ')
        if validation_empty_entries(option_product_categories):
            if option_product_categories not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
                print('\n+--------------------------------+')
                print('|⚠️ Please enter a valid number. |')
                print('+--------------------------------+')
                continue
            else:
                if option_product_categories == '10':
                    print('\nGoing back to the previous page......')
                    ingredient_management()
                    break
                elif option_product_categories == '1':
                    category = 'Flours and Grains'
                    break
                elif option_product_categories == '2':
                    category = 'Sweeteners'
                    break
                elif option_product_categories == '3':
                    category = 'Fats and Oils'
                    break
                elif option_product_categories == '4':
                    category = 'Dairy and Non-Dairy Products'
                    break
                elif option_product_categories == '5':
                    category = 'Leavening Agents'
                    break
                elif option_product_categories == '6':
                    category = 'Others'
                    break
    return category


def ingredient_details():
    ingredient_data = load_data_from_inventory_ingredient()

    category = ingredient_categories()

    ingredient_info = ['Ingredient Name', 'Ingredient Form', 'Batch Number', 'Unit Measurement', 'Quantity Purchased',
                       'Purchase Date (DD-MM-YYYY)', 'Expiry Date (DD-MM-YYYY)', 'Supplier Name',
                       'Supplier Contact Number (xxx-xxxxxxx)', 'Cost Per Unit', 'Storage Requirements',
                       'Allergen Information']

    max_length = 0
    for item in ingredient_info:
        if len(item) > max_length:
            max_length = len(item)

    print('\n+---------------------------------------------------------------------------+')
    print('|💡 Fill out the following fields to add a new ingredient to the inventory. |')
    print('+---------------------------------------------------------------------------+')

    while True:
        ingredient_name = input(f'1. {ingredient_info[0].ljust(max_length + 2)}: ')
        if validation_empty_entries(ingredient_name):
            if validation_alphabet_only(ingredient_name):
                break
            else:
                print('\n+------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid product name. (Cannot contain any digits and special characters.) |')
                print('+------------------------------------------------------------------------------------------+\n')

    while True:
        ingredient_form_list = {
            'Flours and Grains': 'powdered, granules, rolled (eg: oats, barley)',
            'Sweeteners': 'granulated, liquid, powdered',
            'Fats and Oils': 'solid, liquid',
            'Dairy and Non-Dairy Products': 'liquid, cream, semi-solid (eg: yogurt, cream cheese)',
            'Leavening Agents': 'powdered, granules, liquid',
            'Spices and Flavourings': 'powdered, liquid, whole (eg: cloves)',
            'Fillings and Toppings': 'solid, liquid, semi-solid (eg: pastry cream)',
            'Fruits and Vegetables': 'fresh, dried, puree (eg: applesauce, mango puree)',
            'Preservatives and Stabilizers': 'powdered, liquid, crystals'
        }

        form = ingredient_form_list.get(category, '')

        print(f'\n💡 Allowable ingredient form: {form}.💡')
        ingredient_form = input(f'2. {ingredient_info[1].ljust(max_length + 2)}: ').strip()

        allowable_form = []
        for item in form.split(','):
            allowable_form.append(item.strip().lower())

        if validation_empty_entries(ingredient_form):
            if ingredient_form.isalpha():
                if ingredient_form in allowable_form:
                    break
                else:
                    print('\n+-------------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid form from the ingredient form given. (Case Sensitive.) |')
                    print('+-------------------------------------------------------------------------------+')
            else:
                print('\n+--------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid unit. (Cannot contain any spacings, digits and special characters.) |')
                print('+--------------------------------------------------------------------------------------------+')

    while True:
        batch_number = input(f'3. {ingredient_info[2].ljust(max_length + 2)}: ')
        if validation_empty_entries(batch_number):
            if validation_alphanum_only(batch_number):
                if batch_number in ingredient_data:
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
        category_units = {
            'Flours and Grains': 'g, kg',
            'Sweeteners': 'g, kg, ml, l',
            'Fats and Oils': 'g, kg, ml, l',
            'Dairy and Non-Dairy Products': 'g, kg, ml, l',
            'Leavening Agents': 'g, kg',
            'Spices and Flavourings': 'g, kg, ml',
            'Fillings and Toppings': 'g, kg, l',
            'Fruits and Vegetables': 'g, kg, l',
            'Preservatives and Stabilizers': 'g, kg, ml'
        }

        unit = category_units.get(category, '')

        print(f'\n💡 Allowable unit measurement: {unit} 💡')
        unit_measurement = input(f'4. {ingredient_info[3].ljust(max_length + 2)}: ').strip()

        allowable_unit = []
        for item in unit.split(','):
            allowable_unit.append(item.strip().lower())

        if validation_empty_entries(unit_measurement):
            if unit_measurement.isalpha():
                if unit_measurement in allowable_unit:
                    break
                else:
                    print('\n+--------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid unit from the unit given. (Case Sensitive.) |')
                    print('+--------------------------------------------------------------------+')
            else:
                print(
                    '\n+--------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid unit. (Cannot contain any spacings, digits and special characters.) |')
                print('+--------------------------------------------------------------------------------------------+')

    while True:
        quantity_purchased = input(f'5. {ingredient_info[4].ljust(max_length + 2)}: ').strip()
        if validation_empty_entries(quantity_purchased):
            try:
                quantity_purchased = float(quantity_purchased)
                if quantity_purchased > 0:
                    break
                else:
                    print('\n+---------------------------------------------------+')
                    print('|⚠️ Please enter a valid quantity. (Greater than 0) |')
                    print('+---------------------------------------------------+\n')

            except ValueError:
                print('\n+-----------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid quantity. (Cannot contain any alphabets and special characters.) |')
                print('+-----------------------------------------------------------------------------------------+\n')

    while True:
        purchased_date = input(f'6. {ingredient_info[5].ljust(max_length + 2)}: ')
        if validation_empty_entries(purchased_date):
            if validation_date(purchased_date):
                # if purchased_date <= systemdate:
                break
            else:
                print('\n+----------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid purchase date. (With format of "day-month-year", "xx-xx-xxxx".) |')
                print('+----------------------------------------------------------------------------------------+\n')

    while True:
        expiry_date_str = input(f'7. {ingredient_info[6].ljust(max_length + 2)}: ')
        if validation_empty_entries(expiry_date_str):
            if validation_date(expiry_date_str):
                # convert expiry_date_str from string to datetime format
                expiry_date = datetime.strptime(expiry_date_str, '%d-%m-%Y')
                # convert purchase_date from string to datetime format
                purchased_date_new = datetime.strptime(purchased_date, '%d-%m-%Y')
                if expiry_date >= purchased_date_new:
                    break
                else:
                    print(
                        '\n+-----------------------------------------------------------------------------------------+')
                    print('|⚠️ The expired date does not fall within the allowable period.                         |')
                    print(
                        f'| * Allowable period: Greater than or equal to {purchased_date_new.strftime("%d-%m-%Y")}. |')
                    print(
                        '+------------------------------------------------------------------------------------------+\n')
            else:
                print('\n+----------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid purchase date. (With format of "day-month-year", "xx-xx-xxxx".) |')
                print('+----------------------------------------------------------------------------------------+\n')

    while True:
        supplier_name = input(f'8. {ingredient_info[7].ljust(max_length + 2)}: ')
        if validation_empty_entries(supplier_name):
            if re.match(r'^[a-zA-Z0-9 ]+$', supplier_name):
                break
            else:
                print('\n+--------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid supplier name. (Cannot contain any special characters.) |')
                print('+--------------------------------------------------------------------------------+\n')

    while True:
        supplier_contact = input(f'9. {ingredient_info[8].ljust(max_length + 2)}: ')
        if validation_empty_entries(supplier_contact):
            if re.fullmatch(r'^\d{3}-\d{7}$', supplier_contact):
                break
            else:
                print('\n+-----------------------------------------------+')
                print('|⚠️ Invalid contact number. Please enter again. |')
                print('+-----------------------------------------------+\n')

    while True:
        cost_per_unit = input(f'10. {ingredient_info[9].ljust(max_length + 1)}: RM ')
        if validation_empty_entries(cost_per_unit):
            if cost_per_unit.isdigit():
                if int(cost_per_unit) > 0:
                    break
                else:
                    print('\n+-----------------------------------------------+')
                    print('|⚠️ Invalid cost per unit. Must greater than 0. |')
                    print('+-----------------------------------------------+\n')
            else:
                print('\n+--------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid cost. (Cannot contain any alphabets and special characters.)  |')
                print('+--------------------------------------------------------------------------------------+\n')

    while True:
        print(f'\n💡 Allowable storage requirement: dry storage, refrigerated, freezer 💡')
        storage_requirement = input(f'11. {ingredient_info[10].ljust(max_length + 1)}: ')
        if validation_empty_entries(storage_requirement):
            if validation_alphabet_only(storage_requirement):
                if storage_requirement in ['dry storage', 'refrigerator', 'freezer']:
                    break
                else:
                    print('\n+-----------------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid storage requirement from the list given. (Case Sensitive.) |')
                    print('+-----------------------------------------------------------------------------------+\n')
            else:
                print(
                    '\n+---------------------------------------------------------------------------------------------------+')
                print(
                    '|⚠️ Please enter a valid storage requirement. (Cannot contain any digits and special characters.) |')
                print(
                    '+-------------------------------------------------------------------------------------------------+\n')

    while True:
        print(
            '\n+---------------------------------------------------------------------------------------------------------+')
        print(
            '|💡 If there is more than one data item, separate them with a space.                                      |')
        print(
            '|💡 If a name consists of more than one words, use underscore (_) to represent the space, e.g. tree_nuts. |')
        print(
            '+---------------------------------------------------------------------------------------------------------+')
        allergens = input(f'12. {ingredient_info[11].ljust(max_length + 1)}: ').split()
        if validation_empty_entries(allergens):
            if validation_list_alphabet_only(allergens):
                break
            else:
                print('\n+--------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid allergen. (Cannot contain any digits and special characters.) |')
                print('+--------------------------------------------------------------------------------------+\n')

    ingredient_data[batch_number] = {
        'category': category,
        'ingredient_name': ingredient_name,
        'ingredient_form': ingredient_form,
        'batch_number': batch_number,
        'unit_measurement': unit_measurement,
        'quantity_purchased': quantity_purchased,
        'purchase_date': purchased_date,
        'expiry_date': expiry_date_str,
        'supplier_name': supplier_name,
        'supplier_contact': supplier_contact,
        'storage_requirement': storage_requirement,
        'allergen_info': allergens
    }

    save_info(ingredient_data)

    continue_adding()


def continue_adding():
    while True:
        try:
            add_more = input('\nInformation saved. Continue adding? (y=yes, n=no)'
                             '\n>>> ')
            if add_more == 'y':
                ingredient_details()
                break
            elif add_more == 'n':
                print('\nStop adding... Exiting to Ingredient Management page......')
                ingredient_management()
                break
            else:
                print('\n+-------------------------------------------+')
                print('|⚠️ Invalid input. Please enter "y" or "n". |')
                print('+-------------------------------------------+')
        except ValueError:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')



ingredient_management()
