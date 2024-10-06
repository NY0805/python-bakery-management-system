import json
from collections import defaultdict
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


# function that save baker equipment data to 2 different files
def save_info_equipment_details(equipment_details):
    file = open('baker_equipment.txt', 'w')  # open the file to write
    json.dump(equipment_details, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def save_info_equipment_management(equipment_management):
    file = open('notification.txt', 'w')  # open the file to write
    json.dump(equipment_management, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# empty entries validation function
def validation_empty_entries(info):
    if info:
        return True
    else:
        print('❗Please enter something...\n')
        return False


# function that validate digits only
def validation_digit_only(info):
    if info.isdigit():
        return True
    else:
        return False


def validation_alphanum_only(info):
    if info.isalnum():
        return True
    else:
        return False


def validation_date(info, date_format='%d-%m-%Y'):
    try:
        datetime.strptime(info, date_format)
        return True
    except ValueError:
        return False


equipment_list = load_data_from_baker_equipment()

equipment_info = load_data_from_baker_equipment()

equipment_category_groups = defaultdict(list)
for value in equipment_list.values():
    equipment_category_groups[value['category']].append(value)


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

    equipment_info[equipment_name] = {
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

    save_info_equipment_details(equipment_info)


def equipment_management():
    print('\n-------------------------------------------------------')
    print('\t\t\t', '', 'EQUIPMENT MANAGEMENT MENU')
    print('-------------------------------------------------------')
    print('1. Report Malfunction')
    print('2. Report Maintenance Needs')
    print('3. Back to Homepage\n')

    while True:
        equipment_management_type = input('Please choose a service:\n'
                                          '>>> ')
        if validation_empty_entries(equipment_management_type):
            try:
                equipment_management_type = int(equipment_management_type)
                if equipment_management_type in [1, 2, 3]:
                    if equipment_management_type == 1:
                        equipment_malfunction()
                    elif equipment_management_type == 2:
                        equipment_maintenance()
                    elif equipment_management_type == 3:
                        print('Exiting to baker privilege...')
                        break
                else:
                    print('Please enter a valid service type.\n')
            except ValueError:
                print('Please enter a valid number. (Cannot contain spacing.)\n')


def equipment_lists():
    print('\n-------------------------------------------------------')
    print('\t\t\t\t\tEQUIPMENT LIST')
    print('-------------------------------------------------------')
    index = 1
    equipment_index_mapping = {}
    for category, items in equipment_category_groups.items():
        print(f'📍 {category} 📍')
        for equipment in items:
            print(f"{index}. {equipment['equipment_name'].title()}")
            equipment_index_mapping[index] = (category, equipment)
            index += 1
        print('')

    while True:
        selected_index = input('Please select the equipment you want to report. (enter the number of equipment)\n'
                               '>>> ').strip()
        if validation_empty_entries(selected_index):
            try:
                selected_index = int(selected_index)
                if 1 <= selected_index <= len(equipment_index_mapping):
                    break
                else:
                    print('Please enter a valid number based on list given.\n')
            except ValueError:
                print('Please enter a valid number. (Cannot contain spacing.)\n')

    return selected_index, equipment_index_mapping[selected_index]


def equipment_malfunction():
    malfunction_data = load_data_from_manager_notifications()
    print('')
    print('-' * 140)
    print('\nWelcome to the Equipment Malfunction Report page. Please follow the instructions to report any issues.')
    selected_equipment, equipment_info = equipment_lists()
    category, equipment = equipment_info  #unpacking of tuple

    equipment_detail = ['Category', 'Equipment Name', 'Serial Number', 'Manufacturer', 'Model Number', 'Purchase Date',
                        'Purchase Quantity', 'Next Scheduled Maintenance', 'Manufacturer Email', 'Warranty',
                        'Date Of Report', 'Current Condition']

    max_length = 0
    for item in equipment_detail:
        if len(item) > max_length:
            max_length = len(item)

    print('\nBasic details of selected equipment:\n')
    print(f'{equipment_detail[0].ljust(max_length + 4)}: {category.title()}')  # category
    print(f'{equipment_detail[1].ljust(max_length + 4)}: {equipment["equipment_name"].title()}')  # equipment name
    for item, serial_number in enumerate(equipment['serial_number'], start=1):
        print(
            f'{equipment_detail[2]} {str(item).ljust((max_length + 3) - len(equipment_detail[2]))}: {serial_number}')  # serial number
    print(f'{equipment_detail[3].ljust(max_length + 4)}: {equipment["manufacturer"].title()}')  # manufacturer
    print(f'{equipment_detail[4].ljust(max_length + 4)}: {equipment["model_number"]}')  # model number
    print(f'{equipment_detail[5].ljust(max_length + 4)}: {equipment["purchase_date"]}')  # purchase date
    print(f'{equipment_detail[6].ljust(max_length + 4)}: {equipment["purchase_quantity"]}')  # purchase quantity
    print(
        f'{equipment_detail[7].ljust(max_length + 4)}: {equipment["next_scheduled_maintenance"]}')  # next schedule maintenance
    print(f'{equipment_detail[8].ljust(max_length + 4)}: {equipment["manufacturer_email"]}')  # manufacturer email
    print(f'{equipment_detail[9].ljust(max_length + 4)}: {equipment["warranty"]}')  # warranty

    print('')
    print('-' * 140)
    print('\nKindly complete the necessary details to submit a report to manager:\n')
    print(f'1. {equipment_detail[10].ljust(max_length + 2)}: {time.strftime("%d-%m-%Y")}')  # report date
    print(f'2. {equipment_detail[11].ljust(max_length + 2)}: Malfunction')  # current condition

    while True:
        serial_number = input('\nEnter the serial number: ')
        if validation_empty_entries(serial_number):
            if validation_alphanum_only(serial_number):
                if serial_number in equipment['serial_number']:
                    break
                else:
                    print('Please enter a valid serial number based on the list given. (Case sensitive)\n')
            else:
                print('Please enter a valid serial number. (Cannot contain any spacing and special characters.)\n')

    while True:
        malfunction_date = input('Enter the date of malfunction (DD-MM-YYYY): ')
        if validation_empty_entries(malfunction_date):
            if validation_date(malfunction_date):
                break
            else:
                print('Invalid date format. Please enter the date in DD-MM-YYYY format.\n')

    while True:
        last_maintenance_date_str = input('Enter the last maintenance date (DD-MM-YYYY): ')
        if validation_empty_entries(last_maintenance_date_str):
            if validation_date(last_maintenance_date_str):
                # convert last_maintenance_date_str from string to datetime format
                last_maintenance_date = datetime.strptime(last_maintenance_date_str, '%d-%m-%Y')
                # convert malfunction_date from string to datetime format
                malfunction_date_new = datetime.strptime(malfunction_date, '%d-%m-%Y')
                if last_maintenance_date <= malfunction_date_new:
                    break
                else:
                    print('Please enter a valid last maintenance date. Cannot greater than malfunction date.')
            else:
                print('Invalid date format. Please enter the date in DD-MM-YYYY format.\n')

    while True:
        description = input('Enter a clear description of the malfunction: ')
        if validation_empty_entries(description):
            break

    while True:
        confirmation = input('\nConfirm submission of malfunction report to manager? (y=yes, n=no)\n'
                             '>>> ').lower().strip()
        if validation_empty_entries(confirmation):
            if confirmation == 'y':
                malfunction_data[serial_number] = {
                    'category': category,
                    'equipment_name': equipment['equipment_name'],
                    'serial_number': serial_number,
                    'model_number': equipment['model_number'],
                    'manufacturer_email': equipment['manufacturer_email'],
                    'warranty': equipment['warranty'],
                    'report_date': time.strftime("%d-%m-%Y"),
                    'current_condition': 'malfunction',
                    'malfunction_date': malfunction_date,
                    'last_maintenance_date': last_maintenance_date_str,
                    'description': description
                }

                save_info_equipment_management(malfunction_data)
                print('\nMalfunction report has been submitted. Thank you for reporting!\n')
                break
            elif confirmation == 'n':
                print('Report submission has been canceled.\n')
                break
            else:
                print("Please enter 'y' or 'n'.\n")

    while True:
        report_more = input('Continue reporting? (y=yes, n=no)\n'
                            '>>> ').lower().strip()
        if validation_empty_entries(report_more):
            if report_more == 'y':
                equipment_malfunction()
                break
            elif report_more == 'n':
                print('\nExit the maintenance needs report page. Proceeding to equipment management menu......')
                equipment_management()
                break
            else:
                print("Please enter 'y' or 'n'.\n")


def equipment_maintenance():
    maintenance_data = load_data_from_manager_notifications()
    print('')
    print('-' * 140)
    print('\nWelcome to the Equipment Maintenance Report page. Please follow the instructions to report any issues.\n')
    selected_equipment, equipment_info = equipment_lists()
    category, equipment = equipment_info  # unpacking of tuple

    equipment_detail = ['Category', 'Equipment Name', 'Serial Number', 'Manufacturer', 'Model Number', 'Purchase Date',
                        'Purchase Quantity', 'Next Scheduled Maintenance', 'Manufacturer Email', 'Warranty',
                        'Date Of Report', 'Current Condition']

    max_length = 0
    for item in equipment_detail:
        if len(item) > max_length:
            max_length = len(item)

    print('\nBasic details of selected equipment:\n')
    print(f'{equipment_detail[0].ljust(max_length + 4)}: {category.title()}')  # category
    print(f'{equipment_detail[1].ljust(max_length + 4)}: {equipment["equipment_name"].title()}')  # equipment name
    for item, serial_number in enumerate(equipment['serial_number'], start=1):
        print(
            f'{equipment_detail[2]} {str(item).ljust((max_length + 3) - len(equipment_detail[2]))}: {serial_number}')  # serial number
    print(f'{equipment_detail[3].ljust(max_length + 4)}: {equipment["manufacturer"].title()}')  # manufacturer
    print(f'{equipment_detail[4].ljust(max_length + 4)}: {equipment["model_number"]}')  # model number
    print(f'{equipment_detail[5].ljust(max_length + 4)}: {equipment["purchase_date"]}')  # purchase date
    print(f'{equipment_detail[6].ljust(max_length + 4)}: {equipment["purchase_quantity"]}')  # purchase quantity
    print(
        f'{equipment_detail[7].ljust(max_length + 4)}: {equipment["next_scheduled_maintenance"]}')  # next schedule maintenance
    print(f'{equipment_detail[8].ljust(max_length + 4)}: {equipment["manufacturer_email"]}')  # manufacturer email
    print(f'{equipment_detail[9].ljust(max_length + 4)}: {equipment["warranty"]}')  # warranty

    print('')
    print('-' * 140)
    print('\nKindly complete the necessary details to submit a report to manager:\n')
    print(f'1. {equipment_detail[10].ljust(max_length + 2)}: {time.strftime("%d-%m-%Y")}')  # report date
    print(f'2. {equipment_detail[11].ljust(max_length + 2)}: Maintenance Needed\n')  # current condition

    while True:
        serial_number = input('Enter the serial number: ')
        if validation_empty_entries(serial_number):
            if validation_alphanum_only(serial_number):
                if serial_number in equipment['serial_number']:
                    break
                else:
                    print('Please enter a valid serial number based on the list given. (Case sensitive)\n')
            else:
                print('Please enter a valid serial number. (Cannot contain any spacing and special characters.)\n')

    while True:
        maintenance_needed_date = input('Enter the date of incident (DD-MM-YYYY): ')
        if validation_empty_entries(maintenance_needed_date):
            # maintenance_needed_date_new = datetime.strptime(maintenance_needed_date, '%d-%m-%Y')
            if validation_date(maintenance_needed_date):
                # if maintenance_needed_date_new < systemdate
                break
            else:
                print('Invalid date format. Please enter the date in DD-MM-YYYY format.\n')

    while True:
        last_maintenance_date_str = input('Enter the last maintenance date (DD-MM-YYYY): ')
        if validation_empty_entries(last_maintenance_date_str):
            if validation_date(last_maintenance_date_str):
                # convert last_maintenance_date_str from string to datetime format
                last_maintenance_date = datetime.strptime(last_maintenance_date_str, '%d-%m-%Y')
                # convert malfunction_date from string to datetime format
                maintenance_needed_date_new = datetime.strptime(maintenance_needed_date, '%d-%m-%Y')
                if last_maintenance_date <= maintenance_needed_date_new:
                    break
                else:
                    print('Please enter a valid last maintenance date. Cannot greater than malfunction date.')
            else:
                print('Invalid date format. Please enter the date in DD-MM-YYYY format.\n')

    while True:
        severity = input('Enter the severity of the issue (Choose between: urgent, high, medium, low): ').lower().strip()
        if validation_empty_entries(severity):
            if severity.isalpha():
                if severity in ['urgent', 'high', 'medium', 'low']:
                    break
                else:
                    print('Please input the severity level based on the given options.\n')
            else:
                print('Invalid input. (Cannot contain any spacings, digits and special characters.)\n')

    while True:
        description = input('Enter a clear description of the maintenance issue: ')
        if validation_empty_entries(description):
            break

    while True:
        confirmation = input('\nConfirm submission of malfunction report to manager? (y=yes, n=no)\n'
                             '>>> ').lower().strip()
        if validation_empty_entries(confirmation):
            if confirmation == 'y':
                maintenance_data[serial_number] = {
                    'category': category,
                    'equipment_name': equipment['equipment_name'],
                    'serial_number': serial_number,
                    'model_number': equipment['model_number'],
                    'manufacturer_email': equipment['manufacturer_email'],
                    'warranty': equipment['warranty'],
                    'report_date': time.strftime("%d-%m-%Y"),
                    'current_condition': 'maintenance needed',
                    'severity': severity,
                    'maintenance_needed_date': maintenance_needed_date,
                    'last_maintenance_date': last_maintenance_date_str,
                    'next_scheduled_maintenance': equipment['next_scheduled_maintenance'],
                    'description': description
                }

                save_info_equipment_management(maintenance_data)
                print('\nMaintenance needs report has been submitted. Thank you for reporting!\n')
                break
            elif confirmation == 'n':
                print('Report submission has been canceled.\n')
                break
            else:
                print("Please enter 'y' or 'n'.\n")

    while True:
        report_more = input('Continue reporting? (y=yes, n=no)\n'
                            '>>> ').lower().strip()
        if validation_empty_entries(report_more):
            if report_more == 'y':
                equipment_maintenance()
                break
            elif report_more == 'n':
                print('\nExit the malfunction report page. Proceeding to equipment management menu......')
                equipment_management()
                break
            else:
                print("Please enter 'y' or 'n'.\n")


equipment_management()