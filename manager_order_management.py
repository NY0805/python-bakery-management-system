import json


# Define the function that loads customers' orders data from the file
def load_data_from_customer_order_list():
    try:
        file = open('customer_order_list.txt', 'r')  # open the file and read
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


# Define the function that saves customers' orders data to the file
def save_info(order_list):
    file = open('customer_order_list.txt', 'w')  # open the file to write
    json.dump(order_list, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


order_list = load_data_from_customer_order_list()  # store the data that retrieved from file into order_list


# function to display customers' orders
def order_management():
    while True:
        print('\n', '\t'*13, 'ORDER DETAILS')
        print('-' * 125)
        header = ['Cart Id']  # create a list for headers and append the first item in the list

        for value in order_list.values():  # access the values of order_list
            for sub_key, sub_value in value.items():  # access the subkey and sub value in the value of order_list
                header.append(sub_key.title().replace('_', ' '))  # append other details of orders into the header list and replace all underscore with space to enhance readability
            break

        print(f'{header[1]:<19}{header[0]:<19}{header[2]:<20}{header[3]:<24}{header[4]:<26}{header[6]}')  # display the headers
        print('-' * 125)

        # display the details of order_list and specify the spaces between each other
        for cart_id, order_details in order_list.items():
            print(f'{order_details["order_id"]:<19}{cart_id:<19}{order_details["username"]:<20}{order_details["items_ordered"][0]:<24}{float(order_details["total_price (RM)"]):<26.2f}{order_details["status"]}')

            for items in order_details['items_ordered'][1:]:  # for each item in the list of items_ordered
                print(f'{"":<19}{"":<19}{"":<20}{items:<24}{"":<26}{""}')  # display the items line by line and other details that not relevant will be empty
            print('')
        print('-'*125, '\n')

        order_id_to_update = input('Enter Order ID to update order status (or enter "back" to exit):\n>>> ')  # identify the order id to update
        if order_id_to_update == 'back':
            print('\nExiting to Manager Privilege...')
            break  # exit the entire loop

        # check if the input exists in order_list
        for cart_id, order_details in order_list.items():
            if order_details['order_id'] == order_id_to_update:

                while True:
                    update_status = input('\nPlease update the status [payment completed, canceled (or enter "back" to return back)]:\n>>> ')

                    if update_status == 'back':  # return to the previous page
                        break

                    if update_status not in ['payment completed', 'canceled']:
                        print('\n+-------------------------------------------------------+')
                        print('|⚠️ Invalid input. Please enter again. (Case sensitive) |')
                        print('+-------------------------------------------------------+')
                        continue

                    # check if the new status equals to current status
                    current_status = order_details['status'].lower()
                    if update_status.lower() == current_status:
                        print('\n+---------------------------------------------------+')
                        print('|⚠️ This is the current status. Please enter again. |')
                        print('+---------------------------------------------------+')
                        continue

                    order_details['status'] = update_status.title()  # update the order status to new value
                    save_info(order_list)  # save the changes
                    print(f'\nStatus of order ID {order_id_to_update} is updated to "{order_details["status"]}".\n')  # a message to inform users that the status is updated
                    break
                break
        else:
            print('\n+-------------------------------------------+')
            print('|⚠️ Order ID not found. Please enter again. |')
            print('+-------------------------------------------+\n')




#order_management()


