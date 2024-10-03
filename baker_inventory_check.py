import json
from collections import defaultdict
import re


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


def load_data_from_baker_recipe():
    try:
        file = open('baker_recipe.txt', 'r')  # open the file and read
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


def save_info_equipment_management(equipment_management):
    file = open('notification.txt', 'w')  # open the file to write
    json.dump(equipment_management, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('❗Please enter something...\n')
        return False


def validation_alphabet_only(info):
    if re.fullmatch(r'[A-Za-z ]+', info):
        return True
    else:
        return False


def format_recipe_name(product):
    return (
        f"{product['recipe_name'].title()}"
    )


def format_recipe_data(product):
    return (
        f"{product['recipe_category']}\n"
        f"{product['recipe_name'].title()}\n"
        f"{product['ingredient_used']}\n"

    )


recipe_list = load_data_from_baker_recipe()

recipe_category_groups = defaultdict(list)
for value in recipe_list.values():
    recipe_category_groups[value['recipe_category']].append(format_recipe_name(value))


def recipe_lists():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t', '', '', 'RECIPE LIST')
        print('-----------------------------------------------\n')
        for category, items in recipe_category_groups.items():
            print(f'📍 {category} 📍')
            for index, ingredient in enumerate(items, start=1):
                print(f"{index}. {ingredient.title()}")
            print('')

        recipe_choose = input('What recipe you would like to work on today? Please enter the recipe name.\n'
                              '>>> ').strip()
        found_recipe = None

        if validation_empty_entries(recipe_choose):
            if validation_alphabet_only(recipe_choose):
                for category, items in recipe_category_groups.items():
                    for item in items:
                        if recipe_choose.lower() == item.lower():
                            found_recipe = True
                            break
                    if found_recipe:
                        break
                else:
                    print('\n+--------------------------------------------------------------------------+')
                    print('|⚠️ Invalid recipe name. Please enter recipe name based on the list given. |')
                    print('+--------------------------------------------------------------------------+')
            else:
                print('\n+-----------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid recipe name. (Cannot contain any digits and special characters.) |')
                print('+-----------------------------------------------------------------------------------------+')
        if found_recipe:
            break

    recipe_info = ['Category', 'Recipe Name', 'Ingredient Used', 'Ingredient Notes', 'Equipment Used',
                   'Baking Temperature (°C)', 'Baking Time (min)', 'Instructions']

    max_length = 0
    for item in recipe_info:
        if len(item) > max_length:
            max_length = len(item)

    print('\nHere are the details for your chosen recipe:\n')
    for values in recipe_list.values():
        if values['recipe_name'].lower() == recipe_choose.lower():
            print(f'{recipe_info[0].ljust(max_length + 2)}: {values['recipe_category']}')
            print(f'{recipe_info[1].ljust(max_length + 2)}: {values['recipe_name'].title()}')
            print(f'\n{recipe_info[2]}:')
            ingredient_index = 1
            for item in values['ingredient_used']:

                max_length = 0
                for items in values['ingredient_used']:
                    if len(items[0]) > max_length:
                        max_length = len(items[0])

                max_length_unit = 0
                for items in values['ingredient_used']:
                    if len(str(items[1])) > max_length_unit:
                        max_length_unit = len(str(items[1]))

                print(f'{ingredient_index}. {item[0].ljust(max_length + 2).title()}x  {str(item[1]).ljust(max_length_unit + 1)} {item[2]}')
                ingredient_index += 1

            print(f'\n{recipe_info[3].ljust(max_length + 2)}: {values['ingredient_notes'].title()}')
            print(f'\n{recipe_info[4]}:')
            equipment_index = 1
            for item in values['equipment_used']:
                print(f'{equipment_index}. {item.title()}')
                equipment_index += 1
            print(f'\n{recipe_info[5].ljust(max_length + 2)}: {values['baking_temperature']}')
            print(f'{recipe_info[6].ljust(max_length + 2)}: {values['baking_time']}')
            print(f'\n{recipe_info[7]}:')
            instruction_index = 1
            for instruction in values['instructions']:
                print(f'{instruction_index}. {instruction.title()}')
                instruction_index += 1









recipe_lists()
