import re  # import the regular expressions(regex), a type of text pattern matching tool to check if a string contains the specified search pattern
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
def save_info(info):

    file = open('inventory_ingredient.txt', 'w')  # open the file to write
    json.dump(info, file, indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing

option = int(input('choose service:\n'
                   '1. inventory management\n'
                   '2. etctectetc\n'
                   '>>> '))

def inventory_services():

    print('\nEasily manage your bakery\'s inventory with our system!')
    print('With our system, you can effortlessly:\n'
          '\t- Add new ingredients and product\n'
          '\t- Update inventory details\n'
          '\t- Remove outdated or unused items\n'
          '\t- Check inventory levels')
    print('Stay on top of your supplies to ensure fresh and delicious baked goods every day!')

    while True:
        print('\n-------------------------------------------------------')
        print('\t\t\t', '', 'INVENTORY MANAGEMENT MENU')
        print('-------------------------------------------------------\n')
        print('1. Ingredient Management')
        print('2. Product Management\n')

        inventory_services_type = int(input('Please choose a service:\n'
                                            '>>> '))

        if inventory_services_type == 1:
            print('\n-------------------------------------------------------')
            print('\t\t\t\t', '', 'INGREDIENT MANAGEMENT')
            print('-------------------------------------------------------')
            print('\n1. Add Ingredient')
            print('2. Update Ingredient')
            print('3. Remove Ingredient')

            ingredient_management_services_type = int(input('\nPlease choose a service:'
                                                            '\n>>> '))

            if ingredient_management_services_type == 1:
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
                ingredient_main_type = int(input('Please input the main type of bakery ingredients:'
                                                 '\n>>> '))

                    if ingredient_main_type == 1:
                        print()kk



if option == 1:
    inventory_services()