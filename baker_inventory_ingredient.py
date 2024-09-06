import json  # import json text file to record data


# Define the function that loads data from the file
def load_data_from_inventory_ingredient():
    try:
        file = open('inventory_ingredient.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


# Define the function that saves information to the file
def save_info(ingredient_info):

    file = open('inventory_ingredient.txt', 'w')  # open the file to write
    json.dump(ingredient_info, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def ingredient_management():
    print('\n-------------------------------------------------------')
    print('\t\t\t\t', '', 'INGREDIENT MANAGEMENT')
    print('-------------------------------------------------------')
    print('\n1. Add Ingredient')
    print('2. Update Ingredient')
    print('3. Remove Ingredient')

    ingredient_management_services_type = int(input('\nPlease choose a service:'
                                                    '\n>>> '))
    return ingredient_management_services_type


def ingredient_main_type_menu():
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
    ingredient_main_type = int(input('\nPlease input the main type of bakery ingredients:'
                                     '\n>>> '))
    return ingredient_main_type


def ingredient_details():
    print('\nPlease fill out the following fields to add a new ingredient to the inventory:')

    # Initialize an empty dictionary to store the ingredient details
    ingredient_info = {}

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
    add_more = input('\nInformation saved. Continue adding? (y=yes, n=no)'
                     '\n>>> ')
    if add_more == 'y':
        ingredient_main_type_menu()
    elif add_more == 'n':
        print('Stop adding... Existing to the Ingredient Management page.')
        ingredient_management()
    return add_more



