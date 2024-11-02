import json
import textwrap
import time
from datetime import datetime


# Define the function that loads notification data from the file
def load_data_from_notification():
    try:
        file = open('notification.txt', 'r')  # open the file and read
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


# Define the function that loads equipment report keeping data from the file
def load_data_from_equipment_report_keeping():
    try:
        file = open('manager_equipment_report_keeping.txt', 'r')  # open the file and read
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


# Define the function that loads equipment data from the file
def load_data_from_baker_equipment():
    try:
        file = open('baker_equipment.txt', 'r')  # open the file and read
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


# Define the function that saves notification data to the file
def save_info(notice):
    file = open('notification.txt', 'w')  # open the file to write
    json.dump(notice, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# Define the function that saves notification data to the file
def save_info_report(equipment_report_keeping):
    file = open('manager_equipment_report_keeping.txt', 'w')  # open the file to write
    json.dump(equipment_report_keeping, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# group for malfunction equipment
def malfunction_data_group(malfunction_data):
    return (
        f"📍 {malfunction_data['equipment_name'].title()} 📍\n"
        f"Category: {malfunction_data['category'].title()}\n"
        f"Serial number: {malfunction_data['serial_number']}\n"
        f"Model number: {malfunction_data['model_number']}\n"
        f"Report date: {malfunction_data['report_date']}\n"
        f"Current condition: {malfunction_data['current_condition']}\n"
        f"Malfunction date: {malfunction_data['malfunction_date']}\n"
        f"Last maintenance date: {malfunction_data['last_maintenance_date']}\n"
        f"Description: {malfunction_data['description']}"
    )


# group for equipments that need maintenance
def maintenance_data_group(maintenance_data):
    return (
        f"📍 {maintenance_data['equipment_name'].title()} 📍\n"
        f"Category: {maintenance_data['category'].title()}\n"
        f"Serial number: {maintenance_data['serial_number']}\n"
        f"Model number: {maintenance_data['model_number']}\n"
        f"Manufacturer email: {maintenance_data['manufacturer_email']}\n"
        f"Warranty: {maintenance_data['warranty']}\n"
        f"Report date: {maintenance_data['report_date']}\n"
        f"Current condition: {maintenance_data['current_condition']}\n"
        f"Severity: {maintenance_data['severity']}\n"
        f"Maintenance needed date: {maintenance_data['maintenance_needed_date']}\n"
        f"Last maintenance date: {maintenance_data['last_maintenance_date']}\n"
        f"Next scheduled maintenance: {maintenance_data['next_scheduled_maintenance']}\n"
        f"Description: {maintenance_data['description']}"
    )


def wrap_data(data_set, width=60):
    wrapped_lines = []
    for data in data_set:
        info_line = []
        info = data.split()

        for word in info:
            if len(' '.join(info_line + [word])) <= width:
                info_line.append(word)
            else:
                wrapped_lines.append(' '.join(info_line))
                info_line = [word]
        if info_line:
            wrapped_lines.append(' '.join(info_line))

    return wrapped_lines


# define the format of displaying the content
def print_in_column(info1, info2, width=56):
    max_line = len(info1)
    if len(info2) > max_line:
        max_line = len(info2)
    new_info1 = info1 + [""] * (max_line - len(info1))
    new_info2 = info2 + [""] * (max_line - len(info2))

    for line1, line2 in zip(new_info1, new_info2):
        print(f'{line1.ljust(width + 8)}{line2.ljust(width)}')


def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


equipment_report_keeping = load_data_from_equipment_report_keeping()
baker_equipment = load_data_from_baker_equipment()  # store the data that retrieved from file into baker_equipment


def notification():
    while True:
        notice = load_data_from_notification()  # store the data that retrieved from file into notice
        notifications = []  # create a list for the number of notifications received
        print('')
        printed_centered('NOTIFICATIONS')
        # initialize the number of malfunction and maintenance reports to 0
        malfunction_report = 0
        maintenance_report = 0

        # if there is any malfunction equipments or equipments that need maintenance
        for equipment in notice.values():
            if equipment['current_condition'] == 'malfunction':
                malfunction_report += 1  # add the number of equipments that are malfunction to the report
            elif equipment['current_condition'] == 'maintenance needed':
                maintenance_report += 1  # add the number of equipments that need maintenance to the report

        # display how many reports if the report is not empty
        if malfunction_report != 0:
            print(f'🔔 {malfunction_report} notification(s) from Malfunction Report.')
        if maintenance_report != 0:
            print(f'🔔 {maintenance_report} notification(s) from Maintenance Report.\n')
        elif malfunction_report == 0 and maintenance_report == 0:
            print('🎉 Hooray! No notifications yet!\n')  # if there is no report, print the message of no notification

        print('\n1. Malfunction Report\n2. Maintenance Report\n3. Back to Manager Privilege')
        choice_of_report = input('\nEnter a number to get more insights: ')  # choose which report insights to see

        if choice_of_report == '1':  # malfunction report
            malfunction_equipment = []  # create a list to store the equipment names that are malfunction
            for equipment in notice.values():
                if equipment['current_condition'] == 'malfunction':
                    malfunction_equipment.append(equipment['serial_number'].lower())

            if len(malfunction_equipment) == 0:
                print('\n❗There is currently no malfunction report.')

            else:
                print('')
                print('-' * 109)
                print(f'\t\t\t\t\t\t\t\t\t\t\tMALFUNCTION REPORT')
                print('-' * 109)
                # display the malfunction equipment details in 2 columns for easy reading
                for equipment in notice.values():
                    if equipment['current_condition'] == 'malfunction':
                        notifications.append(malfunction_data_group(equipment).split('\n'))  # append the malfunction equipment details into the malfunction group

                for i in range(0, len(notifications), 2):
                    width = 55

                    noti1 = wrap_data(notifications[i], width=60)
                    if i + 1 < len(notifications):
                        noti2 = wrap_data(notifications[i + 1], width=60)
                    else:
                        noti2 = []

                    print_in_column(noti1, noti2)
                    print('-' * (width * 2))
                    if i == len(notifications) - 1:
                        print('')
                    else:
                        print('')

                while True:
                    equipment_number_to_repair = input('Enter serial number that need for repairment (or enter "done" to return back): ')  # collect the equipment name to repair
                    if equipment_number_to_repair.lower() not in malfunction_equipment:  # check if the name not in the list of malfunction equipment
                        if equipment_number_to_repair == 'done':  # user choose to return back to the previous page
                            print('\nExiting to Notification page......')
                            break
                        else:
                            print('\n+---------------------------------------------------------------------------+')
                            print('|⚠️ Invalid input or this equipment didn\'t be reported. Please enter again. |')
                            print('+---------------------------------------------------------------------------+\n')
                    else:
                        # the name is in the list of malfunction equipment
                        ways_to_repair = input('Do you want to repair yourself or contact the manufacturer? (r=repair yourself, c=contact manufacturer)\n>>> ')
                        while ways_to_repair not in ['r', 'c']:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+\n')
                            ways_to_repair = input('Do you want to repair yourself or contact the manufacturer? (r=repair yourself, c=contact manufacturer)\n>>> ')

                        if ways_to_repair == 'c':  # contact manufacturer
                            for equipment_key, equipment_value in baker_equipment.items():
                                if equipment_number_to_repair == equipment_value['serial_number']:  # compare the selected equipment exactly match with the name in notice and return true
                                    print(f'\n❗Please contact the manufacturer for repairment booking by this email: {equipment_value["manufacturer_email"]}')

                        repair_status = input('\nHas the equipment function well after repair? (y=yes, n=no)\n>>> ')
                        while repair_status not in ['y', 'n']:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')
                            repair_status = input('\nHas the equipment function well after repair? (y=yes, n=no)\n>>> ')

                        if repair_status == 'y':  # equipment function well after repairment
                            print('\nGreat! Your bakery can resume smooth operations.')
                            while True:
                                repair_cost = input('Please provide the cost incurred for this repair: RM ')
                                try:
                                    repair_cost = float(repair_cost)
                                    if repair_cost < 0:
                                        print('\n+--------------------------------+')
                                        print('|⚠️ Please enter positive value. |')
                                        print('+--------------------------------+\n')
                                        continue

                                    for serial_number, equipment in notice.items():
                                        if equipment_number_to_repair == equipment['serial_number'].lower():
                                            report_number = equipment['report_number']
                                            equipment_report_keeping[report_number] = {
                                                "category": equipment['category'],
                                                "equipment_name": equipment['equipment_name'],
                                                "serial_number": equipment['serial_number'],
                                                "model_number": equipment['model_number'],
                                                "repair_cost": f'RM {repair_cost:.2f}',
                                                "manufacturer_email": equipment['manufacturer_email'],
                                                "warranty": equipment['warranty'],
                                                "report_date": equipment['report_date'],
                                                "current_condition": "function well",
                                                "malfunction_date": equipment['malfunction_date'],
                                                "last_maintenance_date": equipment['last_maintenance_date'],
                                                "description": equipment['description']
                                            }
                                    del notice[equipment_number_to_repair]  # delete the notification upon settle
                                    save_info(notice)
                                    save_info_report(equipment_report_keeping)
                                    break

                                except ValueError:
                                    print('\n+------------------------------+')
                                    print('|⚠️ Please enter a valid cost. |')
                                    print('+------------------------------+\n')

                            malfunction_equipment.remove(equipment_number_to_repair)  # remove the name from the malfunction list upon read
                            malfunction_report -= 1  # reduce the number of malfunction report upon read
                            print('\nExiting to Notification page......')
                            break

                        elif repair_status == 'n' and ways_to_repair == 'c':  # manufacturer failed to repair the equipment
                            print('\nThe equipment is probably broken. Please claim the warranty from the manufacturer.')
                            for serial_number, equipment in notice.items():
                                if equipment_number_to_repair == equipment['serial_number'].lower():
                                    repair_cost = 0
                                    report_number = equipment['report_number']
                                    warranty = equipment['warranty']
                                    print(f'💡 There is a "{warranty}" warranty for this equipment.')

                                    equipment_report_keeping[report_number] = {
                                        "category": equipment['category'],
                                        "equipment_name": equipment['equipment_name'],
                                        "serial_number": equipment['serial_number'],
                                        "model_number": equipment['model_number'],
                                        "repair_cost": f'RM {repair_cost:.2f}',
                                        "manufacturer_email": equipment['manufacturer_email'],
                                        "warranty": equipment['warranty'],
                                        "report_date": equipment['report_date'],
                                        "current_condition": "waiting to claim the warranty",
                                        "malfunction_date": equipment['malfunction_date'],
                                        "last_maintenance_date": equipment['last_maintenance_date'],
                                        "description": equipment['description']
                                    }
                            del notice[equipment_number_to_repair]  # delete the notification upon settle
                            save_info(notice)
                            save_info_report(equipment_report_keeping)
                            malfunction_equipment.remove(equipment_number_to_repair)  # remove the name from the malfunction list upon read
                            malfunction_report -= 1  # reduce the number of malfunction report upon read
                            print('\nExiting to Notification page......')
                            break

                        elif repair_status == 'n' and ways_to_repair == 'r':  # users repair the equipment themselves but still malfunction
                            # advice user change a new equipment
                            print('\nThe equipment is probably broken. You may need to change a new one.')
                            while True:
                                repair_cost = input('Please provide the cost incurred for this repair: RM ')
                                try:
                                    repair_cost = float(repair_cost)
                                    if repair_cost < 0:
                                        print('\n+--------------------------------+')
                                        print('|⚠️ Please enter positive value. |')
                                        print('+--------------------------------+\n')
                                        continue

                                    for serial_number, equipment in notice.items():
                                        if equipment_number_to_repair == equipment['serial_number'].lower():
                                            report_number = equipment['report_number']
                                            equipment_report_keeping[report_number] = {
                                                "category": equipment['category'],
                                                "equipment_name": equipment['equipment_name'],
                                                "serial_number": equipment['serial_number'],
                                                "model_number": equipment['model_number'],
                                                "repair_cost": f'RM {repair_cost:.2f}',
                                                "manufacturer_email": equipment['manufacturer_email'],
                                                "warranty": equipment['warranty'],
                                                "report_date": equipment['report_date'],
                                                "current_condition": "waiting to replace with a new one",
                                                "malfunction_date": equipment['malfunction_date'],
                                                "last_maintenance_date": equipment['last_maintenance_date'],
                                                "description": equipment['description']
                                            }
                                    del notice[equipment_number_to_repair] # delete the notification upon settle
                                    save_info(notice)
                                    save_info_report(equipment_report_keeping)
                                    break

                                except ValueError:
                                    print('\n+------------------------------+')
                                    print('|⚠️ Please enter a valid cost. |')
                                    print('+------------------------------+\n')

                            malfunction_equipment.remove(equipment_number_to_repair)  # remove the name from the malfunction list upon read
                            malfunction_report -= 1  # reduce the number of malfunction report upon read
                            print('\nExiting to Notification page......')
                            break

        elif choice_of_report == '2':  # maintenance report
            maintenance_equipment = []  # create a list to store the equipment names that need maintenance
            for equipment in notice.values():
                if equipment['current_condition'] == 'maintenance needed':
                    maintenance_equipment.append(equipment['serial_number'].lower())

            if len(maintenance_equipment) == 0:
                print('\n❗There is currently no maintenance report.')

            else:
                print('')
                print('-' * 109)
                print(f'\t\t\t\t\t\t\t\t\t\t\tMAINTENANCE REPORT')
                print('-' * 109)
                # display the details of equipments that need maintenance in 2 columns for easy reading
                for equipment in notice.values():
                    if equipment['current_condition'] == 'maintenance needed':
                        notifications.append(maintenance_data_group(equipment).split('\n'))  # append the details of equipments that need maintenance into the maintenance group

                # display the equipment details that need maintenance in 2 columns for easy reading
                for i in range(0, len(notifications), 2):
                    width = 55

                    noti1 = wrap_data(notifications[i], width=60)
                    if i + 1 < len(notifications):
                        noti2 = wrap_data(notifications[i + 1], width=60)
                    else:
                        noti2 = []

                    print_in_column(noti1, noti2)
                    print('-' * (width * 2))
                    if i == len(notifications) - 1:
                        print('')
                    else:
                        print('')

                while True:
                    equipment_number_for_maintenance = input('Enter serial number that need for maintenance (or enter "done" to return back): ')  # collect the equipment name that need maintenance
                    if equipment_number_for_maintenance.lower() not in maintenance_equipment:  # check if the name not in the list of maintenance equipment
                        if equipment_number_for_maintenance == 'done':  # user choose to return back to the previous page
                            print('\nExiting to Notification page......')
                            break
                        else:
                            print('\n+---------------------------------------------------------------------------+')
                            print('|⚠️ Invalid input or this equipment didn\'t be reported. Please enter again. |')
                            print('+---------------------------------------------------------------------------+\n')

                    # the name is in the list of maintenance equipment
                    else:
                        for equipment in notice.values():
                            if equipment_number_for_maintenance == equipment['equipment_name'].lower():  # compare the selected equipment exactly match with the name in notice and return true
                                print(f'\n❗Please contact the manufacturer for maintenance booking by this email: {equipment["manufacturer_email"]}')  # ask user to contact manufacturer for maintenance
                                break

                        maintenance_status = input('\nHas the equipment function well? (y=yes, n=no)\n>>> ')
                        while maintenance_status not in ['y', 'n']:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+')
                            maintenance_status = input('\nHas the equipment function well after maintenance? (y=yes, n=no)\n>>> ')

                        if maintenance_status == 'y':  # equipment function well after maintenance
                            print('\nGreat! Your bakery can resume smooth operations.')
                            while True:
                                repair_cost = float(input('Please provide the cost incurred for this repair: RM '))
                                try:
                                    repair_cost = float(repair_cost)
                                    if repair_cost < 0:
                                        print('\n+--------------------------------+')
                                        print('|⚠️ Please enter positive value. |')
                                        print('+--------------------------------+\n')
                                        continue

                                    for serial_number, equipment in notice.items():
                                        if equipment_number_for_maintenance == equipment['serial_number'].lower():
                                            report_number = equipment['report_number']
                                            equipment_report_keeping[report_number] = {
                                                "category": equipment['category'],
                                                "equipment_name": equipment['equipment_name'],
                                                "serial_number": equipment['serial_number'],
                                                "model_number": equipment['model_number'],
                                                "repair_cost": f'RM {repair_cost:.2f}',
                                                "manufacturer_email": equipment['manufacturer_email'],
                                                "warranty": equipment['warranty'],
                                                "report_date": equipment['report_date'],
                                                "current_condition": "function well",
                                                "maintenance_needed_date": equipment['maintenance_needed_date'],
                                                "last_maintenance_date": equipment['last_maintenance_date'],
                                                "description": equipment['description']
                                            }
                                    del notice[equipment_number_for_maintenance]  # delete the notification upon settle
                                    save_info(notice)
                                    save_info_report(equipment_report_keeping)
                                    break

                                except ValueError:
                                    print('\n+------------------------------+')
                                    print('|⚠️ Please enter a valid cost. |')
                                    print('+------------------------------+')

                            maintenance_equipment.remove(equipment_number_for_maintenance)
                            maintenance_report -= 1  # reduce the number of maintenance report upon read
                            print('\nExiting to Notification page......')
                            break

                        elif maintenance_status == 'n':  # equipment not function well after maintenance
                            for serial_number, equipment in notice.items():
                                if equipment_number_for_maintenance == equipment['serial_number'].lower():
                                    warranty = equipment['warranty']
                                    print(f'\n💡 There is a "{warranty}" warranty for this equipment.')
                                    print('The equipment is probably broken. Please claim the warranty from the manufacturer.')

                            while True:
                                repair_cost = float(input('Please provide the cost incurred for this repair: RM '))
                                try:
                                    if repair_cost < 0:
                                        print('\n+--------------------------------+')
                                        print('|⚠️ Please enter positive value. |')
                                        print('+--------------------------------+')
                                        continue

                                    for serial_number, equipment in notice.items():
                                        if equipment_number_for_maintenance == equipment['serial_number'].lower():
                                            report_number = equipment['report_number']

                                            equipment_report_keeping[report_number] = {
                                                "category": equipment['category'],
                                                "equipment_name": equipment['equipment_name'],
                                                "serial_number": equipment['serial_number'],
                                                "model_number": equipment['model_number'],
                                                "repair_cost": f'RM {repair_cost:.2f}',
                                                "manufacturer_email": equipment['manufacturer_email'],
                                                "warranty": equipment['warranty'],
                                                "report_date": equipment['report_date'],
                                                "current_condition": "waiting to claim the warranty",
                                                "maintenance_needed_date": equipment['maintenance_needed_date'],
                                                "last_maintenance_date": equipment['last_maintenance_date'],
                                                "description": equipment['description']
                                            }
                                    del notice[equipment_number_for_maintenance]  # delete the notification upon settle
                                    save_info(notice)
                                    save_info_report(equipment_report_keeping)
                                    break

                                except ValueError:
                                    print('\n+------------------------------+')
                                    print('|⚠️ Please enter a valid cost. |')
                                    print('+------------------------------+')

                            maintenance_equipment.remove(equipment_number_for_maintenance)
                            maintenance_report -= 1
                            print('\nExiting to Notification page......')
                            break

        elif choice_of_report == '3':  # return to the previous page
            print('\nExiting to Manager Privilege......')
            return False
    
        else:
            print('\n+--------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

