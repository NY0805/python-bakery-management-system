import json
from collections import defaultdict


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


def load_data_from_manager_notification():
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


def save_info_equipment(equipment):
    file = open('baker_equipment.txt', 'w')  # open the file to write
    json.dump(equipment, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def save_info_equipment_management(equipment_management):
    file = open('baker_equipment.txt', 'w')  # open the file to write
    json.dump(equipment_management, file,
              indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


def validation_empty_entries(info):
    if info:
        return True
    else:
        print('\n❗Please enter something...\n')
        return False


def validation_digit_only(info):
    if info.isdigit():
        return True
    else:
        return False


manager_notification = load_data_from_manager_notification()
equipment_list = load_data_from_baker_equipment()

equipment_category_groups = defaultdict(list)
for value in equipment_list.values():
    equipment_category_groups[value['category']].append(value)

equipment_name = input('enter name: ')
equipment_serial_number = input('enter serial number: ') # enter based on purchase quantity
category = input('enter category: ')
manufacturer = input('enter manufacturer: ')
model_number = input('enter model number: ')
purchase_date = input('enter purchase date: ')
purchase_quantity = input('enter purchase quantity: ')
condition = input('enter condition: ')
next_scheduled_maintenance = input('enter next scheduled maintenance: ')


def equipment_management():
    print('\n-------------------------------------------------------')
    print('\t\t\t', '', 'EQUIPMENT MANAGEMENT MENU')
    print('-------------------------------------------------------\n')
    print('1. Report Malfunction')
    print('2. Report Maintenance Needs')
    print('3. Back to Homepage\n')

    while True:
        try:
            equipment_management_type = int(input('Please choose a service:\n'
                                                  '>>> '))
            if validation_empty_entries(equipment_management_type):
                if equipment_management_type in [1, 2, 3]:
                    if equipment_management_type == 1:
                        pass
                    elif equipment_management_type == 2:
                        pass
                    elif equipment_management_type == 3:
                        print('Exiting to baker privilege...')
                        break
                else:
                    print('Please enter a valid service type.\n')
        except ValueError:
            print('Please enter a valid number. (Cannot contain spacing.)\n')


def equipment_list():
    print('Here are the equipment list:\n')
    index = 1
    total_equipment = 0
    for category, items in equipment_category_groups.items():
        print(f'📍 {category} 📍')
        for equipment in items:
            print(f"{index}. {equipment.title()}")
            index += 1
            total_equipment += 1
        print('')

    while True:
        try:
            selected_equipment = int(input('Please select the equipment you want to report. (enter the number of equipment)\n'
                                           '>>> '))
            if validation_empty_entries(selected_equipment):
                if 1 <= selected_equipment <= total_equipment:
                    break
                else:
                    print('Please enter a valid number based on list given.\n')
        except ValueError:
            print('Please enter a valid number. (Cannot contain spacing.)\n')

    return selected_equipment



def equipment_malfunction():
    equ
    print('Please fill out the form to ')
