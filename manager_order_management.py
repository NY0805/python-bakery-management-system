import json


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


def save_info(order_list):
    file = open('customer_order_list.txt', 'w')  # open the file to write
    json.dump(order_list, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


order_list = load_data_from_customer_order_list()


def order_management():
    while True:
        print('\n', '\t'*13, 'ORDER DETAILS')
        print('-' * 125)
        header = ['Cart Id']
        for value in order_list.values():
            for sub_key, sub_value in value.items():
                header.append(sub_key.title().replace('_', ' '))
            break

        print(f'{header[0]:<19}{header[1]:<19}{header[2]:<20}{header[3]:<24}{header[4]:<26}{header[5]}')
        print('-' * 125)

        for cart_id, order_details in order_list.items():
            print(f'{cart_id:<19}{order_details["order_id"]:<19}{order_details["username"]:<20}{order_details["items_ordered"][0]:<24}{order_details["total_price (RM)"]:<26.2f}{order_details["status"]}')

            for items in order_details['items_ordered'][1:]:
                print(f'{"":<19}{"":<19}{"":<20}{items:<24}{"":<26}{""}')
            print('')
        print('-'*125, '\n')

        order_id_to_update = input('Enter Order ID to update order status (or enter "cancel" to exit):\n>>> ')
        if order_id_to_update == 'cancel':
            print('\nExiting to Manager Privilege...')
            break  # Exit the entire loop

            # Check if the order_id_to_update exists in order_list
        for cart_id, order_details in order_list.items():
            if order_details['order_id'] == order_id_to_update:
                # Proceed to update the order status
                while True:
                    update_status = input('\nPlease update the status [preparing, payment complete, canceled (or enter "back" to return back)]:\n>>> ')

                    if update_status == 'back':
                        break  # Exit the inner status update loop

                    # Validate status input
                    if update_status not in ['preparing', 'payment complete', 'canceled']:
                        print('\n+-------------------------------------------------------+')
                        print('|⚠️ Invalid input. Please enter again. (Case sensitive) |')
                        print('+-------------------------------------------------------+')
                        continue  # Continue to the next iteration for valid input

                    # Check if the new status is different from the current status
                    current_status = order_details['status'].lower()
                    if update_status.lower() == current_status:
                        print('\n+---------------------------------------------------+')
                        print('|⚠️ This is the current status. Please enter again. |')
                        print('+---------------------------------------------------+')
                        continue  # Continue for a different input

                    # Update the status and save the information
                    order_details['status'] = update_status.title()  # Set the new status
                    save_info(order_list)  # Assuming save_info is a function to save the order list
                    print(f'\nStatus of order ID {order_id_to_update} is updated to "{order_details["status"]}".\n')
                    break  # Exit the inner status update loop
                break  # Exit the for-loop when the order ID is found
        else:
            # If the loop completes without finding the order_id, show a not found message
            print('\n+-------------------------------------------+')
            print('|⚠️ Order ID not found. Please enter again. |')
            print('+-------------------------------------------+\n')




order_management()


