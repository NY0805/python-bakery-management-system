import json  # import json text file to record data


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


ingredient_data = {}


def ingredient_management():
    print('\n-------------------------------------------------------')
    print('\t\t\t\t', '', 'INGREDIENT MANAGEMENT')
    print('-------------------------------------------------------')
    print('\n1. Add Ingredient')
    print('2. Update Ingredient')
    print('3. Remove Ingredient')
    print('4. Back to Previous Page')

    while True:
        option_product_management = input('\nPlease choose a service:'
                                          '\n>>> ')
        if option_product_management not in ['1', '2', '3', '4']:
            print('Please enter a valid number.')
        else:
            if option_product_management == '1':
                ingredient_details()
                break
            elif option_product_management == '2':
                pass
            elif option_product_management == '3':
                pass
            elif option_product_management == '4':
                print('Exiting to previous page...')
                break


def ingredient_categories():
    print('\nHere are the main types of bakery ingredients:')
    print('\n1. Flours and Grains')
    print('2. Sweeteners')
    print('3. Fats and Oils')
    print('4. Dairy and Non-Dairy Products')
    print('5. Leavening Agents')
    print('6. Spices and Flavouring')
    print('6. Fillings and Toppings')
    print('7. Fruits and Vegetables')
    print('8. Preservatives and Stabilizers')
    print('9. Others')
    print('10. Back to Previous Page')

    while True:
        option_product_categories = input('\nPlease input the category:'
                                          '\n>>> ')
        if option_product_categories not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            print('Please enter a valid number.')
            continue
        else:
            if option_product_categories == '10':
                print('Going back to the previous page.')
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


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('Please enter something...\n')
        return False


def ingredient_details():
    print('\nPlease fill out the following fields to add a new ingredient to the inventory:')


    # List to hold the input prompts based on ingredient type
    prompts = [
        ('ingredient_name', 'Ingredient Name'),
        ('ingredient_unit_measurement', 'Unit Measurement'),
        ('batch_number', 'Batch Number')
    ]

    # Add conditional prompts based on ingredient_main_type
    if ingredient_main_type_choice == 1:
        prompts.insert(1, ('type_number', 'Type Number'))  # Insert Type Number after Ingredient Name
    elif ingredient_main_type_choice == 2:
        prompts.append(('solidity', 'Solidity'))  # Append Solidity at the end

    # Calculate the maximum length of prompt text for alignment
    max_prompt_length = max(len(prompt_text) for _, prompt_text in prompts)

    # Loop through the prompts list and ask for input with alignment
    for i, (key, prompt_text) in enumerate(prompts, start=1):
        # Format the prompt text to align the input fields
        formatted_prompt = f'{i}. {prompt_text.ljust(max_prompt_length + 2)}: '
        ingredient_info[key] = input(formatted_prompt)


def continue_adding():
    while True:
        try:
            add_more = input('\nInformation saved. Continue adding? (y=yes, n=no)'
                             '\n>>> ')
            if add_more == 'y':
                ingredient_details()
                break
            elif add_more == 'n':
                print('Stop adding... Existing to Product Management page.')
                ingredient_management()
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        except ValueError:
            print('Invalid input. Please enter again.')
