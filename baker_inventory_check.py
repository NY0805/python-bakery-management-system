import json
import random
import time


# loads available ingredient data from the file
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


# loads previously produced product data from the file
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


# loads recipe data from the file
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


# function that save data of produced product to baker inventory check file
def save_info_inventory_check(product_produce):
    file = open('baker_inventory_check.txt', 'w')  # open the file to write
    json.dump(product_produce, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# function that save the updated ingredient quantity to inventory ingredient file
def save_info_inventory_ingredient(ingredient_used):
    file = open('inventory_ingredient.txt', 'w')  # open the file to write
    json.dump(ingredient_used, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# function that validate empty entries
def validation_empty_entries(info):
    if info:
        return True
    else:
        print('❗Please enter something...\n')
        return False


# function that format the recipe data
def format_recipe_name(product):
    return (
        f"{product['recipe_name'].title()}"
    )


# function to print message with border on top and bottom
def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


# load product, ingredient and recipe data from different file
product_list = load_data_from_inventory_check()
recipe_list = load_data_from_baker_recipe()
ingredient_list = load_data_from_inventory_ingredient()

recipe_category_groups = {}  # initialize an empty dictionary to group recipe items by category
for value in recipe_list.values():  # loop through recipe data and get the category for current recipe
    recipe_category = value['recipe_category']

    if recipe_category not in recipe_category_groups:  # if the category does not exist as a key in the dictionary
        recipe_category_groups[recipe_category] = []  # create a new empty list with the category as the key

    # if the category already exist as a key, append the current recipe details
    recipe_category_groups[recipe_category].append(format_recipe_name(value))


# define function that check the availability of ingredients and produce products based on user input quantity
def recipe_lists():
    while True:
        while True:
            # generate a 4 digit unique report number for each report
            report_num = random.randint(1000, 9999)
            if report_num not in product_list.keys():  # break when the generated report number is not duplicate
                break

        # display the recipe list by category
        print('')
        printed_centered('RECIPE LIST')
        for category, items in recipe_category_groups.items():
            index = 1
            print(f'📍 {category} 📍')
            for ingredient in items:
                print(f"{index}. {ingredient.title()}")
                index += 1
            print('')

        # prompt user to select a recipe
        recipe_choose = input('What recipe you would like to work on today? Please enter the recipe name. (or enter "cancel" to back to previous page.)\n'
                              '>>> ').lower().strip()
        found_recipe = None

        if validation_empty_entries(recipe_choose):
            if recipe_choose.replace(" ", '').isalpha():
                if recipe_choose == 'cancel':  # if user enter cancel, return to baker privilege page
                    return False
                else:
                    for category, items in recipe_category_groups.items():  # ensure user input recipe is exist in the list
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
            break  # exit loop if a valid recipe is found

    # display details for selected recipe
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

    while True:
        try:
            # prompt user to enter production quantity
            quantity = int(input('\nPlease enter the quantity you want to produce: '))

            print('\nChecking the availability of required ingredient......')

            # extract the selected recipe and its corresponding category
            selected_recipe = recipe_list[recipe_choose]
            selected_category = recipe_list[recipe_choose]['recipe_category']

            availability = True  # initialize the availability of ingredient to True
            max_possible_quantity = float('inf')  # initialize the variable to infinity to track the maximum possible production quantity
            unavailable_ingredients = []  # create an empty list to store the unavailable ingredient name

            # check ingredient availability and convert units if necessary
            for item in selected_recipe['ingredient_used']:
                ingredient_name = item[0]
                quantity_needed = float(quantity) * item[1]  # calculate the quantity needed by multiple quantity by ingredient used
                unit_measurement = item[2].lower()

                current_quantity = None  # initialize current ingredient quantity to None

                for key, items in ingredient_list.items():
                    if items['ingredient_name'].lower() == ingredient_name.lower():

                        # if the unit of ingredient in recipe is same as the unit in inventory ingredient file
                        if items['unit_measurement'] == unit_measurement:
                            current_quantity = items['quantity_purchased']  # current ingredient quantity equals to quantity in inventory ingredient file
                            break

                        # if the unit of inventory ingredient file is bigger than in recipe
                        elif ((items['unit_measurement'] == 'kg' and unit_measurement == 'g') or
                              (items['unit_measurement'] == 'l' and unit_measurement == 'ml') or
                              (items['unit_measurement'] == 'l' and unit_measurement == 'g') or
                              (items['unit_measurement'] == 'kg' and unit_measurement == 'ml')):
                            current_quantity = items['quantity_purchased'] * 1000  # multiple the ingredient quantity of inventory ingredient file by 1000
                            break

                        # if the unit of inventory ingredient file is smaller than in recipe
                        elif ((items['unit_measurement'] == 'g' and unit_measurement == 'kg') or
                              (items['unit_measurement'] == 'ml' and unit_measurement == 'l') or
                              (items['unit_measurement'] == 'ml' and unit_measurement == 'kg') or
                              (items['unit_measurement'] == 'g' and unit_measurement == 'l')):
                            current_quantity = items['quantity_purchased'] / 1000  # divide the ingredient quantity of inventory ingredient file by 1000
                            break

                # if quantity of particular ingredient is found in inventory ingredient file
                if current_quantity is not None:
                    # if quantity needed is smaller than ingredient quantity in inventory ingredient file
                    if quantity_needed <= current_quantity:
                        pass  # no action needed
                    else:  # if bigger
                        unavailable_ingredients.append(item[0])
                        possible_quantity = current_quantity / item[1]  # calculate the maximum quantity that can be produced
                        if possible_quantity < max_possible_quantity:
                            max_possible_quantity = possible_quantity
                        availability = False  # change availability to False
                else:
                    print('\n+--------------------------------------------------+')
                    print(f'|⚠️ {ingredient_name} not found in the inventory. |')
                    print('+--------------------------------------------------+')
                    recipe_lists()  # restart if ingredient cannot be detected
                    break

            # if availability is True
            if availability:
                print('All ingredients needed available!')
                while True:
                    # prompt user whether to confirm the production
                    production_confirmation = (input(f'\nAre you sure you want to produce {quantity} units of '
                                                     f'{selected_recipe["recipe_name"]}? Enter y for yes or n for no: '))
                    if validation_empty_entries(production_confirmation):
                        if production_confirmation == 'y':  # if user choose to produce the product
                            for item in selected_recipe['ingredient_used']:
                                ingredient_name = item[0]
                                quantity_needed = float(quantity) * item[1]
                                unit_measurement = item[2].lower()

                                # update ingredient quantity in inventory by subtract the quantity_needed, convert units if necessary
                                for key, items in ingredient_list.items():
                                    if items['ingredient_name'].lower() == ingredient_name.lower():
                                        selected_ingredient = key
                                        if items['unit_measurement'] == unit_measurement:
                                            remain_ingredient = items['quantity_purchased'] - quantity_needed
                                            ingredient_list[selected_ingredient]['quantity_purchased'] = remain_ingredient
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

                            # save the production details in the baker inventory check file
                            product_list[report_num] = {
                                'recipe_category': selected_category,
                                'recipe_name': recipe_choose,
                                'production_quantity': quantity,
                                'date_of_production': time.strftime("%d-%m-%Y")
                            }
                            save_info_inventory_check(product_list)
                            print('\nSuccessfully added!')
                            break

                        # if user choose to not produce the product
                        elif production_confirmation == 'n':
                            print('\nProduction cancelled.')
                            break  # break the loop
                        else:
                            print('\n+-------------------------------------------+')
                            print('|⚠️ Invalid input. Please enter "y" or "n". |')
                            print('+-------------------------------------------+')

                # prompt user whether to continue working on another recipe
                while True:
                    produce_more = input('\nContinue working on another recipe? (y=yes, n=no)'
                                         '\n>>> ')
                    if validation_empty_entries(produce_more):
                        if produce_more == 'y':
                            recipe_lists()  # if yes, recursively call function
                            break
                        elif produce_more == 'n':
                            print('\nStop adding. Exiting to main page......')
                            return False  # if no, return to baker privilege page
                        else:
                            print('\n+-------------------------------------------+')
                            print('|⚠️ Invalid input. Please enter "y" or "n". |')
                            print('+-------------------------------------------+')

            # if the ingredient is unavailable, print the ingredient name and maximum possible production quantity
            else:
                print(f'Not enough {", ".join(unavailable_ingredients)} in stock. You can produce a maximum of '
                      f'{max_possible_quantity:.2f} units of {selected_recipe["recipe_name"]}.')

        except ValueError:
            print('\n+--------------------------------+')
            print('|⚠️ Please enter a whole number. |')
            print('+--------------------------------+')


#recipe_lists()
