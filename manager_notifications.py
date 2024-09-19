import json
import time


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


def save_info(notice):
    file = open('notification.txt', 'w')  # open the file to write
    json.dump(notice, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


notice = load_data_from_notification()
baker_equipment = load_data_from_baker_equipment()


def notification():

    while True:
        print('\n-----------------------------------------------')
        print(f'\t\t\t\tNOTIFICATIONS')
        print('-----------------------------------------------')
        malfunction_report = 0
        maintenance_report = 0

        for value in notice.values():
            if value['current_condition'] == 'malfunction':
                malfunction_report += 1
            elif value['current_condition'] == 'maintenance needed':
                maintenance_report += 1

        if malfunction_report != 0:
            print(f'🔔 {malfunction_report} notification(s) from Malfunction Report.')
        if maintenance_report != 0:
            print(f'🔔 {maintenance_report} notification(s) from Maintenance Report.\n')
        else:
            print('🎉 Hooray! No notifications yet!')

        print('\n1. Malfunction Report\n2. Maintenance Report')
        try:
            choice_of_report = int(input('\nEnter a number to get more insights: '))

            if choice_of_report == 1:
                malfunction_equipment = []
                if len(malfunction_equipment) == 0:
                    print('\n❗There is currently no malfunction report.')

                else:
                    print('\n-----------------------------------------------')
                    print(f'\t\t\tMALFUNCTION REPORT')
                    print('-----------------------------------------------')

                    for notice_value in notice.values():
                        if notice_value['current_condition'] == 'malfunction':
                            malfunction_equipment.append(notice_value['equipment_name'].lower())

                            print(f'📍 {notice_value["equipment_name"].title()} 📍')
                            for sub_key, sub_value in notice_value.items():
                                if sub_key == 'equipment_name':
                                    continue
                                else:
                                    print(f'{sub_key:<23}: {sub_value}')
                            print('')

                            while True:
                                equipment_name_to_repair = input('Enter equipment name that need for repairment (or enter "done" to return back): ')
                                if equipment_name_to_repair.lower() not in malfunction_equipment:
                                    if equipment_name_to_repair == 'done':
                                        print('\nExiting to Notification page......')
                                        break
                                    else:
                                        print('\n+---------------------------------------------------------------------------+')
                                        print('|⚠️ Invalid input or this equipment didn\'t be reported. Please enter again. |')
                                        print('+---------------------------------------------------------------------------+\n')
                                else:
                                    ways_to_repair = input('Do you want to repair yourself or contact the manufacturer? (a=repair yourself, b=contact manufacturer)\n>>> ')
                                    while ways_to_repair not in ['a', 'b']:
                                        print('\n+--------------------------------------+')
                                        print('|⚠️ Invalid input. Please enter again. |')
                                        print('+--------------------------------------+\n')
                                        ways_to_repair = input('Do you want to repair yourself or contact the manufacturer? (a=repair yourself, b=contact manufacturer)\n>>> ')

                                    if ways_to_repair == 'b':
                                        for equipment_key, equipment_value in baker_equipment.items():
                                            if equipment_name_to_repair.lower() == equipment_value['equipment_name'].lower():  # to ensure it is exactly the selected item
                                                manufacturer_name = equipment_value['manufacturer']
                                                manufacturer_email = equipment_value['manufacturer_email']
                                                serial_number = notice_value['serial_number']

                                                print('\n❗Important Information❗')
                                                print(f'Serial number: {serial_number}\n'
                                                      f'Manufacturer: {manufacturer_name}'
                                                      f'Contact email: {manufacturer_email}')

                                    repair_status = input('\nHas the equipment function well? (y=yes, n=no)\n>>> ')
                                    while repair_status not in ['y', 'n']:
                                        print('\n+--------------------------------------+')
                                        print('|⚠️ Invalid input. Please enter again. |')
                                        print('+--------------------------------------+')
                                        repair_status = input('\nHas the equipment function well? (y=yes, n=no)\n>>> ')

                                    if repair_status == 'y':
                                        print('\nGreat! Your bakery can resume smooth operations.')
                                        malfunction_equipment.remove(equipment_name_to_repair)
                                        notice_value['current_condition'] = 'function well'
                                        malfunction_report -= 1
                                        break

                                    elif repair_status == 'n' and ways_to_repair == 'b':
                                        for equipment in baker_equipment.values():
                                            warranty = equipment['warranty']
                                            print('\n+---------------------------------------------+')
                                            print(f'|💡 There is a "{warranty}" warranty for this equipment. |')
                                            print('+---------------------------------------------+\n')
                                            print('The equipment is probably broken. You may need to change a new one or claim the warranty from the manufacturer.')
                                            print('Exiting to Notification page......')
                                            notice_value['current_condition'] = 'waiting to claim warranty / replace with a new one'
                                            malfunction_report -= 1
                                            break
                                        break

                                    elif repair_status == 'n' and ways_to_repair == 'a':
                                        print('\nThe equipment is probably broken. You may need to change a new one.')
                                        print('Exiting to Notification page......')
                                        notice_value['current_condition'] = 'waiting to replace with a new one'
                                        malfunction_report -= 1
                                        break

                            save_info(notice)

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+\n')

        except ValueError:
            print('\n+------------------------------+')
            print('|⚠️ Please enter numbers only. |')
            print('+------------------------------+\n')





notification()