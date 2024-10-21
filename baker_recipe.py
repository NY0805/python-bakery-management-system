import json


# Define the function that loads data from the file
def load_data_from_recipe():
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


def load_data_from_equipment():
    try:
        file = open('baker_equipment.txt', 'r')  # open the file and read
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


def save_info(recipe):
    file = open('baker_recipe.txt', 'w')  # open the file to write
    json.dump(recipe, file,
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


def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


def format_ingredient_data(product):
    return (
        f"{product['ingredient_name'].title()}"
    )


def format_equipment_data(product):
    return (
        f"{product['equipment_name'].title()}"
    )


recipe_data = load_data_from_recipe()

equipment_list = load_data_from_equipment()

equipment_category_groups = {}
for value in equipment_list.values():
    equipment_category = value['category']

    if equipment_category not in equipment_category_groups:
        equipment_category_groups[equipment_category] = []

    equipment_category_groups[equipment_category].append(format_equipment_data(value))

ingredient_list = load_data_from_inventory_ingredient()

ingredient_category_groups = {}
for value in ingredient_list.values():
    ingredient_category = value['category']

    if ingredient_category not in ingredient_category_groups:
        ingredient_category_groups[ingredient_category] = []

    ingredient_category_groups[ingredient_category].append(format_ingredient_data(value))


def recipe_management():
    printed_centered('PRODUCT MANAGEMENT')
    print('\n1. Add Recipe')
    print('2. Update Recipe')
    print('3. Remove Recipe')
    print('4. Back to Previous Page')

    while True:
        option_recipe_management = input('\nPlease choose a service by entering its index number:'
                                         '\n>>> ')
        if validation_empty_entries(option_recipe_management):
            if option_recipe_management not in ['1', '2', '3', '4']:
                print('\n+--------------------------------------+')
                print('|⚠️ Please enter a valid index number. |')
                print('+--------------------------------------+')
            else:
                if option_recipe_management == '1':
                    recipe_instruction()
                    break
                elif option_recipe_management == '2':
                    update_recipe()
                    break
                elif option_recipe_management == '3':
                    delete_recipe()
                    break
                elif option_recipe_management == '4':
                    print('\nExiting to the previous page......')
                    break


def create_recipe():
    recipe_info = ['Recipe Name', 'Recipe\'s Category', 'Recipe Code', 'Ingredient Name', 'Ingredient_Per_Unit',
                   'Variation', 'Notes']

    max_length = 0
    for item in recipe_info:
        if len(item) > max_length:
            max_length = len(item)

    while True:
        print('\n💡 Categories: Breads, Cakes, Pastries, Biscuits, Muffins, Others 💡')
        category = input(f'1. {recipe_info[1].ljust(max_length + 2)}: ')
        if validation_empty_entries(category):
            if category.strip().isalpha():
                if category in ['Breads', 'Cakes', 'Pastries', 'Biscuits', 'Muffins', 'Others']:
                    break
                else:
                    print('\n+----------------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid category based on the categories given. (Case sensitive.) |')
                    print('+----------------------------------------------------------------------------------+')
            else:
                print(
                    '\n+-----------------------------------------------------------------------------------------------+')
                print(
                    '|⚠️ Please enter a valid category. (Cannot contain any spacing, digits and special characters.) |')
                print(
                    '+-----------------------------------------------------------------------------------------------+')

    while True:
        recipe_name = input(f'2. {recipe_info[0].ljust(max_length + 2)}: ').strip()
        if validation_empty_entries(recipe_name):
            if recipe_name.replace(" ", '').isalpha():
                if recipe_name not in recipe_data.keys():
                    break
                else:
                    print(
                        '\n+-------------------------------------+')
                    print('|⚠️ Duplicate recipe name detected. |')
                    print('+-----------------------------------+\n')
            else:
                print('\n+-----------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid recipe name. (Cannot contain any digits and special characters.) |')
                print('+-----------------------------------------------------------------------------------------+\n')

    return category, recipe_name


def is_ingredient_duplicate(ingredient_name, ingredients):
    for i in ingredients:
        if ingredient_name.lower() == i[0].lower():
            return False
    return True


def recipe_ingredient(adding_ingredient, update_ingredient):
    ingredients = []
    add_notes = True
    ingredient_notes = None
    while add_notes:
        while True:
            printed_centered('INGREDIENT LIST')
            for category, items in ingredient_category_groups.items():
                index = 1
                print(f'📍 {category} 📍')
                for ingredient in items:
                    print(f"{index}. {ingredient.title()}")
                    index += 1
                print('')

            ingredient_name = input(f'✏️ Enter the ingredient name: ').strip()
            found_category = None

            if validation_empty_entries(ingredient_name):
                if ingredient_name.replace(" ", '').isalpha():
                    if is_ingredient_duplicate(ingredient_name, ingredients):
                        for category, items in ingredient_category_groups.items():
                            for item in items:
                                if ingredient_name.lower() == item.lower():
                                    found_category = category
                                    break
                            if found_category:
                                break
                        else:
                            print(
                                '\n+---------------------------------------------------------------------------------------------+')
                            print(
                                '|⚠️ Invalid ingredient name. Please enter ingredient name based on the ingredient list given. |')
                            print(
                                '+---------------------------------------------------------------------------------------------+')
                    else:
                        print('\n+---------------------------------------------------------------------+')
                        print('|⚠️ Duplicate ingredient name. You\'ve already added this ingredient. |')
                        print('+---------------------------------------------------------------------+')
                    if found_category:
                        break
                else:
                    print(
                        '\n+---------------------------------------------------------------------------------------------+')
                    print(
                        '|⚠️ Please enter a valid ingredient name. (Cannot contain any digits and special characters.) |')
                    print(
                        '+---------------------------------------------------------------------------------------------+')

        while True:
            category_units = {
                'Flours and Grains': 'g, kg',
                'Sweeteners': 'g, ml',
                'Fats and Oils': 'g, ml',
                'Dairy and Non-Dairy Products': 'g, kg, l, ml',
                'Leavening Agents': 'g',
                'Spices and Flavourings': 'g',
                'Fillings and Toppings': 'g',
                'Fruits and Vegetables': 'g, kg',
                'Preservatives and Stabilizers': 'g'
            }

            unit = category_units.get(found_category, '')

            print(f'\n💡 Allowable unit measurement: {unit}')
            unit_measurement = input(f'✏️ Enter the unit measurement of {ingredient_name}: ').lower().strip()

            allowable_unit = []
            for item in unit.split(','):
                allowable_unit.append(item.strip().lower())

            if validation_empty_entries(unit_measurement):
                if unit_measurement.isalpha():
                    if unit_measurement in allowable_unit:
                        break
                    else:
                        print('\n+-------------------------------------------------+')
                        print('|⚠️ Please enter a valid unit from the unit given.|')
                        print('+-------------------------------------------------+')
                else:
                    print(
                        '\n+--------------------------------------------------------------------------------------------+')
                    print(
                        '|⚠️ Please enter a valid unit. (Cannot contain any spacings, digits and special characters.) |')
                    print(
                        '+--------------------------------------------------------------------------------------------+')

        while True:
            quantity_per_unit = input(f'\n✏️ Enter the quantity per unit of {ingredient_name}: ').strip()
            if validation_empty_entries(quantity_per_unit):
                try:
                    quantity_per_unit = float(quantity_per_unit)
                    if quantity_per_unit > 0:
                        break
                    else:
                        print('\n+---------------------------------------------------+')
                        print('|⚠️ Please enter a valid quantity. (Greater than 0) |')
                        print('+---------------------------------------------------+')

                except ValueError:
                    print(
                        '\n+-----------------------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid quantity. (Cannot contain any alphabets and special characters.) |')
                    print(
                        '+-----------------------------------------------------------------------------------------+')

        ingredient_used = [ingredient_name.lower(), quantity_per_unit, unit_measurement]
        ingredients.append(ingredient_used)

        print('\nIngredient so far:')

        ingredient_index = 1
        max_length = 0
        for item in ingredients:
            if len(item[0]) > max_length:
                max_length = len(item[0])

            max_length_unit = 0
            for items in ingredients:
                if len(str(items[1])) > max_length_unit:
                    max_length_unit = len(str(items[1]))

            print(
                f'{ingredient_index}. {item[0].ljust(max_length + 2).title()}x  {str(item[1]).ljust(max_length_unit + 1)} {item[2]}')
            ingredient_index += 1

        if adding_ingredient:
            while True:
                add_more = input('\nContinue adding ingredients? (y=yes, n=no)'
                                 '\n>>> ').lower().strip()
                if add_more == 'y':
                    break
                elif add_more == 'n':
                    if update_ingredient:
                        while True:
                            ingredient_notes = input(
                                "\nAny additional details or notes you'd like to include for these ingredients? If not, enter 'no'.\n>>> ")
                            if validation_empty_entries(ingredient_notes):
                                if ingredient_notes.lower() == 'no':
                                    print('\nStop adding. Proceeding to select the necessary equipment 😊')
                                    add_notes = False
                                    break
                                else:
                                    print(f'\nNote added: {ingredient_notes}')
                                    print('\nStop adding. Proceeding to select the necessary equipment 😊')
                                    add_notes = False
                                    break
                    add_notes = False
                    break
                else:
                    print('\n+-------------------------------------------+')
                    print('|⚠️ Invalid input. Please enter "y" or "n". |')
                    print('+-------------------------------------------+')
                if not add_notes:
                    break
        add_notes = False
        break

    return ingredients, ingredient_notes


def is_equipment_duplicate(equipment_name, equipments):
    for i in equipments:
        if equipment_name.lower() == i.lower():
            return False
    return True


def recipe_equipment(update_equipment):
    equipments = []
    printed_centered('EQUIPMENT LIST')
    for category, items in equipment_category_groups.items():
        index = 1
        print(f'📍 {category} 📍')
        for equipment in items:
            print(f"{index}. {equipment.title()}")
            index += 1
        print('')
    print('💡 Please enter the name of selected equipment (or type "done" to finish)')

    if update_equipment:
        while True:
            equipment_name = input(f'\n✏️ Enter the name of selected equipment {len(equipments) + 1}: ').lower().strip()

            if equipment_name == 'done':
                if len(equipments) == 0:
                    print('\n+-----------------------------------------------------------+')
                    print('|⚠️ You must enter at least one equipment before finishing. |')
                    print('+-----------------------------------------------------------+')
                    continue
                else:
                    print('\nStop adding. Continue to Recipe Instruction page......')
                    break

            if validation_empty_entries(equipment_name):
                if equipment_name.replace(" ", "").isalpha():
                    if is_equipment_duplicate(equipment_name, equipments):
                        found_category = None
                        for category, items in equipment_category_groups.items():
                            for item in items:
                                if equipment_name.lower() == item.lower():
                                    found_category = True
                                    break
                            if found_category:
                                break
                        else:
                            print(
                                '\n+------------------------------------------------------------------------------------------+')
                            print(
                                '|⚠️ Invalid equipment name. Please enter equipment name based on the equipment list given. |')
                            print(
                                '+------------------------------------------------------------------------------------------+')
                            continue

                        equipments.append(equipment_name)
                    else:
                        print('\n+-------------------------------------------------------------------+')
                        print('|⚠️ Duplicate equipment name. You\'ve already added this equipment. |')
                        print('+-------------------------------------------------------------------+')
                else:
                    print(
                        '\n+--------------------------------------------------------------------------------------------+')
                    print(
                        '|⚠️ Please enter a valid equipment name. (Cannot contain any digits and special characters.) |')
                    print(
                        '+--------------------------------------------------------------------------------------------+')

    else:
        while True:
            equipment_name = input(
                f'\n✏️ Enter the name of selected equipment {len(equipments) + 1}: ').lower().strip()

            if validation_empty_entries(equipment_name):
                if equipment_name.replace(" ", "").isalpha():
                    if is_equipment_duplicate(equipment_name, equipments):
                        found_category = None
                        for category, items in equipment_category_groups.items():
                            for item in items:
                                if equipment_name.lower() == item.lower():
                                    found_category = True
                                    break
                            if found_category:
                                break
                        else:
                            print(
                                '\n+------------------------------------------------------------------------------------------+')
                            print(
                                '|⚠️ Invalid equipment name. Please enter equipment name based on the equipment list given. |')
                            print(
                                '+------------------------------------------------------------------------------------------+')
                            continue

                        equipments.append(equipment_name)
                    else:
                        print('\n+-------------------------------------------------------------------+')
                        print('|⚠️ Duplicate equipment name. You\'ve already added this equipment. |')
                        print('+-------------------------------------------------------------------+')
                        continue
                else:
                    print(
                        '\n+--------------------------------------------------------------------------------------------+')
                    print(
                        '|⚠️ Please enter a valid equipment name. (Cannot contain any digits and special characters.) |')
                    print(
                        '+--------------------------------------------------------------------------------------------+')
                    continue
            return equipments
    return equipments


def recipe_instruction():
    instructions = []

    category, recipe_name = create_recipe()
    ingredients, ingredient_notes = recipe_ingredient(adding_ingredient=True, update_ingredient=True)
    equipments = recipe_equipment(update_equipment=True)

    print('')
    print('-' * 140)
    print(
        "\nWelcome to the Recipe Instruction page! Let's get started with creating your delicious bakery goods step by step.\n")
    print("🥗 Selected ingredients 🥗")
    max_length = 0
    index = 1
    for item in ingredients:
        if len(item) > max_length:
            max_length = len(item)

        print(f'{index}. {item[0].ljust(max_length).title()} x {item[1]} {item[2]}')
        index += 1

    print("\n🛠️ Selected equipments 🛠️")
    index = 1
    for item in equipments:
        print(f'{index}. {item.title()}')
        index += 1

        if index == len(item):
            print('')

    while True:
        try:
            baking_temperature = int(input('\nPlease provide the baking temperature (°C): '))
            if validation_empty_entries(baking_temperature):
                if 0 < baking_temperature <= 300:
                    break
                else:
                    print('\n+----------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid temperature. (Greater than 0°C, smaller than 301°C) |')
                    print('+----------------------------------------------------------------------------+')
        except ValueError:
            print('\n+---------------------------------------------------------------+')
            print('|⚠️ Invalid input. Please enter a whole number for temperature. |')
            print('+---------------------------------------------------------------+')

    while True:
        try:
            baking_time = int(input('\nPlease provide the baking time (in minutes): '))
            if validation_empty_entries(baking_time):
                if 0 < baking_time <= 90:
                    print('\n📝 Instructions (type "done" to finish)')
                    break
                else:
                    print('\n+-------------------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid duration. (Greater than 0 minutes, smaller than 91 minutes.) |')
                    print('+-------------------------------------------------------------------------------------+')
        except ValueError:
            print('\n+---------------------------------------------------------------+')
            print('|⚠️ Invalid input. Please enter whole numbers for the duration. |')
            print('+---------------------------------------------------------------+')

    while True:
        instruction = input(f'{len(instructions) + 1}. ').strip()

        if instruction == 'done':
            if len(instructions) == 0:
                print('\n+-------------------------------------------------------------+')
                print('|⚠️ You must enter at least one instruction before finishing. |')
                print('+-------------------------------------------------------------+')
                continue
            else:
                print(f'\nStop adding instructions... Recipe {recipe_name.title()} successfully saved!')
                break

        if validation_empty_entries(instruction):
            instructions.append(instruction)
            continue

    recipe_data[recipe_name] = {
        'recipe_category': category,
        'recipe_name': recipe_name,
        'ingredient_used': ingredients,
        'ingredient_notes': ingredient_notes,
        'equipment_used': equipments,
        'baking_temperature': baking_temperature,
        'baking_time': baking_time,
        'instructions': instructions
    }

    save_info(recipe_data)

    continue_adding_recipe()


def continue_adding_recipe():
    while True:
        add_more = input('\nContinue adding new recipe? (y=yes, n=no)'
                         '\n>>> ')
        if validation_empty_entries(add_more):
            if add_more == 'y':
                recipe_instruction()
                break
            elif add_more == 'n':
                print('\nStop adding. Exiting to Recipe Management page......')
                recipe_management()
                break
            else:
                print('\n+-------------------------------------------+')
                print('|⚠️ Invalid input. Please enter "y" or "n". |')
                print('+-------------------------------------------+')


def display_recipe(recipe):
    print(f'{'recipe_category':<20}: {recipe['recipe_category']}')
    print(f'{'recipe_name':<20}: {recipe['recipe_name']}')
    print(f'{'\ningredient_used'}:')
    ingredient_index = 1
    max_length = 0
    for item in recipe['ingredient_used']:
        if len(item[0]) > max_length:
            max_length = len(item[0])

        max_length_unit = 0
        for items in recipe['ingredient_used']:
            if len(str(items[1])) > max_length_unit:
                max_length_unit = len(str(items[1]))

        print(
            f'{ingredient_index}. {item[0].ljust(max_length + 2).title()}x  {str(item[1]).ljust(max_length_unit + 1)} {item[2]}')
        ingredient_index += 1
    print(f'{'ingredient_notes':<20}: {recipe['ingredient_notes']}')
    print(f'{'\nequipment_used'}:')
    equipment_index = 1
    for item in recipe['equipment_used']:
        print(f'{equipment_index}. {item.title()}')
        equipment_index += 1
    print(f'{'baking_temperature (°C)':<25}: {recipe['baking_temperature']}')
    print(f'{'baking_time (min)':<25}: {recipe['baking_time']}')
    print(f'{'\ninstructions'}:')
    instruction_index = 1
    for instruction in recipe['instructions']:
        print(f'{instruction_index}. {instruction.upper()}')
        instruction_index += 1


def update_recipe():
    while True:
        index = 1
        printed_centered('RECIPE LIST')
        for key, recipe in recipe_data.items():
            print(f'{index}. {recipe["recipe_name"].title()}')
            index += 1
        print(f'{len(recipe_data) + 1}. Cancel')

        try:
            index_of_product_to_edit = int(
                input(
                    f'\nEnter index number to update the information of the recipe (or enter {len(recipe_data) + 1} to cancel):\n>>> '))

            if index_of_product_to_edit == len(recipe_data) + 1:  # if "Cancel" is selected
                print('\nCancelling. Exiting to Product Management page......')  # return to the previous page
                recipe_management()
                break

            elif 1 <= index_of_product_to_edit <= len(recipe_data):
                for key, recipe in recipe_data.items():
                    selected_recipe_key = list(recipe_data.keys())[
                        index_of_product_to_edit - 1]  # indicate which recipe is selected

                    print('\n--------------------------------------------------')
                    print(f'\t\t\t\t {selected_recipe_key.upper()}\'S DATA')
                    print('--------------------------------------------------')

                    display_recipe(recipe_data[selected_recipe_key])
                    break
            else:
                print('\n❗Recipe not found.')  # error displayed if selected product not found
                continue

        except ValueError:
            print('\n+-----------------------------------------+')
            print('|⚠️ Invalid input. Please enter a number. |')
            print('+-----------------------------------------+')
            continue

        while True:
            selected_recipe_key = list(recipe_data.keys())[
                index_of_product_to_edit - 1]  # indicate which recipe is selected

            print('\nTo change the information, please enter the exact matching name. Example: product_name.')
            attribute_of_recipe_data = input('Which information do you want to update? (or enter \"cancel\")\n>>> ')

            if attribute_of_recipe_data == 'cancel':
                print('\nCancelling. Exiting to the Recipe List......')
                update_recipe()
                break

            elif attribute_of_recipe_data == 'ingredient_used':
                ingredient_index = 1
                max_length = 0
                print('')
                for item in recipe_data[selected_recipe_key]['ingredient_used']:
                    if len(item[0]) > max_length:
                        max_length = len(item[0])

                    max_length_unit = 0
                    for items in recipe_data[selected_recipe_key]['ingredient_used']:
                        if len(str(items[1])) > max_length_unit:
                            max_length_unit = len(str(items[1]))

                    print(
                        f'{ingredient_index}. {item[0].ljust(max_length + 2).title()}x  {str(item[1]).ljust(max_length_unit + 1)} {item[2]}')
                    ingredient_index += 1

                print('')
                edit_ingredient = input(
                    "Add, edit or delete ingredient? \nPlease enter 'add', 'edit' or 'delete' (or enter 'cancel' to stop): ")

                if edit_ingredient == 'add':
                    new_ingredient_list, notes = recipe_ingredient(adding_ingredient=True, update_ingredient=False)
                    if new_ingredient_list:
                        recipe_data[selected_recipe_key]['ingredient_used'].extend(new_ingredient_list)
                        save_info(recipe_data)
                        print('\nInformation saved.')
                        break
                    else:
                        print('\nNo new ingredient added.')
                        break

                elif edit_ingredient == 'edit':
                    while True:
                        try:
                            edit_ingredient = input(
                                "\nPlease enter the index number of ingredient you want to edit (or enter 'cancel')\n>>> ")

                            if not validation_empty_entries(edit_ingredient):
                                continue

                            if edit_ingredient == 'cancel':
                                break

                            edit_ingredient = int(edit_ingredient)

                            if 1 <= edit_ingredient <= len(recipe_data[selected_recipe_key]['ingredient_used']):
                                new_ingredients, notes = recipe_ingredient(adding_ingredient=False,
                                                                           update_ingredient=False)
                                if new_ingredients:
                                    recipe_data[selected_recipe_key]['ingredient_used'][edit_ingredient - 1] = \
                                    new_ingredients[0]
                                    save_info(recipe_data)
                                    print('\nInformation saved.')
                                    break
                                else:
                                    print('\nNo new ingredient added.')
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

                elif edit_ingredient == 'delete':
                    while True:
                        try:
                            delete_ingredient = input(
                                "\nPlease enter the index number of ingredient you want to delete (or enter 'cancel')\n>>> ").lower().strip()
                            if not validation_empty_entries(delete_ingredient):
                                continue

                            if delete_ingredient == 'cancel':
                                break

                            delete_ingredient = int(delete_ingredient)

                            if 1 <= delete_ingredient <= len(recipe_data[selected_recipe_key]['ingredient_used']):
                                del recipe_data[selected_recipe_key]['ingredient_used'][delete_ingredient - 1]
                                save_info(recipe_data)
                                print('\nIngredient deleted.')
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
                elif edit_ingredient == 'cancel':
                    break

                else:
                    print('\n+-----------------------------------------------------+')
                    print('|⚠️ Please enter "add", "edit", "delete" or "cancel". |')
                    print('+-----------------------------------------------------+')
                    continue

            elif attribute_of_recipe_data == 'equipment_used':
                equipment_index = 1
                print('')
                for item in recipe_data[selected_recipe_key]['equipment_used']:
                    print(f'{equipment_index}. {item.title()}')
                    equipment_index += 1
                print('')

                edit_equipment = input(
                    "Add, edit or delete ingredient? \nPlease enter 'add', 'edit' or 'delete' (or enter 'cancel' to stop): ")

                if edit_equipment == 'add':
                    new_equipment = recipe_equipment(update_equipment=True)
                    if new_equipment:
                        recipe_data[selected_recipe_key]['equipment_used'].extend(new_equipment)
                        save_info(recipe_data)
                        print('\nInformation saved.')
                        break
                    else:
                        print('\nNo new equipment added.')
                        break

                elif edit_equipment == 'edit':
                    while True:
                        try:
                            new_edit_equipment = input(
                                "\nPlease enter the index number of ingredient you want to edit (or enter 'cancel')\n>>> ")

                            if not validation_empty_entries(new_edit_equipment):
                                continue

                            if new_edit_equipment == 'cancel':
                                break

                            new_edit_equipment = int(new_edit_equipment)

                            if 1 <= new_edit_equipment <= len(recipe_data[selected_recipe_key]['equipment_used']):
                                new_equipment = recipe_equipment(update_equipment=False)

                                if new_equipment:
                                    recipe_data[selected_recipe_key]['equipment_used'][new_edit_equipment - 1] = \
                                        new_equipment[0]
                                    save_info(recipe_data)
                                    print('\nInformation saved.')
                                    break
                                else:
                                    print('\nNo new equipment added.')
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

                elif edit_equipment == 'delete':
                    while True:
                        try:
                            delete_equipment = input(
                                "\nPlease enter the index number of ingredient you want to delete (or enter 'cancel')\n>>> ").lower().strip()
                            if not validation_empty_entries(delete_equipment):
                                continue

                            if delete_equipment == 'cancel':
                                break

                            delete_equipment = int(delete_equipment)

                            if 1 <= delete_equipment <= len(recipe_data[selected_recipe_key]['equipment_used']):
                                del recipe_data[selected_recipe_key]['equipment_used'][delete_equipment - 1]
                                save_info(recipe_data)
                                print('\nEquipment deleted.')
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
                elif edit_equipment == 'cancel':
                    break

                else:
                    print('\n+-----------------------------------------------------+')
                    print('|⚠️ Please enter "add", "edit", "delete" or "cancel". |')
                    print('+-----------------------------------------------------+')
                    continue

            elif attribute_of_recipe_data == 'instructions':
                instructions = []

                instruction_index = 1
                for instruction in recipe_data[selected_recipe_key]['instructions']:
                    print(f'{instruction_index}. {instruction.title()}')
                    instruction_index += 1
                print('')

                print('Enter new instruction. (type "done" to finish updating, "cancel" to exit to previous page.)')

                while True:
                    instruction = input(f'{len(instructions) + 1}. ').strip()

                    if instruction == 'done':
                        if len(instructions) == 0:
                            print('\n+-----------------------------------------------------------+')
                            print('|⚠️ You must enter at least one equipment before finishing. |')
                            print('+-----------------------------------------------------------+')
                            continue
                        else:
                            recipe_data[selected_recipe_key]['instructions'] = instructions
                            save_info(recipe_data)
                            print(f'\nInformation saved.')
                            break

                    if instruction == 'cancel':
                        break

                    if validation_empty_entries(instruction):
                        instructions.append(instruction)
                        continue

            elif attribute_of_recipe_data in recipe:
                while True:
                    new_value = input(f'\nEnter new {attribute_of_recipe_data}: ')

                    if not validation_empty_entries(new_value):
                        continue
                    else:
                        if attribute_of_recipe_data == 'recipe_category':
                            print('💡 Categories: Breads, Cakes, Pastries, Biscuits, Muffins, Others 💡')
                            if not new_value.strip().isalpha():
                                if new_value not in ['Breads', 'Cakes', 'Pastries', 'Biscuits', 'Muffins', 'Others']:
                                    print(
                                        '\n+----------------------------------------------------------------------------------+')
                                    print(
                                        '|⚠️ Please enter a valid category based on the categories given. (Case sensitive.) |')
                                    print(
                                        '+----------------------------------------------------------------------------------+\n')
                                    continue
                            else:
                                print(
                                    '\n+-----------------------------------------------------------------------------------------------+')
                                print(
                                    '|⚠️ Please enter a valid category. (Cannot contain any spacing, digits and special characters.) |')
                                print(
                                    '+-----------------------------------------------------------------------------------------------+\n')
                                continue

                        elif attribute_of_recipe_data == 'recipe_name':
                            if not new_value.replace(" ", '').isalpha():
                                if new_value in recipe_data.keys():
                                    print('\n+-------------------------------------+')
                                    print('|⚠️ Duplicate recipe name detected. |')
                                    print('+-----------------------------------+')
                                    continue
                            else:
                                print(
                                    '\n+-----------------------------------------------------------------------------------------+')
                                print(
                                    '|⚠️ Please enter a valid recipe name. (Cannot contain any digits and special characters.) |')
                                print(
                                    '+-----------------------------------------------------------------------------------------+\n')
                                continue

                        elif attribute_of_recipe_data == 'ingredient_notes':
                            if not validation_empty_entries(new_value):
                                continue

                        elif attribute_of_recipe_data == 'baking_temperature':
                            try:
                                new_value = int(new_value)
                                if not 0 < new_value <= 300:
                                    print(
                                        '\n+----------------------------------------------------------------------------+')
                                    print(
                                        '|⚠️ Please enter a valid temperature. (Greater than 0°C, smaller than 301°C) |')
                                    print(
                                        '+----------------------------------------------------------------------------+')
                                    continue
                            except ValueError:
                                print('\n+---------------------------------------------------------------+')
                                print('|⚠️ Invalid input. Please enter a whole number for temperature. |')
                                print('+---------------------------------------------------------------+')
                                continue

                        elif attribute_of_recipe_data == 'baking_time':
                            try:
                                new_value = int(new_value)
                                if not 0 < new_value <= 90:
                                    print(
                                        '\n+-------------------------------------------------------------------------------------+')
                                    print(
                                        '|⚠️ Please enter a valid duration. (Greater than 0 minutes, smaller than 91 minutes.) |')
                                    print(
                                        '+-------------------------------------------------------------------------------------+')
                                    continue
                            except ValueError:
                                print('\n+---------------------------------------------------------------+')
                                print('|⚠️ Invalid input. Please enter whole numbers for the duration. |')
                                print('+---------------------------------------------------------------+')
                                continue

                        print(
                            f'\n{attribute_of_recipe_data} of {selected_recipe_key} is updated.')  # inform user about the data is updated
                        recipe_data[selected_recipe_key].update(
                            {attribute_of_recipe_data: new_value})  # assign the new value entered to the attributes
                        save_info(recipe_data)  # save the data
                        break
            else:
                print('\n❗Data not found.')  # error displayed if attribute entered not found


def delete_recipe():
    while True:
        index = 1
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'RECIPE LIST')
        print('-----------------------------------------------')
        for name, info in recipe_data.items():
            print(f'{index}. {name.title()}')
            index += 1
        print(f'{len(recipe_data) + 1}. cancel')

        try:
            index_remove_recipe = int(
                input(f'\nWhich recipe do you want to remove? (or enter {len(recipe_data) + 1} to cancel)\n>>> '))
            if index_remove_recipe == len(recipe_data) + 1:  # cancel the process
                print('\nCancelling. Exiting to Services page......')
                recipe_management()
                break

            elif 1 <= index_remove_recipe <= len(recipe_data):
                recipe_to_remove = list(recipe_data.keys())[
                    index_remove_recipe - 1]  # identify baker to remove by accesing the index of key of baker
                del recipe_data[recipe_to_remove]  # delete the selected baker
                save_info(recipe_data)
                print(
                    f'\n{recipe_to_remove.title()} is removed.\n')  # inform user that the selected baker is removed successfully

                while True:
                    remove_more = input(
                        'Continue to remove? (y=yes, n=no)\n>>> ')  # ask user if they want to continue removing
                    if remove_more == 'y':
                        break
                    elif remove_more == 'n':
                        print('\nStop removing. Exiting to Services page......')
                        recipe_management()
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


#update_recipe()
recipe_management()
