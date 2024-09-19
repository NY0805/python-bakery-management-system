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
            print(f'🔔 {maintenance_report} notification(s) from Maintenance Report.\n\n')

        while True:
            print('1. Malfunction Report\n2. Maintenance Report')
            choice_of_report = input('\nChoose a report to see more details: ')

            if choice_of_report not in ['1,', '2']:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+\n')
            if choice_of_report.lower() == '1' or 'malfunction_report':
                print('\n-----------------------------------------------')
                print(f'\t\t\tMALFUNCTION REPORT')
                print('-----------------------------------------------')
                malfunction_equipment = []
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

                        equipment_name_to_repair = input('Enter equipment name that need for repairment: ')
                        while equipment_name_to_repair.lower() not in malfunction_equipment:
                            print('\n+----------------------------------------------------------------------------+')
                            print('|⚠️ Invalid input or this equipment didn\'t be reported. Please enter again. |')
                            print('+----------------------------------------------------------------------------+\n')
                            equipment_name_to_repair = input('Enter equipment name that need for repairment: ')

                        ways_to_repair = input('Do you want to repair yourself or contact the manufacturer? (a=repair yourself, b=contact manufacturer)\n>>> ')
                        while ways_to_repair not in ['a', 'b']:
                            print('\n+--------------------------------------+')
                            print('|⚠️ Invalid input. Please enter again. |')
                            print('+--------------------------------------+\n')
                            ways_to_repair = input('Do you want to repair yourself or contact the manufacturer? (a=repair yourself, b=contact manufacturer)\n>>> ')

                        else:
                            if ways_to_repair == 'b':
                                for equipment_key, equipment_value in baker_equipment.items():
                                    if equipment_name_to_repair.lower() == equipment_value['equipment_name'].lower():  # to ensure it is exactly the selected item
                                        manufacturer_name = equipment_value['manufacturer']
                                        #manufacturer_contact = equipment_value['manufacturer_email']
                                        serial_number = notice_value['serial_number']

                                        print('\n❗Important Information:')
                                        print(f'Serial number: {serial_number}\n'
                                              f'Manufacturer: {manufacturer_name}\n')
                                              #f'Contact email: {manufacturer_email}')

                            while True:
                                repair_status = input('Has the equipment function well? (y=yes, n=no)\n>>> ')
                                if repair_status == 'y':
                                    print('Great! Your bakery can resume smooth operations.\n')
                                    malfunction_equipment.remove(equipment_name_to_repair)
                                    notice_value['current_condition'] = 'function well'
                                    #save_info(notice)
                                    break

                                elif repair_status == 'n':
                                    for equipment in baker_equipment.values():
                                        #warranty = equipment['warranty']
                                        print('\n+---------------------------------------------+')
                                        #print(f'|💡 There is a {warranty} for this equipment. |')
                                        print('+---------------------------------------------+\n')
                                        print('The equipment is probably broken. You may need to change a new one or claim the warranty from the manufacturer.\n')
                                        break
                                    break

                                else:
                                    print('\n+--------------------------------------+')
                                    print('|⚠️ Invalid input. Please enter again. |')
                                    print('+--------------------------------------+\n')

            else:
                print('\n+--------------------------------------+')
                print('|⚠️ Invalid input. Please enter again. |')
                print('+--------------------------------------+\n')




    else:
        print('🎉 Hooray! No notifications yet!')


        #print(time.strftime("%d-%m-%Y"))



notification()