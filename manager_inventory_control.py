import json
import manager_inventory_ingredient


# Define the function that loads product data from the file
def load_data_from_product():
    try:
        file = open('baker_product_keeping.txt', 'r')  # open the file and read
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


# Define the function that loads product inventory data from the file
def load_data_from_manager_product_inventory():
    try:
        file = open('manager_product_inventory.txt', 'r')  # open the file and read
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


# Define the function that saves product_inventory data to the file
def save_info_product_inventory(product_inventory):
    file = open('manager_product_inventory.txt', 'w')  # open the file to write
    json.dump(product_inventory, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# Define the function that saves product data to the file
def save_info_product(product):
    file = open('baker_product_keeping.txt', 'w')  # open the file to write
    json.dump(product, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


product = load_data_from_product()  # store the data that retrieved from file into product
product_inventory = load_data_from_manager_product_inventory()  # store the data that retrieved from file into product_inventory


# define the function to control product inventory
def inventory_control_product():
    while True:
        if len(product_inventory) == 0:
            print('\n❗The product inventory is empty. Please restock in time.')  # output a warning message when the product in inventory is empty

        # display the options of how to control the product in the inventory
        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'PRODUCT MANAGEMENT')
        print('-----------------------------------------------')
        print('1. Add products into inventory\n2. Remove products from inventory\n3. Update products in inventory\n4. Back to Main Inventory Management⛔🔙\n')
        product_control = input('\nWhat action do you wish to perform? (1, 2, 3, 4)\n>>> ')  # collect user preference

        while True:

            if product_control == '1':  # add products into inventory
                print('\n-----------------------------------------------')
                print('\t', '', 'CURRENT PRODUCTS PRODUCED BY BAKERS')
                print('-----------------------------------------------')

                # retrieve the information of product name and quantity to display
                for key, value in product.items():
                    product_name = value['product_name']
                    quantity = len(value['serial_number'])  # determine how many serial number for each product to represent the quantity of the product

                    print(f'Product name: {product_name:<15} quantity: {quantity}')

                chosen_product = input('\nWhich product do you want to restock? (or enter "cancel" to cancel)\n>>> ')  # collect user's chosen product

                if chosen_product == 'cancel':
                    print('\nCancelling. Exiting to Product Management page......')
                    break

                product_found = False
                for batch_number, value in product.items():
                    if chosen_product == value['product_name']:  # check if the chosen product is in the list of product name
                        product_found = True
                        while True:
                            try:
                                add_stock = int(input(f'\nNumber of {chosen_product} to add: '))  # collect the number of each product to add into the inventory
                                if add_stock < 0:  # validate the input is not smaller than 0
                                    print('\n+-------------------------------+')
                                    print('|⚠️ Please enter a valid input. |')
                                    print('+-------------------------------+')

                                elif add_stock == 0:  # input equals to 0 means nothing is added
                                    print('\n💡 No product is added.')
                                    break

                                else:
                                    serial_number = value['serial_number']

                                    if add_stock > len(serial_number): # if the input exceed the actual quantity of the products
                                        print(f'\n⚠️ Not enough. The current number of {chosen_product}(s) is(are) {len(serial_number)}.')
                                        add_stock = 0
                                        break

                                    if batch_number in product_inventory:  # check whether th products already exist in the inventory
                                        stock = int(product_inventory[batch_number]['stock']) + add_stock  # add the user input to the previous quantity
                                    else:
                                        stock = add_stock  # directly assign the quantity products if the products haven't in the inventory

                                    #if 'price' not in product_inventory.get(batch_number, {}):  # check if the products are newly added into the inventory that not priced yet, and return empty value instead of errors vice versa
                                    if 'price' not in product_inventory[batch_number] or batch_number not in product_inventory:
                                        while True:
                                            try:
                                                price = float(input('Price per unit: RM '))  # determine the price per unit for each newly added products
                                                if price < 0:  # validate the price as a positive number
                                                    print('\n+-----------------------------------+')
                                                    print('|⚠️ Please enter a positive number. |')
                                                    print('+-----------------------------------+\n')
                                                price = f'RM {price:.2f}'  # convert the price into 2 decimal places
                                                break

                                            except ValueError:
                                                print('\n+------------------------------+')
                                                print('|⚠️ Please enter numbers only. |')
                                                print('+------------------------------+\n')
                                    else:
                                        price = product_inventory[batch_number]['price']  # the original price will not be updated if the products is already in the inventory

                                    if 'description' not in product_inventory.get(batch_number, {}):  # check if the products are newly added into the inventory that no description yet, and return empty value instead of errors vice versa
                                        product_description = input('Add product description for menu display:\n>>> ')  # add the product description
                                    else:
                                        product_description = product_inventory[batch_number]['description']  # the existing descripiton will not be updated if the products are already in the inventory

                                    # update the dictionary with user input
                                    product_inventory[batch_number] = {
                                        'product_name': chosen_product,
                                        'stock': stock,
                                        'price': price,
                                        'description': product_description
                                    }

                                    quantity = len(serial_number) - add_stock  # reduce the quantity of products in record keeping after being added into inventory
                                    # if the quantity of products finished, the record for the particular product will be deleted
                                    if quantity <= 0:
                                        del product[batch_number]
                                    else:
                                        del serial_number[0: add_stock]  # if there is any product left, the system will only delete the serial number of the particular product that has been added into the inventory

                                    # save the updates of both product inventory and product record keeping
                                    save_info_product(product)
                                    save_info_product_inventory(product_inventory)

                                    #  display messages that inform users about the updates
                                    print(f'\n{add_stock} {chosen_product}(s) is(are) added into the inventory.')
                                    print(f'Current stock of {chosen_product} in product inventory: {stock}')
                                    break

                            except ValueError:
                                print('\n+--------------------------+')
                                print('|⚠️ Please enter a number. |')
                                print('+--------------------------+')

                if not product_found:
                    print('\n❗Product not found, enter again.')  # error message appears if the chosen products are not found

            elif product_control == '2':  # remove products from the inventory
                if len(product_inventory) == 0:
                    print('\n❗Out of stock!')  # warning message when the inventory is empty and nothing can be removed
                    break

                else:
                    print('\n-----------------------------------------------')
                    print('\t\t\t', ' ', 'PRODUCT INVENTORY')
                    print('-----------------------------------------------')
                    for batch_number, value in product_inventory.items():
                        product_name = value['product_name']
                        available_quantity = value['stock']

                        print(f'{product_name:<15}: {available_quantity}')  # display the products and their corresponding stock quantity

                    product_stock = input('\nWhich products do you want to reduce? (or enter "cancel" to cancel)\n>>> ')  # collect chosen product to remove

                    if product_stock == 'cancel':
                        print('\nCancelling. Exiting to Product Management page......')
                        break

                    product_found = False
                    for batch_number, value in product_inventory.items():
                        if product_stock == value['product_name']:  # check if the chosen product found in the inventory
                            product_found = True
                            while True:
                                try:
                                    quantity_to_reduce = int(input(f'\nNumber of {product_stock} to reduce: '))  # collect thr quantity of products to remove
                                    if quantity_to_reduce < 0:
                                        print('\n+-------------------------------+')
                                        print('|⚠️ Please enter a valid input. |')
                                        print('+-------------------------------+')

                                    elif quantity_to_reduce == 0:
                                        print('\n💡 No product is reduced.')
                                        break

                                    else:
                                        available_stock = value['stock']

                                        if quantity_to_reduce > available_stock:  # check if the quantity inputted exceed the original stock in the inventory
                                            print(f'⚠️ Out of range. The current stock of {product_stock}(s) is(are) {available_stock}.')
                                            break

                                        else:
                                            stock_left = available_stock - quantity_to_reduce  # update the value of stock after being removed
                                            print(f'\n{quantity_to_reduce} {product_stock}(s) is(are) reduced.')

                                        # update the dictionary with user input
                                        product_inventory[batch_number] = {
                                            'product_name': product_stock,
                                            'stock': stock_left,
                                            'price': value['price'],
                                            'description': value['description']
                                        }

                                        if stock_left <= 0:
                                            del product_inventory[batch_number]  # if there is no stock left, delete the product from the inventory
                                            print('\n+-------------------------------------------------------------------------------+')
                                            print(f'|⚠️ Last {product_stock} has finished. Ask bakers to bake more {product_stock}. |')
                                            print('+-------------------------------------------------------------------------------+')
                                        break


                                except ValueError:
                                    print('\n+--------------------------+')
                                    print('|⚠️ Please enter a number. |')
                                    print('+--------------------------+')
                            save_info_product_inventory(product_inventory)
                            break
                    if not product_found:
                        print('\n❗Product not found, enter again.')



            elif product_control == '3':  # update product details in the inventory
                if len(product_inventory) == 0:
                    print('\n❗Out of stock!')  # warning message appears if the inventory is empty
                    break

                while True:
                    index = 1
                    print('\n-----------------------------------------------')
                    print('\t\t\t\tPRODUCT LIST')
                    print('-----------------------------------------------')
                    for key, value in product_inventory.items():
                        print(f'{index}. {value["product_name"].title()}')
                        index += 1
                    print(f'{len(product_inventory) + 1}. cancel')

                    try:
                        product_to_update = int(input('\nEnter the product\'s index number to update: '))
                        if product_to_update == len(product_inventory) + 1:  # Cancel update
                            print('\nCancelling. Exiting to Product Management page......')
                            break

                        elif 1 <= product_to_update <= len(product_inventory):  # if user input in the range of product quantity in the inventory
                            selected_product = list(product_inventory.keys())[product_to_update - 1]  # append all the keys into a list and identify the selected product by indexing
                            while True:
                                # display the product name
                                print('\n-----------------------------------------------')
                                print(f'\t\t\t\t {product_inventory[selected_product]["product_name"].upper()}')
                                print('-----------------------------------------------')

                                for product_inventory_key, product_inventory_value in (product_inventory[selected_product].items()):
                                    print(f'{product_inventory_key}: {product_inventory_value}')  # display the dedtails of the selected product

                                attribute_of_product_inventory = input('\nWhich information do you want to update? (or enter \"cancel\")\n>>> ')  # collect attribute of the product to update
                                if attribute_of_product_inventory in product_inventory[selected_product]:  # check if the attribute found in the selected product details

                                    while True:
                                        try:
                                            new_value = input(f'\nEnter new {attribute_of_product_inventory}: ')  # prompt user to enter new value for the attribute

                                            # validate the new value for each attribute
                                            if attribute_of_product_inventory == 'product_name':  # if new value equals to the current product name, duplication occurs
                                                duplicate = False
                                                for value in product_inventory.values():
                                                    if new_value == value['product_name']:
                                                        print('\n+-----------------------------------------------------------------------+')
                                                        print('|⚠️ Duplicate product name detected. Please enter another product name. |')
                                                        print('+-----------------------------------------------------------------------+')
                                                        duplicate = True
                                                        break
                                                if duplicate:
                                                    continue

                                            elif attribute_of_product_inventory == 'stock':
                                                with open('baker_product_keeping.txt', 'r') as product_keeping:
                                                    products = json.load(product_keeping)

                                                    serial_number = products[selected_product]['serial_number']
                                                    if int(new_value) > len(serial_number):  # check if stock to update exceed the current quantity of products in the record keeping
                                                        print('\n+-----------------------------------------------------------+')
                                                        print(f'|⚠️ The current stock of {products[selected_product]["product_name"]} is {len(serial_number)}. Please enter again. |')
                                                        print('+-----------------------------------------------------------+')
                                                        continue

                                            elif attribute_of_product_inventory == 'price':
                                                try:
                                                    new_value = float(new_value)  # Ensure the entered value is a valid float number
                                                    new_value = f'RM {new_value:.2f}'  # Format the price as 'RM {value}' with 2 decimal places
                                                except ValueError:
                                                    print('\n+-------------------------------+')
                                                    print('|⚠️ Please enter a valid price. |')
                                                    print('+-------------------------------+')
                                                    continue  # Ask for new input if the price is not valid

                                            # update the information
                                            product_inventory[selected_product][attribute_of_product_inventory] = new_value
                                            print(f'\n{attribute_of_product_inventory.title().replace("_", " ")} is updated.')
                                            save_info_product_inventory(product_inventory)
                                            break

                                        except ValueError:
                                            print('\n+------------------------------+')
                                            print('|⚠️ Please enter numbers only. |')
                                            print('+------------------------------+')

                                elif attribute_of_product_inventory == 'cancel':
                                    print('\nCancelling. Exiting to Product List......')
                                    break

                                else:
                                    print('\n❗Data not found.')  # error message appears if attribute entered not found
                        else:
                            print('\n❗Product not found.')  # error message appears if product entered not found

                    except ValueError:
                        print('\n+--------------------------+')
                        print('|⚠️ Please enter a number. |')
                        print('+--------------------------+')
                break

            elif product_control == '4':  # return to the previous page
                print('\nExiting to Main Inventory Management......')
                return False

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+')
                break


# main inventory control for products and ingredients
def inventory_control():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t', ' ', 'MAIN INVENTORY MANAGEMENT')
        print('-----------------------------------------------')
        print('1. Ingredient Inventory\n2. Product Inventory\n3. Back to Manager Privilege⛔🔙')

        # determine which inventory to manage and execute their corresponding functions
        control = input('\nSelect the inventory that you want to manage(1, 2, 3, 4):\n>>> ')
        if control == '1':
            manager_inventory_ingredient.ingredient_management()

        elif control == '2':
            inventory_control_product()

        elif control == '3':
            print('\nExiting to Manager Privilege......')
            break

        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')


#inventory_control()