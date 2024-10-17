import json  # import json text file to record data
import re
from datetime import datetime  # %I = 01-12, %H = 00-23


# Define the function that loads ingredient inventory data from the file
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


# Define the function that saves ingredient inventory data to the file
def save_info(ingredient_data):
    file = open('inventory_ingredient.txt', 'w')  # open the file to write
    json.dump(ingredient_data, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# define the function to print content in center
def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('\n❗Please enter something...')
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


ingredient_data = load_data_from_inventory_ingredient() # store the data that retrieved from file into ingredient_data


# define function to manage ingredient in the inventory
def ingredient_management():
    while True:
        print('\n-------------------------------------------------------')
        print('\t\t\t\tINGREDIENT MANAGEMENT')
        print('-------------------------------------------------------')
        print(
            '1. Add Ingredients\n2. Remove Ingredients\n3. Update Ingredients\n4. Back to Main Inventory Management⛔🔙')

        option_product_management = input('\nWhat action do you wish to perform? (1, 2, 3, 4)\n>>> ')
        if validation_empty_entries(option_product_management):
            if option_product_management not in ['1', '2', '3', '4']:
                print('\n+--------------------------------+')
                print('|⚠️ Please enter a valid number. |')
                print('+--------------------------------+')
            else:
                if option_product_management == '1':
                    add_ingredient()
                elif option_product_management == '2':
                    pass
                elif option_product_management == '3':
                    update_ingredient()
                elif option_product_management == '4':
                    print('\nExiting to Main Inventory Management page...')
                    break


def ingredient_categories():
    while True:
        print('\n-----------------------------------------------')
        print('\t\tMAIN CATEGORIES OF INGREDIENTS')
        print('-----------------------------------------------')
        print('1. Flours and Grains')
        print('2. Sweeteners')
        print('3. Fats and Oils')
        print('4. Dairy and Non-Dairy Products')
        print('5. Leavening Agents')
        print('6. Spices and Flavourings')
        print('7. Fillings and Toppings')
        print('8. Fruits and Vegetables')
        print('9. Preservatives and Stabilizers')
        print('10. Others')
        print('11. Back to Ingredient Management page')

        option_product_categories = input('\nPlease input the category:'
                                          '\n>>> ')
        if validation_empty_entries(option_product_categories):
            if option_product_categories not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', "11"]:
                print('\n+--------------------------------+')
                print('|⚠️ Please enter a valid number. |')
                print('+--------------------------------+')
                continue
            else:
                if option_product_categories == '10':
                    print('\nGoing back to Ingredient Management page......')
                    ingredient_management()
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
                    category = 'Spices and Flavourings'
                    break
                elif option_product_categories == '7':
                    category = 'Fillings and Toppings'
                    break
                elif option_product_categories == '8':
                    category = 'Fruits and Vegetables'
                    break
                elif option_product_categories == '9':
                    category = 'Preservatives and Stabilizers'
                    break
                elif option_product_categories == '10':
                    category = 'Others'
                    break
    return category


def add_ingredient():
    category = ingredient_categories()

    ingredient_info = ['Ingredient Name', 'Ingredient Form', 'Batch Number', 'Unit Measurement', 'Total Quantity Purchased',
                       'Purchase Date (DD-MM-YYYY)', 'Expiry Date (DD-MM-YYYY)', 'Supplier Name',
                       'Supplier Contact Number (xxx-xxxxxxx)', 'Cost Per Unit', 'Storage Requirements',
                       'Allergen Information', 'Quantity Per Unit']

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
                print('|⚠️ Please enter a valid ingredient name. (Cannot contain any digits and special characters.) |')
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
            print(allowable_form)

        if validation_empty_entries(ingredient_form):
            if ingredient_form.isalpha():
                if ingredient_form in allowable_form:
                    break
                else:
                    print('\n+-------------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid form from the ingredient form given. (Case Sensitive.) |')
                    print('+-------------------------------------------------------------------------------+')
            else:
                print(
                    '\n+--------------------------------------------------------------------------------------------+')
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
        cost_per_unit = input(f'5. {ingredient_info[9].ljust(max_length + 2)}: ').strip()
        if validation_empty_entries(cost_per_unit):
            try:
                cost_per_unit = float(cost_per_unit)
                if cost_per_unit > 0:
                    break
                else:
                    print('\n+-----------------------------------------------+')
                    print('|⚠️ Please enter a valid cost. (Greater than 0) |')
                    print('+-----------------------------------------------+\n')

            except ValueError:
                print('\n+-------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid cost. (Cannot contain any alphabets and special characters.) |')
                print('+-------------------------------------------------------------------------------------+\n')

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
                if purchased_date <= datetime.now().strftime("%d-%m-%Y"):
                    break
                else:
                    print('\n+-------------------------------------------------------+')
                    print('|⚠️ Purchased date should not larger than current date. |')
                    print('+-------------------------------------------------------+\n')
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
                    print('\n+---------------------------------------------------------------+')
                    print('|⚠️ The expired date does not fall within the allowable period. |')
                    print(f'| * Allowable period: Greater than or equal to {purchased_date_new.strftime("%d-%m-%Y")}.      |')
                    print('+---------------------------------------------------------------+\n')

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
        print(f'\n💡 Allowable storage requirement: dry storage, refrigerated, freezer 💡')
        storage_requirement = input(f'11. {ingredient_info[10].ljust(max_length + 1)}: ')
        if validation_empty_entries(storage_requirement):
            if validation_alphabet_only(storage_requirement):
                if storage_requirement in ['dry storage', 'refrigerated', 'freezer']:
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
        'cost_per_unit': f'RM {cost_per_unit:.2f}',
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
                add_ingredient()
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


# function to update ingredient details in the inventory
def update_ingredient():
    while True:
        index = 1
        print('\n-----------------------------------------------')
        print('\t\t\t\tINGREDIENT LIST')
        print('-----------------------------------------------')
        for key, value in ingredient_data.items():
            print(f'{index}. {value["ingredient_name"].title()}')
            index += 1
        print(f'{len(ingredient_data) + 1}. cancel')

        try:
            ingredient_to_update = int(input('\nEnter the ingredient\'s index number to update: '))  # identify which ingredient to update
            if ingredient_to_update == len(ingredient_data) + 1:  # cancel update
                print('\nCancelling. Exiting to Ingredient Management page......')
                break

            elif 1 <= ingredient_to_update <= len(ingredient_data):
                selected_ingredient = list(ingredient_data.keys())[ingredient_to_update - 1]  # append all the keys into a list and identify the selected ingredient by indexing
                while True:
                    print('')
                    printed_centered(ingredient_data[selected_ingredient]["ingredient_name"].upper())  # display the ingredient name

                    # display the details of ingredient in a custom format
                    for ingredient_data_key, ingredient_data_value in (ingredient_data[selected_ingredient].items()):
                        if ingredient_data_key == 'allergen_info':
                            print(f'{ingredient_data_key:<20}: {", ".join(ingredient_data_value)}')
                        else:
                            print(f'{ingredient_data_key:<20}: {ingredient_data_value}')

                    attribute_of_ingredient_data = input('\nWhich information do you want to update? (or enter \"cancel\")\n>>> ')

                    # gather the category of ingredients into a list
                    categories = ['Flours and Grains', 'Sweeteners', 'Fats and Oils', 'Dairy and Non-Dairy Products',
                                  'Leavening Agents', 'Spices and Flavourings', 'Fillings and Toppings',
                                  'Fruits and Vegetables', 'Preservatives and Stabilizers', 'Others']
                    if validation_empty_entries(attribute_of_ingredient_data):
                        if attribute_of_ingredient_data in ingredient_data[selected_ingredient]:
                            if attribute_of_ingredient_data == 'category':
                                print('')
                                # display tne category in 2 lines
                                print(*categories[0:5], sep=' ▫️ ')
                                print(*categories[5:], sep=' ▫️ ')

                            elif attribute_of_ingredient_data == 'ingredient_form':
                                # determine the form of each ingredient
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

                                category = ingredient_data[selected_ingredient]['category']  # access the category for the selected ingredient
                                form = ingredient_form_list.get(category, '')  # determine the allowable form for the selected ingredient
                                print(f'\n💡 Allowable ingredient form: {form}.💡')

                            elif attribute_of_ingredient_data == 'unit_measurement':
                                # determine the unit measurements for each ingredient category
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
                                category = ingredient_data[selected_ingredient]['category']
                                unit = category_units.get(category, '')  # determine the allowable unit measurement for the selected ingredient
                                print(f'\n💡 Allowable unit measurement: {unit} 💡')

                            elif attribute_of_ingredient_data == 'storage_requirement':
                                print(f'\n💡 Allowable storage requirement: dry storage, refrigerated, freezer 💡')

                            elif attribute_of_ingredient_data == 'allergen_info':
                                print(
                                    '\n+---------------------------------------------------------------------------------------------------------+')
                                print(
                                    '|💡 If there is more than one data item, separate them with a space.                                      |')
                                print(
                                    '|💡 If a name consists of more than one words, use underscore (_) to represent the space, e.g. tree_nuts. |')
                                print(
                                    '+---------------------------------------------------------------------------------------------------------+')

                            while True:

                                new_value = input(f'\nEnter new {attribute_of_ingredient_data}: ')  # collect new value for the selected attribute

                                # validate new value for each attribute
                                if attribute_of_ingredient_data == 'category':
                                    if new_value not in [category.lower() for category in categories]:
                                        print('\n+--------------------------------------+')
                                        print('|⚠️ Out of category. Please enter again. |')
                                        print('+----------------------------------------+')
                                    else:
                                        break

                                if attribute_of_ingredient_data == 'ingredient_name':
                                    if validation_alphabet_only(new_value):
                                        # if the new ingredient name existed, duplication occurs
                                        if new_value in (ingredient_data[selected_ingredient]['ingredient_name'] for
                                                         selected_ingredient in ingredient_data):
                                            print(
                                                '\n+-----------------------------------------------------------------------------+')
                                            print(
                                                '|⚠️ Duplicate ingredient name detected. Please enter another ingredient name. |')
                                            print(
                                                '+-----------------------------------------------------------------------------+')
                                        else:
                                            break
                                    else:
                                        print(
                                            '\n+---------------------------------------------------------------------------------------------+')
                                        print(
                                            '|⚠️ Please enter a valid ingredient name. (Cannot contain any digits and special characters.) |')
                                        print(
                                            '+---------------------------------------------------------------------------------------------+')

                                if attribute_of_ingredient_data == 'ingredient_form':

                                    if validation_empty_entries(new_value):
                                        if validation_list_alphabet_only(new_value):
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

                                            category = ingredient_data[selected_ingredient]['category']
                                            form = ingredient_form_list.get(category, '')
                                            allowable_form = []
                                            for item in form.split(','):
                                                allowable_form.append(item.strip().lower())

                                            if new_value in allowable_form:  # validate new unit is in the list of allowable form
                                                break
                                            else:
                                                print(
                                                    '\n+-------------------------------------------------------------------------------+')
                                                print(
                                                    '|⚠️ Please enter a valid form from the ingredient form given. (Case Sensitive.) |')
                                                print(
                                                    '+-------------------------------------------------------------------------------+')
                                        else:
                                            print(
                                                '\n+--------------------------------------------------------------------------------------------+')
                                            print(
                                                '|⚠️ Please enter a valid form. (Cannot contain any spacings, digits and special characters.) |')
                                            print(
                                                '+--------------------------------------------------------------------------------------------+')

                                if attribute_of_ingredient_data == 'batch_number':
                                    if validation_alphanum_only(new_value):
                                        if new_value in ingredient_data:  # if the new batch number existed, duplication occurs
                                            print(
                                                '\n+---------------------------------------------------------------------------+')
                                            print(
                                                '|⚠️ Duplicate batch number detected. Please input the correct batch number. |')
                                            print(
                                                '+---------------------------------------------------------------------------+')
                                        else:
                                            break
                                    else:
                                        print(
                                            '\n+-------------------------------------------------------------------------------+')
                                        print(
                                            '|⚠️ Please enter a valid batch number. (Cannot contain any special characters.) |')
                                        print(
                                            '+-------------------------------------------------------------------------------+')

                                if attribute_of_ingredient_data == 'unit_measurement':
                                    if new_value.isalpha():
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
                                        category = ingredient_data[selected_ingredient]['category']
                                        unit = category_units.get(category, '')
                                        allowable_unit = []
                                        for item in unit.split(','):
                                            allowable_unit.append(item.strip().lower())

                                        if new_value in allowable_unit:  # validate new unit is in the list of allowable unit
                                            break
                                        else:
                                            print(
                                                '\n+--------------------------------------------------------------------+')
                                            print(
                                                '|⚠️ Please enter a valid unit from the unit given. (Case Sensitive.) |')
                                            print(
                                                '+--------------------------------------------------------------------+')
                                    else:
                                        print(
                                            '\n+--------------------------------------------------------------------------------------------+')
                                        print(
                                            '|⚠️ Please enter a valid unit. (Cannot contain any spacings, digits and special characters.) |')
                                        print(
                                            '+--------------------------------------------------------------------------------------------+')

                                if attribute_of_ingredient_data == 'quantity_purchased':
                                    try:
                                        new_value = float(new_value)
                                        if new_value > 0:  # ensure the quantity must in positive
                                            break
                                        else:
                                            print('\n+---------------------------------------------------+')
                                            print('|⚠️ Please enter a valid quantity. (Greater than 0) |')
                                            print('+---------------------------------------------------+')

                                    except ValueError:
                                        print(
                                            '\n+-----------------------------------------------------------------------------------------+')
                                        print(
                                            '|⚠️ Please enter a valid quantity. (Cannot contain any alphabets and special characters.) |')
                                        print(
                                            '+-----------------------------------------------------------------------------------------+')

                                if attribute_of_ingredient_data == 'purchase_date':
                                    if validation_date(new_value):
                                        if new_value <= datetime.now().strftime("%d-%m-%Y"):  # make sure the new purchased date entered is valid and logic
                                            break
                                        else:
                                            print('\n+-------------------------------------------------------+')
                                            print('|⚠️ Purchased date should not larger than current date. |')
                                            print('+-------------------------------------------------------+\n')
                                    else:
                                        print(
                                            '\n+----------------------------------------------------------------------------------------+')
                                        print(
                                            '|⚠️ Please enter a valid purchase date. (With format of "day-month-year", "xx-xx-xxxx".) |')
                                        print(
                                            '+----------------------------------------------------------------------------------------+')

                                if attribute_of_ingredient_data == 'expiry_date':
                                    if validation_date(new_value):
                                        # convert expiry_date_str from string to datetime format
                                        expiry_date = datetime.strptime(new_value, '%d-%m-%Y')
                                        # convert purchase_date from string to datetime format
                                        purchased_date_new = datetime.strptime(
                                            ingredient_data[selected_ingredient]['purchase_date'], '%d-%m-%Y')
                                        if expiry_date >= purchased_date_new:  # ensure the expiry date is after the purchased date
                                            break
                                        else:
                                            print('\n+---------------------------------------------------------------+')
                                            print('|⚠️ The expired date does not fall within the allowable period. |')
                                            print(f'| * Allowable period: Greater than or equal to {purchased_date_new.strftime("%d-%m-%Y")}.      |')
                                            print('+---------------------------------------------------------------+')
                                    else:
                                        print(
                                            '\n+--------------------------------------------------------------------------------------+')
                                        print(
                                            '|⚠️ Please enter a valid expiry date. (With format of "day-month-year", "xx-xx-xxxx".) |')
                                        print(
                                            '+--------------------------------------------------------------------------------------+')

                                if attribute_of_ingredient_data == 'supplier_name':
                                    if new_value.replace(" ", "").isalpha():
                                        break
                                    else:
                                        print(
                                            '\n+--------------------------------------------------------------------------------+')
                                        print(
                                            '|⚠️ Please enter a valid supplier name. (Cannot contain any special characters.) |')
                                        print(
                                            '+--------------------------------------------------------------------------------+')

                                if attribute_of_ingredient_data == 'supplier_contact':
                                    if re.fullmatch(r'^\d{3}-\d{7}$', new_value):  # validate the format of supplier's contact number
                                        break
                                    else:
                                        print('\n+-----------------------------------------------+')
                                        print('|⚠️ Invalid contact number. Please enter again. |')
                                        print('+-----------------------------------------------+')

                                if attribute_of_ingredient_data == 'cost_per_unit':
                                    if validation_empty_entries(new_value):
                                        if new_value.isdigit():
                                            if int(new_value) > 0:
                                                break
                                            else:
                                                print('\n+-----------------------------------------------+')
                                                print('|⚠️ Invalid cost per unit. Must greater than 0. |')
                                                print('+-----------------------------------------------+\n')
                                        else:
                                            print('\n+--------------------------------------------------------------------------------------+')
                                            print('|⚠️ Please enter a valid cost. (Cannot contain any alphabets and special characters.)  |')
                                            print('+--------------------------------------------------------------------------------------+\n')

                                if attribute_of_ingredient_data == 'storage_requirement':
                                    if validation_alphabet_only(new_value):
                                        if new_value in ['dry storage', 'refrigerated', 'freezer']:
                                            break
                                        else:
                                            print(
                                                '\n+-----------------------------------------------------------------------------------+')
                                            print(
                                                '|⚠️ Please enter a valid storage requirement from the list given. (Case Sensitive.) |')
                                            print(
                                                '+-----------------------------------------------------------------------------------+')
                                    else:
                                        print(
                                            '\n+---------------------------------------------------------------------------------------------------+')
                                        print(
                                            '|⚠️ Please enter a valid storage requirement. (Cannot contain any digits and special characters.) |')
                                        print(
                                            '+-------------------------------------------------------------------------------------------------+')

                                if attribute_of_ingredient_data == 'allergen_info':
                                    if validation_list_alphabet_only(new_value):
                                        break
                                    else:
                                        print(
                                            '\n+--------------------------------------------------------------------------------------+')
                                        print(
                                            '|⚠️ Please enter a valid allergen. (Cannot contain any digits and special characters.) |')
                                        print(
                                            '+--------------------------------------------------------------------------------------+')

                        elif attribute_of_ingredient_data == 'cancel':
                            print('\nCancelling. Exiting to Ingredient List......')
                            break

                        else:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')
                            continue

                        # display a message that inform users the information is updated
                        print(f'\n{attribute_of_ingredient_data} of {ingredient_data[selected_ingredient]["ingredient_name"]} is updated.')
                        ingredient_data[selected_ingredient].update({attribute_of_ingredient_data: new_value})
                        save_info(ingredient_data)

        except ValueError:
            print('\n+--------------------------+')
            print('|⚠️ Please enter a number. |')
            print('+--------------------------+')


#update_ingredient()
#ingredient_management()

