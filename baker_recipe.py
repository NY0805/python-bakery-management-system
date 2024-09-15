import json
import re
from collections import defaultdict


# Define the function that loads data from the file
def load_data_from_recipe():
    try:
        file = open('recipe.txt', 'r')  # open the file and read
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


def save_info(baker_recipe):
    file = open('customer.txt', 'w')  # open the file to write
    json.dump(recipe, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


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


def format_ingredient_data(product):
    return (
        f"{product['ingredient_name'].title()}"
    )


ingredient_list = load_data_from_inventory_ingredient()

ingredient_category_groups = defaultdict(list)
for value in ingredient_list.values():
    ingredient_category_groups[value['category']].append(format_ingredient_data(value))


def create_recipe():
    recipe_info = ['Recipe Name', 'Categories', 'Ingredient Name', 'Ingredient_Per_Unit', 'Variation', 'Notes']

    max_length = 0
    for item in recipe_info:
        if len(item) > max_length:
            max_length = len(item)

    while True:
        recipe_name = input(f'1. {recipe_info[0].ljust(max_length + 2)}: ')
        if validation_empty_entries(recipe_name):
            if validation_alphabet_only(recipe_name):
                break
            else:
                print('Please enter a valid recipe name. (Cannot contain any digits and special characters.)\n')

    while True:
        print('* Categories: Breads, Cakes, Pastries, Biscuits, Muffins, Others *')
        category = input(f'2. {recipe_info[1].ljust(max_length + 2)}: ')
        if validation_empty_entries(category):
            match = re.match(r'[A-Za-z]+$', category.strip())
            if match:
                if category in ['Breads', 'Cakes', 'Pastries', 'Biscuits', 'Muffins', 'Others']:
                    break
                else:
                    print('Please enter a valid category based on the categories given. (Case sensitive.)\n')
            else:
                print('Please enter a valid category. (Cannot contain any spacing, digits and special characters.)\n')

    recipe_ingredient()


def is_duplicate(ingredient_name, ingredients):
    for i in ingredients:
        if ingredient_name.lower() == i[0].lower():
            return False
    return True


def recipe_ingredient():
    ingredients = []
    while True:
        while True:
            print('\nHere are the ingredient list:')
            for category, items in ingredient_category_groups.items():
                print(f'\n* {category} *')
                for index, ingredient in enumerate(items, start=1):
                    print(f"{index}. {ingredient.title()}")

            ingredient_name = input(f'\nEnter the ingredient name: ')
            found_category = None

            if validation_empty_entries(ingredient_name):
                if validation_alphabet_only(ingredient_name):
                    if is_duplicate(ingredient_name, ingredients):
                        for category, items in ingredient_category_groups.items():
                            for item in items:
                                if ingredient_name.lower() == item.lower():
                                    found_category = category
                                    break
                            if found_category:
                                break
                        else:
                            print(
                                'Invalid ingredient name. Please enter ingredient name based on the ingredient list given.\n')
                    else:
                        print("Duplicate ingredient name. You've already added this ingredient.")
                    if found_category:
                        break
                else:
                    print(
                        'Please enter a valid ingredient name. (Cannot contain any digits and special characters.)\n')

        while True:
            category_units = {
                'Flours and Grains': 'g, kg, cups',
                'Sweeteners': 'g, ml, cups',
                'Fats and Oils': 'g, ml',
                'Dairy and Non-Dairy Products': 'g, kg, l, ml, cups',
                'Leavening Agents': 'g, tsp',
                'Spices and Flavourings': 'g, tsp, tbsp',
                'Fillings and Toppings': 'g, pieces',
                'Fruits and Vegetables': 'g, kg, pieces, cups',
                'Preservatives and Stabilizers': 'g, tsp'
            }

            unit = category_units.get(found_category, '')

            if found_category in ['Leavening Agents', 'Preservatives and Stabilizers']:
                print(f'* Allowable unit measurement: {unit}, tsp = teaspoon. *')
            elif found_category == 'Spices and Flavourings':
                print(f'* Allowable unit measurement: {unit}, tsp = teaspoon, tbsp = tablespoon. *')
            else:
                print(f'* Allowable unit measurement: {unit} *')

            unit_measurement = input(f'Enter the unit measurement of {ingredient_name}: ').strip()

            allowable_unit = []
            for item in unit.split(','):
                allowable_unit.append(item.strip().lower())

            if validation_empty_entries(unit_measurement):
                if unit_measurement.isalpha():
                    if unit_measurement in allowable_unit:
                        break
                    else:
                        print('Please enter a valid unit from the unit given. (Case Sensitive.)\n')
                else:
                    print('Please enter a valid unit. (Cannot contain any digits and special characters.)\n')

        while True:
            quantity_per_unit = input(f'Enter the quantity per unit of {ingredient_name}: ')
            if validation_empty_entries(quantity_per_unit):
                try:
                    quantity_per_unit = float(quantity_per_unit)
                    break
                except ValueError:
                    print('Please enter a valid quantity. (Cannot contain any alphabets and special characters.)\n')

        ingredient_used = [ingredient_name.lower(), quantity_per_unit, unit_measurement]
        ingredients.append(ingredient_used)

        print('\nIngredient so far:')

        max_length = 0
        for item in ingredients:
            if len(item) > max_length:
                max_length = len(item)

        for index, item in enumerate(ingredients, start=1):
            print(f'{index}. {item[0].ljust(max_length).title()} x {item[1]} {item[2]}')

        while True:
            add_more = input('\nContinue adding ingredients? (y=yes, n=no)'
                             '\n>>> ')
            if add_more == 'y':
                break
            elif add_more == 'n':
                while True:
                    ingredient_notes = input(
                        "Any additional details or notes you'd like to include for these ingredients? If not, enter 'no'.\n>>> ")
                    if validation_empty_entries(ingredient_notes):
                        if ingredient_notes.lower() == 'no':
                            print('Stop adding. Continue to instruction page......')
                            pass  # can directly call instruction function?
                            break
                        else:
                            print(f'Note added: {ingredient_notes}')
                            print('Stop adding. Continue to instruction page......')
                            pass  # can directly call instruction function?
                            break
                break  #kebujia
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        if add_more == 'n':  #kebujia
            break


def recipe_instruction():
    print("Welcome to the Recipe Instruction page! Let's get started with creating your delicious bakery goods step by step.\n")






def continue_adding_recipe():
    while True:
        try:
            add_more = input('\nContinue adding ingredients? (y=yes, n=no)'
                             '\n>>> ')
            if add_more == 'y':
                recipe_ingredient()
                break
            elif add_more == 'n':
                print('Stop adding. Exiting to product management page......')
                pass
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        except ValueError:
            print('Invalid input. Please enter again.')


create_recipe()
