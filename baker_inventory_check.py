import json
import random


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


def save_info_inventory_check(product_produce):
    file = open('baker_inventory_check.txt', 'w')  # open the file to write
    json.dump(product_produce, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def save_info_inventory_ingredient(ingredient_used):
    file = open('inventory_ingredient.txt', 'w')  # open the file to write
    json.dump(ingredient_used, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('❗Please enter something...\n')
        return False


def format_recipe_name(product):
    return (
        f"{product['recipe_name'].title()}"
    )


def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


product_list = load_data_from_inventory_check()
recipe_list = load_data_from_baker_recipe()
ingredient_list = load_data_from_inventory_ingredient()

recipe_category_groups = {}
for value in recipe_list.values():
    recipe_category = value['recipe_category']

    if recipe_category not in recipe_category_groups:
        recipe_category_groups[recipe_category] = []

    recipe_category_groups[recipe_category].append(format_recipe_name(value))


def recipe_lists():
    while True:
        while True:
            report_num = random.randint(1000, 9999)
            if report_num not in product_list.keys():
                break

        print('')
        printed_centered('RECIPE LIST')
        for category, items in recipe_category_groups.items():
            print(f'📍 {category} 📍')
            for index, ingredient in enumerate(items, start=1):
                print(f"{index}. {ingredient.title()}")
            print('')

        recipe_choose = input('What recipe you would like to work on today? Please enter the recipe name. (or enter "cancel" to back to previous page.)\n'
                              '>>> ').lower().strip()
        found_recipe = None

        if validation_empty_entries(recipe_choose):
            if recipe_choose.replace(" ", '').isalpha():
                if recipe_choose == 'cancel':
                    return False
                else:
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

    print('\nHere are the details for your chosen recipe:\n')
    for values in recipe_list.values():
        if values['recipe_name'].lower() == recipe_choose:
            print(f'{"Recipe Category":<20}: {values["recipe_category"]}')
            print(f'{"Recipe Name":<20}: {values["recipe_name"]}')
            print(f'\n{"Ingredient Used"}:')
            ingredient_index = 1
            max_length = 0
            for item in values['ingredient_used']:
                if len(item[0]) > max_length:
                    max_length = len(item[0])

                max_length_unit = 0
                for items in values['ingredient_used']:
                    if len(str(items[1])) > max_length_unit:
                        max_length_unit = len(str(items[1]))

                print(
                    f'{ingredient_index}. {item[0].ljust(max_length + 2).title()}x  {str(item[1]).ljust(max_length_unit + 1)} {item[2]}')
                ingredient_index += 1
            print(f'{"Ingredient Notes":<20}: {values["ingredient_notes"]}')
            print(f'\n{"Equipment Used"}:')
            equipment_index = 1
            for item in values['equipment_used']:
                print(f'{equipment_index}. {item.title()}')
                equipment_index += 1
            print(f'{"Baking Temperature (°C)":<25}: {values["baking_temperature"]}')
            print(f'{"Baking Time (min)":<25}: {values["baking_time"]}')
            print(f'\n{"Instructions"}:')
            instruction_index = 1
            for instruction in values['instructions']:
                print(f'{instruction_index}. {instruction.title()}')
                instruction_index += 1
            print('')

    while True:
        try:
            quantity = int(input('Please enter the quantity you want to produce: '))

            print('\nChecking the availability of required ingredient......')

            selected_recipe = recipe_list[recipe_choose]
            selected_category = recipe_list[recipe_choose]['recipe_category']
            print(selected_category)

            availability = True
            max_possible_quantity = float('inf')
            unavailable_ingredients = []

            for item in selected_recipe['ingredient_used']:
                ingredient_name = item[0]
                quantity_needed = float(quantity) * item[1]
                unit_measurement = item[2].lower()
                print(unit_measurement)
                print(quantity_needed)

                current_quantity = None

                for key, items in ingredient_list.items():
                    if items['ingredient_name'].lower() == ingredient_name.lower():
                        if items['unit_measurement'] == unit_measurement:
                            current_quantity = items['quantity_purchased']
                            print(current_quantity)
                            break
                        elif ((items['unit_measurement'] == 'kg' and unit_measurement == 'g') or
                              (items['unit_measurement'] == 'l' and unit_measurement == 'ml') or
                              (items['unit_measurement'] == 'l' and unit_measurement == 'g') or
                              (items['unit_measurement'] == 'kg' and unit_measurement == 'ml')):
                            current_quantity = items['quantity_purchased'] * 1000
                            print(current_quantity)
                            break
                        elif ((items['unit_measurement'] == 'g' and unit_measurement == 'kg') or
                              (items['unit_measurement'] == 'ml' and unit_measurement == 'l') or
                              (items['unit_measurement'] == 'ml' and unit_measurement == 'kg') or
                              (items['unit_measurement'] == 'g' and unit_measurement == 'l')):
                            current_quantity = items['quantity_purchased'] / 1000
                            print(current_quantity)
                            break

                if current_quantity is not None:
                    if quantity_needed <= current_quantity:
                        pass
                    else:
                        unavailable_ingredients.append(item[0])
                        possible_quantity = current_quantity / item[1]
                        if possible_quantity < max_possible_quantity:
                            max_possible_quantity = possible_quantity
                        availability = False
                else:
                    print('\n+--------------------------------------------------+')
                    print(f'|⚠️ {ingredient_name} not found in the inventory. |')
                    print('+--------------------------------------------------+')
                    recipe_lists()
                    break

            if availability:
                while True:
                    production_confirmation = (input(f'Are you sure you want to produce {quantity} units of '
                                                     f'{selected_recipe["recipe_name"]}? Enter y for yes or n for no: '))
                    if validation_empty_entries(production_confirmation):
                        if production_confirmation == 'y':
                            for item in selected_recipe['ingredient_used']:
                                ingredient_name = item[0]
                                quantity_needed = float(quantity) * item[1]
                                unit_measurement = item[2].lower()

                                for key, items in ingredient_list.items():
                                    if items['ingredient_name'].lower() == ingredient_name.lower():
                                        selected_ingredient = key
                                        if items['unit_measurement'] == unit_measurement:
                                            remain_ingredient = items['quantity_purchased'] - quantity_needed
                                            ingredient_list[selected_ingredient][
                                                'quantity_purchased'] = remain_ingredient
                                            save_info_inventory_ingredient(ingredient_list)
                                            break
                                        elif ((items['unit_measurement'] == 'kg' and unit_measurement == 'g') or
                                              (items['unit_measurement'] == 'l' and unit_measurement == 'ml') or
                                              (items['unit_measurement'] == 'l' and unit_measurement == 'g') or
                                              (items['unit_measurement'] == 'kg' and unit_measurement == 'ml')):
                                            remain_ingredient = items['quantity_purchased'] - (quantity_needed / 1000)
                                            ingredient_list[selected_ingredient][
                                                'quantity_purchased'] = remain_ingredient
                                            save_info_inventory_ingredient(ingredient_list)
                                            break
                                        elif ((items['unit_measurement'] == 'g' and unit_measurement == 'kg') or
                                              (items['unit_measurement'] == 'ml' and unit_measurement == 'l') or
                                              (items['unit_measurement'] == 'ml' and unit_measurement == 'kg') or
                                              (items['unit_measurement'] == 'g' and unit_measurement == 'l')):
                                            remain_ingredient = items['quantity_purchased'] - (quantity_needed * 1000)
                                            ingredient_list[selected_ingredient][
                                                'quantity_purchased'] = remain_ingredient
                                            save_info_inventory_ingredient(ingredient_list)
                                            break

                            product_list[report_num] = {
                                'recipe_category': selected_category,
                                'recipe_name': recipe_choose,
                                'production_quantity': quantity,
                                'date_of_production': 'date'
                            }
                            save_info_inventory_check(product_list)
                            print('\nSuccessfully added!')
                            break

                        elif production_confirmation == 'n':
                            print('\nProduction cancelled.')
                            break
                        else:
                            print('\n+-------------------------------------------+')
                            print('|⚠️ Invalid input. Please enter "y" or "n". |')
                            print('+-------------------------------------------+')

                while True:
                    produce_more = input('\nContinue working on another recipe? (y=yes, n=no)'
                                         '\n>>> ')
                    if validation_empty_entries(produce_more):
                        if produce_more == 'y':
                            recipe_lists()
                            break
                        elif produce_more == 'n':
                            print('\nStop adding. Exiting to Recipe Management page......')
                            pass
                            break
                        else:
                            print('\n+-------------------------------------------+')
                            print('|⚠️ Invalid input. Please enter "y" or "n". |')
                            print('+-------------------------------------------+')

            else:
                print(f'Not enough {", ".join(unavailable_ingredients)} in stock. You can produce a maximum of '
                      f'{max_possible_quantity} units of {selected_recipe["recipe_name"]}.')

        except ValueError:
            print('\nPlease enter a whole number.')


#recipe_lists()
