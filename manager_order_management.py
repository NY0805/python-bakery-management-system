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
        print('\n\t\t\t\t\t\t\t\t\t\tORDER DETAILS')
        print('-' * 105)
        header = ['Order ID']
        for value in order_list.values():
            for sub_key, sub_value in value.items():
                header.append(sub_key.title().replace('_', ' '))
            break

        print(f'{header[0]:<20}{header[1]:<20}{header[2]:<25}{header[3]:<22}{header[4]}')
        print('-' * 105)

        for order_id, order_details in order_list.items():
            print(f'{order_id:<20}{order_details["username"]:<20}{order_details["items_ordered"][0]:<25}{order_details["total_price"]:<22}{order_details["status"]}')

            for items in order_details['items_ordered'][1:]:
                print(f'{"":<20}{"":<20}{items:<25}{"":<22}{""}')
            print('')
        print('-'*105, '\n')

        while True:
            order_id_to_update = input('Enter Order ID to update order status (or enter "cancel" to exit):\n>>> ')
            if order_id_to_update not in order_list.keys() and order_id_to_update != 'cancel':
                print('\n+-------------------------------------------+')
                print('|⚠️ Order id not found. Please enter again. |')
                print('+-------------------------------------------+\n')
            elif order_id_to_update == 'cancel':
                print('\nExiting to Manager Privilege......')
                return False
            else:
                break

        while True:
            update_status = input('\nPlease update the status [processing, delivered, payment complete ("cancel" to return back)]:\n>>> ')
            if update_status not in ['processing', 'delivered', 'payment complete'] and update_status != 'cancel':
                print('\n+-------------------------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. (Case sensitive) |')
                print('+-------------------------------------------------------+')

            elif update_status == 'cancel':
                break

            else:
                order_details = order_list[order_id_to_update]
                status = order_details['status']
                if update_status == status.lower():
                    print('\n+---------------------------------------------------+')
                    print('|⚠️ This is the current status. Please enter again. |')
                    print('+---------------------------------------------------+')

                else:
                    status = update_status.title()
                    save_info(order_list)
                    print(f'\nStatus of order id {order_id_to_update} is updated to "{status}".\n')
                    break

#order_management()


