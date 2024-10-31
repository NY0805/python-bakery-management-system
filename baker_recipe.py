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


# Define the function that save recipe data to the file
def save_info(recipe):
    file = open('baker_recipe.txt', 'w')  # open the file to write
    json.dump(recipe, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# function that validate empty entries
def validation_empty_entries(info):
    if info:
        return True
    else:
        print('\n❗Please enter something...\n')
        return False


# validate input that store a list is alphabet only
def validation_list_alphabet_only(info):
    for item in info:
        if item.replace(" ", "").isalpha():
            return True
        else:
            return False


# print the title at the center for design purpose
def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


# format the data get from different file
def format_ingredient_data(product):
    return (
        f"{product['ingredient_name'].title()}"
    )


def format_equipment_data(product):
    return (
        f"{product['equipment_name'].title()}"
    )


# load recipe data from baker recipe file
recipe_data = load_data_from_recipe()

# load equipment data from baker equipment file
equipment_list = load_data_from_equipment()

equipment_category_groups = {}  # initialize an empty dictionary to group equipment items by category
for value in equipment_list.values():  # loop through equipment data and get the category for current equipment
    equipment_category = value['category']

    if equipment_category not in equipment_category_groups:  # if the category does not exist as a key in the dictionary
        equipment_category_groups[equipment_category] = []  # create a new empty list with the category as the key

    # if the category already exist as a key, append the current equipment details
    equipment_category_groups[equipment_category].append(format_equipment_data(value))


# load ingredient data from inventory ingredient file
ingredient_list = load_data_from_inventory_ingredient()

# group the ingredients based on its category, similar as grouping the equipment items
ingredient_category_groups = {}
for value in ingredient_list.values():
    ingredient_category = value['category']

    if ingredient_category not in ingredient_category_groups:
        ingredient_category_groups[ingredient_category] = []

    ingredient_category_groups[ingredient_category].append(format_ingredient_data(value))


# define function that let user to select recipe management service
def recipe_management():
    printed_centered('RECIPE MANAGEMENT')
    print('\n1. Add Recipe')
    print('2. Update Recipe')
    print('3. Remove Recipe')
    print('4. Back to Previous Page')

    # loop until a valid choice is selected or user choose to exit
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


# define function that let user enter recipe category and recipe name
def create_recipe():
    recipe_info = ['Recipe Name', 'Recipe\'s Category']  # list of required information for the recipe

    # calculate the maximum length of items in recipe_info for formatting purpose
    max_length = 0
    for item in recipe_info:
        if len(item) > max_length:
            max_length = len(item)

    # prompt user to enter recipe category and ensure the input fall within given categories
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

    # prompt user to enter recipe name and ensure it is unique in baker recipe file
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

    return category, recipe_name  # return the category and recipe name


# define the function that check whether user input ingredient is duplicate
def is_ingredient_duplicate(ingredient_name, ingredients):
    for i in ingredients:
        if ingredient_name.lower() == i[0].lower():
            return False
    return True


# define the function that let user add ingredient for recipe
def recipe_ingredient(adding_ingredient, update_ingredient):
    ingredients = []  # initialize an empty list to store selected ingredients
    add_notes = True  # create a flag to help in exit loop
    ingredient_notes = None  # initialize ingredient_notes to None

    while add_notes:
        # loop until valid ingredient name is selected
        while True:
            printed_centered('INGREDIENT LIST')
            for category, items in ingredient_category_groups.items():
                index = 1
                print(f'📍 {category} 📍')
                for ingredient in items:
                    print(f"{index}. {ingredient.title()}")  # print the index and ingredient name
                    index += 1
                print('')

            # prompt user to select an ingredient
            ingredient_name = input(f'✏️ Enter the ingredient name: ').strip()
            found_category = None

            # ensure the input ingredient is existed in the list given
            if validation_empty_entries(ingredient_name):
                if ingredient_name.replace(" ", '').isalpha():
                    if is_ingredient_duplicate(ingredient_name, ingredients):  # ensure the entered ingredient does not duplicate
                        for category, items in ingredient_category_groups.items():
                            for item in items:
                                if ingredient_name.lower() == item.lower():
                                    found_category = category  # track the category of selected ingredient
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

        # prompt user to enter valid unit measurement based on corresponding category limit
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

            unit = category_units.get(found_category, '')  # track the valid unit measurement of selected ingredient

            print(f'\n💡 Allowable unit measurement: {unit}')

            # collect user input unit measurement
            unit_measurement = input(f'✏️ Enter the unit measurement of {ingredient_name}: ').lower().strip()

            allowable_unit = []
            for item in unit.split(','):
                allowable_unit.append(item.strip().lower())  # store the allowable unit in a list for comparison

            if validation_empty_entries(unit_measurement):
                if unit_measurement.isalpha():
                    if unit_measurement in allowable_unit:  # if input includes in the allowable unit, exit the loop
                        break
                    else:  # if not, prompt user to enter again
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

        # prompt user to enter the quantity of ingredient needed per unit
        while True:
            quantity_per_unit = input(f'\n✏️ Enter the quantity per unit of {ingredient_name}: ').strip()
            if validation_empty_entries(quantity_per_unit):
                try:
                    quantity_per_unit = float(quantity_per_unit)
                    if quantity_per_unit > 0:  # ensure the quantity is digit and greater than 0
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

        # store the ingredient name, quantity and unit measurement selected in the empty list
        ingredient_used = [ingredient_name.lower(), quantity_per_unit, unit_measurement]
        ingredients.append(ingredient_used)

        # print current ingredient stored in the list
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

        # prompt user whether to add another ingredient
        if adding_ingredient:
            while True:
                add_more = input('\nContinue adding ingredients? (y=yes, n=no)'
                                 '\n>>> ').lower().strip()
                if add_more == 'y':  # if user choose to add another ingredient
                    add_notes = True  # ensure add_notes is True so that the code will continue looping from the start after breaking this loop
                    break
                elif add_more == 'n':  # if user choose to not add
                    if update_ingredient:
                        # prompt user to enter ingredient notes
                        while True:
                            ingredient_notes = input(
                                "\nAny additional details or notes you'd like to include for these ingredients? If not, enter 'no'.\n>>> ")
                            if validation_empty_entries(ingredient_notes):
                                if ingredient_notes.lower() == 'no':
                                    print('\nStop adding. Proceeding to select the necessary equipment 😊')
                                    add_notes = False  # change the flag to False to exit the loop
                                    break
                                else:
                                    print(f'\nNote added: {ingredient_notes}')
                                    print('\nStop adding. Proceeding to select the necessary equipment 😊')
                                    add_notes = False  # change the flag to False to exit the loop
                                    break
                    else:
                        add_notes = False
                    break
                else:
                    print('\n+-------------------------------------------+')
                    print('|⚠️ Invalid input. Please enter "y" or "n". |')
                    print('+-------------------------------------------+')
        else:
            break
        if not add_notes:
            break

    return ingredients, ingredient_notes


# define the function that check whether user input equipment is duplicate
def is_equipment_duplicate(equipment_name, equipments):
    for i in equipments:
        if equipment_name.lower() == i.lower():
            return False
    return True


# define the function that let user add equipment for recipe
def recipe_equipment(update_equipment):
    equipments = []  # initialize an empty list to store selected equipment
    printed_centered('EQUIPMENT LIST')
    for category, items in equipment_category_groups.items():
        index = 1
        print(f'📍 {category} 📍')
        for equipment in items:
            print(f"{index}. {equipment.title()}")  # print the index with equipment name
            index += 1
        print('')
    print('💡 Please enter the name of selected equipment (or type "done" to finish)')

    # if update_equipment equals to True, prompt user to enter equipment
    if update_equipment:
        while True:
            equipment_name = input(f'\n✏️ Enter the name of selected equipment {len(equipments) + 1}: ').lower().strip()

            # if user choose to stop enter
            if equipment_name == 'done':
                if len(equipments) == 0:  # ensure user have entered at least one equipment
                    print('\n+-----------------------------------------------------------+')
                    print('|⚠️ You must enter at least one equipment before finishing. |')
                    print('+-----------------------------------------------------------+')
                    continue
                else:
                    print('\nStop adding. Continue to Recipe Instruction page......')
                    break

            # ensure the selected equipment is existed in the list given
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

                        equipments.append(equipment_name)  # append the selected equipment into the empty list
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
        # if update_equipment equals to False, prompt user to enter equipment for one time only
        while True:
            equipment_name = input(
                f'\n✏️ Enter the name of selected equipment {len(equipments) + 1}: ').lower().strip()

            if equipment_name == 'done':  # user can choose to not enter any equipment
                break

            # ensure the selected equipment is existed in the list given
            elif validation_empty_entries(equipment_name):
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

                        equipments.append(equipment_name)  # append the selected equipment to the empty list
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


# define the function to let user add instructions for recipe
def recipe_instruction():
    instructions = []  # initialize an empty list to store entered instructions

    category, recipe_name = create_recipe()  # get category and recipe name
    ingredients, ingredient_notes = recipe_ingredient(adding_ingredient=True, update_ingredient=True)  # get selected ingredient list and ingredient notes
    equipments = recipe_equipment(update_equipment=True)  # get selected equipment list

    # print the selected equipments and ingredients
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

    # prompt user to enter baking temperature and ensure it falls within valid range
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

    # prompt user to enter baking time and ensure it falls within valid range
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

    # prompt user to enter cost and ensure it greater than 0
    while True:
        try:
            cost = float(input('\nPlease provide the cost to make one unit of this product (RM): '))
            if validation_empty_entries(cost):
                if 0 < cost:
                    print('\n📝 Instructions (type "done" to finish)')
                    break
                else:
                    print('\n+-----------------------------------------------+')
                    print('|⚠️ Please enter a valid cost. (Greater than 0) |')
                    print('+-----------------------------------------------+')
        except ValueError:
            print('\n+-----------------------------------------------------+')
            print('|⚠️ Invalid input. Please enter numbers for the cost. |')
            print('+-----------------------------------------------------+')

    # prompt user to enter instructions
    while True:
        instruction = input(f'{len(instructions) + 1}. ').strip()

        if instruction == 'done':  # if user choose to stop enter
            if len(instructions) == 0:  # ensure user have entered at least one instruction
                print('\n+-------------------------------------------------------------+')
                print('|⚠️ You must enter at least one instruction before finishing. |')
                print('+-------------------------------------------------------------+')
                continue
            else:  # if user choose to stop and have entered at least one instruction
                print(f'\nStop adding instructions... Recipe {recipe_name.title()} successfully saved!')
                break  # break the loop

        if validation_empty_entries(instruction):
            instructions.append(instruction)  # append the instruction to the empty list after ensure it have value
            continue

    # save the recipe data to baker recipe file
    recipe_data[recipe_name] = {
        'recipe_category': category,
        'recipe_name': recipe_name,
        'ingredient_used': ingredients,
        'ingredient_notes': ingredient_notes,
        'equipment_used': equipments,
        'baking_temperature': baking_temperature,
        'baking_time': baking_time,
        'cost_per_unit': cost,
        'instructions': instructions
    }

    save_info(recipe_data)

    # call the function that prompt user whether continue to add another recipe
    continue_adding_recipe()


# define the function that let user select whether continue to add another recipe
def continue_adding_recipe():
    # prompt user whether continue to add another recipe
    while True:
        add_more = input('\nContinue adding new recipe? (y=yes, n=no)'
                         '\n>>> ')
        if validation_empty_entries(add_more):
            if add_more == 'y':  # if yes, recursively call function
                recipe_instruction()
                break
            elif add_more == 'n':  # if no, return to recipe management page
                print('\nStop adding. Exiting to Recipe Management page......')
                recipe_management()
                break
            else:
                print('\n+-------------------------------------------+')
                print('|⚠️ Invalid input. Please enter "y" or "n". |')
                print('+-------------------------------------------+')


# define the function to display the details of selected recipe
def display_recipe(recipe):
    # print the details of selected recipe with formatting
    print(f'{"recipe_category":<20}: {recipe["recipe_category"]}')
    print(f'{"recipe_name":<20}: {recipe["recipe_name"]}')
    print(f'\n{"🥗 ingredient_used"}:')
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
    print(f'\n{"ingredient_notes":<20}: {recipe["ingredient_notes"]}')
    print(f'\n{"🛠️ equipment_used"}:')
    equipment_index = 1
    for item in recipe['equipment_used']:
        print(f'{equipment_index}. {item.title()}')
        equipment_index += 1
    print(f'\n{"baking_temperature (°C)":<26}: {recipe["baking_temperature"]}')
    print(f'{"baking_time (min)":<25}: {recipe["baking_time"]}')
    print(f'{"cost_per_unit (RM)":<25}: {recipe["cost_per_unit"]}')
    print(f'\n{"instructions"}:')
    instruction_index = 1
    for instruction in recipe['instructions']:
        print(f'{instruction_index}. {instruction.capitalize()}')
        instruction_index += 1


# define the function that let user update chosen recipe
def update_recipe():
    while True:
        index = 1
        printed_centered('RECIPE LIST')
        for key, recipe in recipe_data.items():
            print(f'{index}. {recipe["recipe_name"].title()}')  # print the index with recipe name
            index += 1
        print(f'{len(recipe_data) + 1}. Cancel')

        # prompt user to select a recipe to edit
        try:
            index_of_product_to_edit = int(
                input(
                    f'\nEnter index number to update the information of the recipe (or enter {len(recipe_data) + 1} to cancel):\n>>> '))

            if index_of_product_to_edit == len(recipe_data) + 1:  # if "Cancel" is selected
                print('\nCancelling. Exiting to Product Management page......')  # return to the previous page
                recipe_management()
                break

            # id selected index falls within valid range
            elif 1 <= index_of_product_to_edit <= len(recipe_data):
                for key, recipe in recipe_data.items():
                    selected_recipe_key = list(recipe_data.keys())[
                        index_of_product_to_edit - 1]  # indicate which recipe is selected
                    break
            else:
                print('\n❗Recipe not found.')  # error displayed if selected product not found
                continue

        except ValueError:
            print('\n+-----------------------------------------+')
            print('|⚠️ Invalid input. Please enter a number. |')
            print('+-----------------------------------------+')
            continue

        # loop until a valid new value of product attribute is updated
        while True:
            selected_recipe_key = list(recipe_data.keys())[
                index_of_product_to_edit - 1]  # indicate which recipe is selected

            # print the details of selected recipe
            print('\n--------------------------------------------------')
            print(f'\t\t\t\t {selected_recipe_key.upper()}\'S DATA')
            print('--------------------------------------------------')

            display_recipe(recipe_data[selected_recipe_key])

            print(
                '\nTo change the information, please enter the exact matching name but without the (). Example: baking_time.')

            # prompt user to enter an attribute for update
            attribute_of_recipe_data = input('Which information do you want to update? (or enter \"cancel\")\n>>> ')

            # if user choose cancel, return to the recipe list
            if attribute_of_recipe_data == 'cancel':
                print('\nCancelling. Exiting to the Recipe List......')
                update_recipe()
                break

            # handle the update for ingredient used
            elif attribute_of_recipe_data == 'ingredient_used':

                # print current ingredient with its index
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

                # prompt user to add, edit or delete ingredient
                print('')
                edit_ingredient = input(
                    "Add, edit or delete ingredient? \nPlease enter 'add', 'edit' or 'delete' (or enter 'cancel' to stop): ")

                # if user choose to add ingredient
                if edit_ingredient == 'add':
                    # call the recipe_ingredient function with the adding_ingredient parameter = True and update_ingredient = False
                    new_ingredient_list, notes = recipe_ingredient(adding_ingredient=True, update_ingredient=False)
                    if new_ingredient_list:  # if the new_ingredient_list have value
                        recipe_data[selected_recipe_key]['ingredient_used'].extend(new_ingredient_list)
                        save_info(recipe_data)  # get the value in ingredient list and save to baker recipe file
                        print('\nInformation saved.')
                        continue
                    else:
                        # if ingredient list have no value, print the message
                        print('\nNo new ingredient added.')
                        continue

                # if user choose to edit
                elif edit_ingredient == 'edit':
                    while True:
                        try:
                            # get the selected ingredient
                            edit_ingredient = input(
                                "\nPlease enter the index number of ingredient you want to edit (or enter 'cancel')\n>>> ")

                            if not validation_empty_entries(edit_ingredient):
                                continue

                            if edit_ingredient == 'cancel':
                                break  # if user choose cancel, exit the loop

                            edit_ingredient = int(edit_ingredient)

                            # ensure the selected index falls within valid range
                            if 1 <= edit_ingredient <= len(recipe_data[selected_recipe_key]['ingredient_used']):
                                # get the new value of updated ingredient
                                new_ingredients, notes = recipe_ingredient(adding_ingredient=False,
                                                                           update_ingredient=False)
                                if new_ingredients:
                                    recipe_data[selected_recipe_key]['ingredient_used'][edit_ingredient - 1] = \
                                        new_ingredients[0]
                                    save_info(recipe_data)  # save the new value to baker recipe file
                                    print('\nInformation saved.')
                                    break
                                else:
                                    print('\nNo new ingredient added.')
                                    break
                            # prompt user to enter again if input is invalid
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

                # if user choose to delete
                elif edit_ingredient == 'delete':
                    while True:
                        try:
                            # get the selected ingredient
                            delete_ingredient = input(
                                "\nPlease enter the index number of ingredient you want to delete (or enter 'cancel')\n>>> ").lower().strip()
                            if not validation_empty_entries(delete_ingredient):
                                continue

                            if delete_ingredient == 'cancel':
                                break  # if user choose cancel, exit the loop

                            delete_ingredient = int(delete_ingredient)

                            # ensure the selected index falls within valid range
                            if 1 <= delete_ingredient <= len(recipe_data[selected_recipe_key]['ingredient_used']):
                                del recipe_data[selected_recipe_key]['ingredient_used'][delete_ingredient - 1]
                                save_info(recipe_data)  # delete the specific ingredient based on the index and save data
                                print('\nIngredient deleted.')
                                break
                            #
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
                # prompt user to enter again if input is invalid
                else:
                    print('\n+-----------------------------------------------------+')
                    print('|⚠️ Please enter "add", "edit", "delete" or "cancel". |')
                    print('+-----------------------------------------------------+')
                    continue

            # handle update for equipment used
            elif attribute_of_recipe_data == 'equipment_used':
                equipment_index = 1
                print('')
                for item in recipe_data[selected_recipe_key]['equipment_used']:
                    print(f'{equipment_index}. {item.title()}')  # print the equipment name with index
                    equipment_index += 1
                print('')

                # prompt user to add, edit or delete ingredient
                edit_equipment = input(
                    "Add, edit or delete ingredient? \nPlease enter 'add', 'edit' or 'delete' (or enter 'cancel' to stop): ")

                # if user choose to add
                if edit_equipment == 'add':
                    # call the recipe_equipment function with the update_ingredient parameter = False
                    new_equipment = recipe_equipment(update_equipment=False)
                    if new_equipment:
                        recipe_data[selected_recipe_key]['equipment_used'].extend(new_equipment)
                        save_info(recipe_data)  # get the new equipment and save to baker recipe file
                        print('\nInformation saved.')
                        continue
                    else:
                        print('\nNo new equipment added.')
                        continue

                # if user choose to edit
                elif edit_equipment == 'edit':
                    while True:
                        try:
                            # get the selected equipment
                            new_edit_equipment = input(
                                "\nPlease enter the index number of ingredient you want to edit (or enter 'cancel')\n>>> ")

                            if not validation_empty_entries(new_edit_equipment):
                                continue

                            # if user choose to cancel, exit the loop
                            if new_edit_equipment == 'cancel':
                                break

                            new_edit_equipment = int(new_edit_equipment)

                            # if selected index falls within valid range
                            if 1 <= new_edit_equipment <= len(recipe_data[selected_recipe_key]['equipment_used']):
                                new_equipment = recipe_equipment(update_equipment=False)

                                if new_equipment:  # get the new value of updated equipment
                                    recipe_data[selected_recipe_key]['equipment_used'][new_edit_equipment - 1] = \
                                        new_equipment[0]
                                    save_info(recipe_data)  # save new value to baker recipe file
                                    print('\nInformation saved.')
                                    break
                                else:
                                    print('\nNo equipment edited.')
                                    break
                            # prompt user to enter again if input is invalid
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

                # if user choose to delete
                elif edit_equipment == 'delete':
                    while True:
                        try:
                            # get the selected equipment
                            delete_equipment = input(
                                "\nPlease enter the index number of ingredient you want to delete (or enter 'cancel')\n>>> ").lower().strip()
                            if not validation_empty_entries(delete_equipment):
                                continue

                            # if user choose to cancel, exit the loop
                            if delete_equipment == 'cancel':
                                break

                            delete_equipment = int(delete_equipment)

                            # if selected index falls within valid range
                            if 1 <= delete_equipment <= len(recipe_data[selected_recipe_key]['equipment_used']):
                                del recipe_data[selected_recipe_key]['equipment_used'][delete_equipment - 1]
                                save_info(recipe_data)  # delete the selected equipment and save data
                                print('\nEquipment deleted.')
                                break
                            # prompt user to enter again if input is invalid
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
                # if user choose to cancel, exit the loop
                elif edit_equipment == 'cancel':
                    break

                else:
                    print('\n+-----------------------------------------------------+')
                    print('|⚠️ Please enter "add", "edit", "delete" or "cancel". |')
                    print('+-----------------------------------------------------+')
                    continue

            # handle update of instructions
            elif attribute_of_recipe_data == 'instructions':
                instructions = []  # initialize an empty list to store new instructions

                instruction_index = 1
                for instruction in recipe_data[selected_recipe_key]['instructions']:
                    print(f'{instruction_index}. {instruction.title()}')  # print current instructions
                    instruction_index += 1
                print('')

                print('Enter new instruction. (type "done" to finish updating, "cancel" to exit to previous page.)')

                # prompt user to enter new instructions
                while True:
                    instruction = input(f'{len(instructions) + 1}. ').strip()

                    if instruction == 'done':  # if user choose to stop enter
                        if len(instructions) == 0:  # ensure they enter at least one instruction
                            print('\n+-----------------------------------------------------------+')
                            print('|⚠️ You must enter at least one equipment before finishing. |')
                            print('+-----------------------------------------------------------+')
                            continue
                        else:  # if instructions list have value
                            recipe_data[selected_recipe_key]['instructions'] = instructions
                            save_info(recipe_data)  # update the instructions with new value and save data
                            print(f'\nInformation saved.')
                            break

                    # if user choose to cancel, break the loop
                    if instruction == 'cancel':
                        break

                    # if user input have value and not equals to 'done', append the value to instruction list
                    if validation_empty_entries(instruction):
                        instructions.append(instruction)
                        continue

            # handle general attribute update
            elif attribute_of_recipe_data in recipe:
                while True:
                    # prompt user to enter a new value for the selected attribute
                    new_value = input(f'\nEnter new {attribute_of_recipe_data}: ')

                    # ensure the new_value have value
                    if not validation_empty_entries(new_value):
                        continue

                    else:
                        # ensure the new category is existed based on the given list
                        if attribute_of_recipe_data == 'recipe_category':
                            print('\n💡 Categories: Breads, Cakes, Pastries, Biscuits, Muffins, Others 💡')
                            if new_value.strip().isalpha():
                                if new_value not in ['Breads', 'Cakes', 'Pastries', 'Biscuits', 'Muffins', 'Others']:
                                    print(
                                        '+----------------------------------------------------------------------------------+')
                                    print(
                                        '|⚠️ Please enter a valid category based on the categories given. (Case sensitive.) |')
                                    print(
                                        '+----------------------------------------------------------------------------------+')
                                    continue
                            else:
                                print(
                                    '+-----------------------------------------------------------------------------------------------+')
                                print(
                                    '|⚠️ Please enter a valid category. (Cannot contain any spacing, digits and special characters.) |')
                                print(
                                    '+-----------------------------------------------------------------------------------------------+')
                                continue

                        # ensure the new recipe name does not exist in baker recipe file
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

                        # ensure new ingredient notes have value
                        elif attribute_of_recipe_data == 'ingredient_notes':
                            if not validation_empty_entries(new_value):
                                continue

                        # ensure new baking temperature is digit and fall within valid range
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

                        # ensure new baking time is digit and fall within valid range
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

                        # ensure new cost per unit is digit and greater than 0
                        elif attribute_of_recipe_data == 'cost_per_unit':
                            try:
                                new_value = float(new_value)
                                if not 0 < new_value:
                                    print('\n+-----------------------------------------------+')
                                    print('|⚠️ Please enter a valid cost. (Greater than 0) |')
                                    print('+-----------------------------------------------+')
                                    continue
                            except ValueError:
                                print('\n+-----------------------------------------------------+')
                                print('|⚠️ Invalid input. Please enter numbers for the cost. |')
                                print('+-----------------------------------------------------+')
                                continue

                        print(
                            f'\n{attribute_of_recipe_data} of {selected_recipe_key} is updated.')  # inform user about the data is updated
                        recipe_data[selected_recipe_key].update(
                            {attribute_of_recipe_data: new_value})  # assign the new value entered to the attributes
                        save_info(recipe_data)  # save the data
                        break
            else:
                print('\n❗Data not found.')  # error displayed if attribute entered not found


# define the function that let user delete recipe
def delete_recipe():
    while True:
        index = 1
        print('\n-----------------------------------------------')
        print('\t\t\t\t', '', 'RECIPE LIST')
        print('-----------------------------------------------')
        for name, info in recipe_data.items():
            print(f'{index}. {name.title()}')  # print recipe name with its index
            index += 1
        print(f'{len(recipe_data) + 1}. cancel')

        try:
            index_remove_recipe = int(
                input(f'\nWhich recipe do you want to remove? (or enter {len(recipe_data) + 1} to cancel)\n>>> '))
            if index_remove_recipe == len(recipe_data) + 1:  # if user choose 'cancel'
                print('\nCancelling. Exiting to Services page......')
                recipe_management()  # return to recipe management page
                break

            # if selected index falls within valid range
            elif 1 <= index_remove_recipe <= len(recipe_data):
                recipe_to_remove = list(recipe_data.keys())[
                    index_remove_recipe - 1]  # identify recipe to remove by accessing the index of key of recipe
                del recipe_data[recipe_to_remove]  # delete the selected recipe
                save_info(recipe_data)  # save the data
                print(
                    f'\n{recipe_to_remove.title()} is removed.')  # inform user that the selected recipe is removed successfully

                # prompt user whether to remove another recipe
                while True:
                    remove_more = input(
                        '\nContinue to remove? (y=yes, n=no)\n>>> ')
                    if remove_more == 'y':  # if yes, break the loop
                        break
                    elif remove_more == 'n':  # if no, return to recipe management page
                        print('\nStop removing. Exiting to Recipe Management page......')
                        recipe_management()
                        break
                    # prompt user to enter again if input is invalid
                    else:
                        print('\n+--------------------------------------+')
                        print('|⚠️ Invalid input. Please enter again. |')
                        print('+--------------------------------------+')
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')

        except ValueError:
            print('\n+-----------------------------------------+')
            print('|⚠️ Invalid input. Please enter a number. |')
            print('+-----------------------------------------+')


#update_recipe()
#recipe_management()
