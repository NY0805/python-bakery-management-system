import json
import random
from datetime import datetime
import time


# loads baker equipment data from the file
def load_data_from_baker_equipment():
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


# loads manager notification data from the file
def load_data_from_manager_notifications():
    try:
        file = open('notification.txt', 'r')  # open the file and read
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


# function that save new added equipment data to baker equipment file
def save_info_equipment_details(equipment_details):
    file = open('baker_equipment.txt', 'w')  # open the file to write
    json.dump(equipment_details, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# function that save malfunction and maintenance report to manager notification file
def save_info_equipment_management(equipment_management):
    file = open('notification.txt', 'w')  # open the file to write
    json.dump(equipment_management, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# validate empty entries
def validation_empty_entries(info):
    if info:
        return True  # if user input have value, return True
    else:
        print('\n❗Please enter something...\n')
        return False  # if user input does not have value, print error message and return false


# validate whether user's input is in date format
def validation_date(info, date_format='%d-%m-%Y'):
    try:
        datetime.strptime(info, date_format)
        return True  # if user input is in date format, return True
    except ValueError:
        return False  # if user input not in date format, return False


# function to print message with border on top and bottom
def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


# load equipment data from baker equipment file
equipment_list = load_data_from_baker_equipment()

equipment_category_groups = {}  # initialize an empty dictionary to group equipment items by category
for value in equipment_list.values():  # loop through equipment data and get the category for current equipment
    equipment_category = value['category']

    if equipment_category not in equipment_category_groups:  # if the category does not exist as a key in the dictionary
        equipment_category_groups[equipment_category] = []  # create a new empty list with the category as the key

    # if the category already exist as a key, append the current equipment details
    equipment_category_groups[equipment_category].append(value)


def enter_equipment():
    category = input('enter category: ')
    equipment_name = input('enter name: ')
    purchase_quantity = int(input('enter purchase quantity: '))
    serial_numbers = []
    for i in range(purchase_quantity):
        equipment_serial_number = input(f'enter serial number {i + 1}: ')  # enter based on purchase quantity
        serial_numbers.append(equipment_serial_number)
    manufacturer = input('enter manufacturer: ')
    model_number = input('enter model number: ')
    purchase_date = input('enter purchase date: ')
    next_scheduled_maintenance = input('enter next scheduled maintenance: ')
    manufacturer_email = input('enter manufacturer email: ')
    warranty = input('enter warranty: ')

    equipment_list[equipment_name] = {
        'category': category,
        'equipment_name': equipment_name,
        'purchase_quantity': purchase_quantity,
        'serial_number': serial_numbers,
        'manufacturer': manufacturer,
        'model_number': model_number,
        'purchase_date': purchase_date,
        'next_scheduled_maintenance': next_scheduled_maintenance,
        'manufacturer_email': manufacturer_email,
        'warranty': warranty
    }

    save_info_equipment_details(equipment_list)


# define function that let user to select equipment management option
def equipment_management():
    # display the equipment management option
    print('')
    printed_centered('EQUIPMENT MANAGEMENT MENU')
    print('1. Report Malfunction')
    print('2. Report Maintenance Needs')
    print('3. Back to Homepage\n')

    # loop until a valid choice is selected or user choose to exit
    while True:
        equipment_management_type = input('Please choose a service:\n'
                                          '>>> ').strip()
        if validation_empty_entries(equipment_management_type):
            if equipment_management_type == '1':
                equipment_malfunction()
            elif equipment_management_type == '2':
                equipment_maintenance()
            elif equipment_management_type == '3':
                print('Exiting to baker privilege...')
                break
            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Please enter a valid service type. |')
                print('+--------------------------------------+\n')


# define function that let user to selected which equipment to report
def equipment_lists():
    print('')
    printed_centered('EQUIPMENT LIST')
    index = 1  # initialize index for each equipment
    equipment_index_mapping = {}  # create a dictionary to map equipment index with its category and details

    # loop through each equipment category and display equipment names with corresponding index
    for category, items in equipment_category_groups.items():
        print(f'📍 {category} 📍')
        for equipment in items:
            print(f"{index}. {equipment['equipment_name'].title()}")
            equipment_index_mapping[index] = (category, equipment)  # map index to category and equipment details
            index += 1
        print('')

    while True:
        # get user selected equipment
        selected_index = input('Please select the equipment you want to report. (enter the number of equipment)\n'
                               '>>> ').strip()
        if validation_empty_entries(selected_index):
            try:
                selected_index = int(selected_index)  # if input is a digit and fall within valid range
                if 1 <= selected_index <= len(equipment_index_mapping):
                    break  # exit loop when valid selection is made
                else:
                    # if input is invalid, prompt user to enter again
                    print('\n+----------------------------------------------------+')
                    print('|⚠️ Please enter a valid number based on list given. |')
                    print('+----------------------------------------------------+\n')
            except ValueError:
                print('\n+----------------------------------------------------------+')
                print('|⚠️ Please enter a valid number. (Cannot contain spacing.) |')
                print('+----------------------------------------------------------+\n')

    return selected_index, equipment_index_mapping[selected_index]


# define function that let user to make malfunction equipment report
def equipment_malfunction():
    malfunction_data = load_data_from_manager_notifications()  # load previous malfunction report from file
    print('')
    print('-' * 140)
    print('\nWelcome to the Equipment Malfunction Report page. Please follow the instructions to report any issues.')
    selected_equipment, equipment_info = equipment_lists()  # get user selected equipment and its information
    category, equipment = equipment_info  # unpack the tuple to get category and other details

    # display the details of selected equipment
    max_length = len('Next Scheduled Maintenance')

    print('\nBasic details of selected equipment:\n')
    print(f'{"Category":<28}: {category.title()}')  # category
    print(f'{"Equipment Name":<28}: {equipment["equipment_name"].title()}')  # equipment name
    index = 1
    for serial_number in equipment['serial_number']:
        print(f'Serial Number {str(index).ljust((max_length + 1) - len("Serial Number"))}: {serial_number}')
        index += 1
    print(f'{"Manufacturer":<28}: {equipment["manufacturer"].title()}')  # manufacturer
    print(f'{"Model Number":<28}: {equipment["model_number"]}')  # model number
    print(f'{"Purchase Date":<28}: {equipment["purchase_date"]}')  # purchase date
    print(f'{"Purchase Quantity":<28}: {equipment["purchase_quantity"]}')  # purchase quantity
    print(f'{"Next Scheduled Maintenance":<28}: {equipment["next_scheduled_maintenance"]}')  # next schedule maintenance
    print(f'{"Manufacturer Email":<28}: {equipment["manufacturer_email"]}')  # manufacturer email
    print(f'{"Warranty":<28}: {equipment["warranty"]}')  # warranty

    print('')
    print('-' * 140)
    print('\nKindly complete the necessary details to submit a report to manager:\n')
    print(f'1. {"Date of Report":<20}: {time.strftime("%d-%m-%Y")}')  # report date
    print(f'2. {"Current Condition":<20}: Malfunction')  # current condition
    print('')

    # prompt user to enter specific serial number of equipment that want to report
    while True:
        serial_number = input('Enter the serial number: ').strip()
        if validation_empty_entries(serial_number):
            if serial_number.isalnum():
                if serial_number in equipment['serial_number']:  # ensure the serial number exist in selected equipment
                    break
                else:
                    print('\n+--------------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid serial number based on the list given. (Case sensitive) |')
                    print('+--------------------------------------------------------------------------------+\n')
            else:
                print(
                    '\n+--------------------------------------------------------------------------------------------+')
                print('|⚠️ Please enter a valid serial number. (Cannot contain any spacing and special characters.) |')
                print(
                    '+--------------------------------------------------------------------------------------------+\n')

    # prompt user to enter malfunction date and ensure it does not greater that system date
    while True:
        malfunction_date = input('Enter the date of malfunction (DD-MM-YYYY): ')
        if validation_empty_entries(malfunction_date):
            if validation_date(malfunction_date):
                malfunction_date = datetime.strptime(malfunction_date, '%d-%m-%Y')
                if malfunction_date <= datetime.now():
                    break
                else:
                    print('\n+-------------------------------------------------------------------------------+')
                    print(f'|⚠️ Please enter a valid malfunction date. Cannot greater than date of report. |')
                    print('+-------------------------------------------------------------------------------+\n')
            else:
                print('\n+--------------------------------------------------------------------+')
                print('|⚠️ Invalid date format. Please enter the date in DD-MM-YYYY format. |')
                print('+--------------------------------------------------------------------+\n')

    # prompt user to enter last maintenance date and ensure it does not greater than malfunction date
    while True:
        last_maintenance_date_str = input('Enter the last maintenance date (DD-MM-YYYY): ')
        if validation_empty_entries(last_maintenance_date_str):
            if validation_date(last_maintenance_date_str):
                # convert last_maintenance_date_str from string to datetime format
                last_maintenance_date = datetime.strptime(last_maintenance_date_str, '%d-%m-%Y')
                # convert malfunction_date from string to datetime format
                if last_maintenance_date <= malfunction_date:
                    break
                else:
                    print('\n+-------------------------------------------------------------------------------------+')
                    print('|⚠️ Please enter a valid last maintenance date. Cannot greater than malfunction date. |')
                    print('+-------------------------------------------------------------------------------------+\n')
            else:
                print('\n+--------------------------------------------------------------------+')
                print('|⚠️ Invalid date format. Please enter the date in DD-MM-YYYY format. |')
                print('+--------------------------------------------------------------------+\n')

    # prompt user to enter description that explain about the malfunction
    while True:
        description = input('Enter a clear description of the malfunction: ')
        if validation_empty_entries(description):
            break

    # confirm submission of malfunction report
    while True:
        confirmation = input('\nConfirm submission of malfunction report to manager? (y=yes, n=no)\n'
                             '>>> ').lower().strip()
        if validation_empty_entries(confirmation):
            if confirmation == 'y':  # if user choose to submit report
                previous_number = None
                while True:
                    try:
                        # Generate a random number between 1000 and 9999
                        report_number = random.randint(1000, 9999)
                        # Try checking for duplicates in 'report_number'
                        if report_number in malfunction_data['report_number']:
                            continue  # If duplicate found, generate again
                        else:
                            previous_number = report_number
                            break  # Exit the loop when a unique number is found
                    except KeyError:
                        # Handle the case where 'report_number' key does not exist
                        print('\nGenerating report number...')
                        report_number = random.randint(1000, 9999)
                        previous_number = report_number  # Assign the generated number
                        break  # Exit loop since we don't need to check for duplicates in this case

                # save the malfunction report to manager notification file
                malfunction_data[serial_number] = {
                    'report_number': f'REPORT-{previous_number}',
                    'category': category,
                    'equipment_name': equipment['equipment_name'],
                    'serial_number': serial_number,
                    'model_number': equipment['model_number'],
                    'manufacturer_email': equipment['manufacturer_email'],
                    'warranty': equipment['warranty'],
                    'report_date': time.strftime("%d-%m-%Y"),
                    'current_condition': 'malfunction',
                    'malfunction_date': malfunction_date.strftime("%d-%m-%Y"),
                    'last_maintenance_date': last_maintenance_date_str,
                    'description': description
                }

                save_info_equipment_management(malfunction_data)
                print('\nMalfunction report has been submitted. Thank you for reporting!\n')
                break
            elif confirmation == 'n':  # if user choose to not submit the report
                print('Report submission has been canceled.\n')
                break  # exit the loop
            else:
                # print error message when input is invalid
                print('\n+----------------------------+')
                print("|⚠️ Please enter 'y' or 'n'. |")
                print('+----------------------------+\n')

    # prompt user whether to submit another malfunction report
    while True:
        report_more = input('Continue reporting? (y=yes, n=no)\n'
                            '>>> ').lower().strip()
        if validation_empty_entries(report_more):
            if report_more == 'y':  # if yes, recursively call function
                equipment_malfunction()
                break
            elif report_more == 'n':  # if no, return to equipment management page
                print('\nExit the malfunction report page. Proceeding to equipment management menu......')
                equipment_management()
                break
            else:
                print('\n+----------------------------+')
                print("|⚠️ Please enter 'y' or 'n'. |")
                print('+----------------------------+\n')


# define function that let user make maintenance report
def equipment_maintenance():
    maintenance_data = load_data_from_manager_notifications()  # load previous maintenance report from manager notification file

    print('')
    print('-' * 140)
    print('\nWelcome to the Equipment Maintenance Report page. Please follow the instructions to report any issues.')
    selected_equipment, equipment_info = equipment_lists()  # get user selected equipment and its information
    category, equipment = equipment_info  # unpack the tuple to get category and other details

    # display the details of selected equipment
    max_length = len('Next Scheduled Maintenance')

    print('\nBasic details of selected equipment:\n')
    print(f'{"Category":<28}: {category.title()}')  # category
    print(f'{"Equipment Name":<28}: {equipment["equipment_name"].title()}')  # equipment name
    index = 1
    for serial_number in equipment['serial_number']:
        print(f'Serial Number {str(index).ljust((max_length + 1) - len("Serial Number"))}: {serial_number}')
        index += 1
    print(f'{"Manufacturer":<28}: {equipment["manufacturer"].title()}')  # manufacturer
    print(f'{"Model Number":<28}: {equipment["model_number"]}')  # model number
    print(f'{"Purchase Date":<28}: {equipment["purchase_date"]}')  # purchase date
    print(f'{"Purchase Quantity":<28}: {equipment["purchase_quantity"]}')  # purchase quantity
    print(f'{"Next Scheduled Maintenance":<28}: {equipment["next_scheduled_maintenance"]}')  # next schedule maintenance
    print(f'{"Manufacturer Email":<28}: {equipment["manufacturer_email"]}')  # manufacturer email
    print(f'{"Warranty":<28}: {equipment["warranty"]}')  # warranty

    print('')
    print('-' * 140)
    print('\nKindly complete the necessary details to submit a report to manager:\n')
    print(f'1. {"Date of Report":<20}: {time.strftime("%d-%m-%Y")}')  # report date
    print(f'2. {"Current Condition":<20}: Maintenance Needed')  # current condition
    print('')

    # prompt user to enter specific serial number of equipment that want to report
    while True:
        serial_number = input('Enter the serial number: ')
        if validation_empty_entries(serial_number):
            if serial_number.isalnum():
                if serial_number in equipment['serial_number']:  # ensure the serial number exist in selected equipment
                    break
                else:
                    print('\n+--------------------------------------------------------------------------------+')
                    print("|⚠️ Please enter a valid serial number based on the list given. (Case sensitive) |")
                    print('+--------------------------------------------------------------------------------+\n')
            else:
                print(
                    '\n+--------------------------------------------------------------------------------------------+')
                print("|⚠️ Please enter a valid serial number. (Cannot contain any spacing and special characters.) |")
                print(
                    '+--------------------------------------------------------------------------------------------+\n')

    # prompt user to enter maintenance date and ensure it does not greater that system date
    while True:
        maintenance_needed_date = input('Enter the date of incident (DD-MM-YYYY): ')
        if validation_empty_entries(maintenance_needed_date):
            maintenance_needed_date = datetime.strptime(maintenance_needed_date, '%d-%m-%Y')
            if maintenance_needed_date <= datetime.now():
                break
            else:
                print('\n+--------------------------------------------------------------------------------------+')
                print(f'|⚠️ Please enter a valid maintenance needed date. Cannot greater than date of report. |')
                print('+--------------------------------------------------------------------------------------+\n')
        else:
            print('\n+---------------------------------------------------------------------+')
            print(f'|⚠️ Invalid date format. Please enter the date in DD-MM-YYYY format. |')
            print('+---------------------------------------------------------------------+\n')

    # prompt user to enter last maintenance date and ensure it does not greater than maintenance date
    while True:
        last_maintenance_date_str = input('Enter the last maintenance date (DD-MM-YYYY): ')
        if validation_empty_entries(last_maintenance_date_str):
            if validation_date(last_maintenance_date_str):
                # convert last_maintenance_date_str from string to datetime format
                last_maintenance_date = datetime.strptime(last_maintenance_date_str, '%d-%m-%Y')
                # convert maintenance_date from string to datetime format
                if last_maintenance_date <= maintenance_needed_date:
                    break
                else:
                    print('\n+--------------------------------------------------------------------------------------+')
                    print(f'|⚠️ Please enter a valid last maintenance date. Cannot greater than malfunction date. |')
                    print('+--------------------------------------------------------------------------------------+\n')
            else:
                print('\n+---------------------------------------------------------------------+')
                print(f'|⚠️ Invalid date format. Please enter the date in DD-MM-YYYY format. |')
                print('+---------------------------------------------------------------------+\n')

    # prompt user to enter the severity of selected equipment
    while True:
        severity = input(
            'Enter the severity of the issue (Choose between: urgent, high, medium, low): ').lower().strip()
        if validation_empty_entries(severity):
            if severity.isalpha():
                if severity in ['urgent', 'high', 'medium', 'low']:
                    break
                else:
                    print('\n+----------------------------------------------------------------+')
                    print(f'|⚠️ Please input the severity level based on the given options. |')
                    print('+----------------------------------------------------------------+\n')
            else:
                print('\n+---------------------------------------------------------------------------------+')
                print(f'|⚠️ Invalid input. (Cannot contain any spacings, digits and special characters.) |')
                print('+---------------------------------------------------------------------------------+\n')

    # prompt user to enter description that explain about the maintenance issue
    while True:
        description = input('Enter a clear description of the maintenance issue: ')
        if validation_empty_entries(description):
            break

    # confirm submission of maintenance report
    while True:
        confirmation = input('\nConfirm submission of maintenance report to manager? (y=yes, n=no)\n'
                             '>>> ').lower().strip()
        if validation_empty_entries(confirmation):
            if confirmation == 'y':  # if user choose to submit report
                previous_number = None
                while True:
                    try:
                        # Generate a random number between 1000 and 9999
                        report_number = random.randint(1000, 9999)
                        # Try checking for duplicates in 'report_number'
                        if report_number in maintenance_data['report_number']:
                            continue  # If duplicate found, generate again
                        else:
                            previous_number = report_number
                            break  # Exit the loop when a unique number is found
                    except KeyError:
                        # Handle the case where 'report_number' key does not exist
                        print('\nGenerating report number...')
                        report_number = random.randint(1000, 9999)
                        previous_number = report_number  # Assign the generated number
                        break  # Exit loop since we don't need to check for duplicates in this case

                # save the maintenance report to manager notification file
                maintenance_data[serial_number] = {
                    'report_number': f'REPORT-{previous_number}',
                    'category': category,
                    'equipment_name': equipment['equipment_name'],
                    'serial_number': serial_number,
                    'model_number': equipment['model_number'],
                    'manufacturer_email': equipment['manufacturer_email'],
                    'warranty': equipment['warranty'],
                    'report_date': time.strftime("%d-%m-%Y"),
                    'current_condition': 'maintenance needed',
                    'severity': severity,
                    'maintenance_needed_date': maintenance_needed_date.strftime("%d-%m-%Y"),
                    'last_maintenance_date': last_maintenance_date_str,
                    'next_scheduled_maintenance': equipment['next_scheduled_maintenance'],
                    'description': description
                }

                save_info_equipment_management(maintenance_data)
                print('\nMaintenance needs report has been submitted. Thank you for reporting!\n')
                break
            elif confirmation == 'n':  # if user choose to not submit the report
                print('Report submission has been canceled.\n')
                break  # exit the loop
            else:
                print('\n+----------------------------+')
                print("|⚠️ Please enter 'y' or 'n'. |")
                print('+----------------------------+\n')

    # prompt user whether to submit another maintenance report
    while True:
        report_more = input('Continue reporting? (y=yes, n=no)\n'
                            '>>> ').lower().strip()
        if validation_empty_entries(report_more):
            if report_more == 'y':
                equipment_maintenance()  # if yes, recursively call function
                break
            elif report_more == 'n':
                print('\nExit the maintenance report page. Proceeding to equipment management menu......')
                equipment_management()  # if no, return to the equipment management page
                break
            else:
                print('\n+----------------------------+')
                print("|⚠️ Please enter 'y' or 'n'. |")
                print('+----------------------------+\n')

#equipment_management()
