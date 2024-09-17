import json


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


def save_info(notice):
    file = open('notification.txt', 'w')  # open the file to write
    json.dump(notice, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


notice = load_data_from_notification()


def notification():
    print('\n-----------------------------------------------')
    print(f'\t\t\t\tNOTIFICATIONS')
    print('-----------------------------------------------')
    if len(notice) == 0:
        print('🎉 Hooray! No notifications yet!')
        noti_person = 'uncle'
        noti_message = 'aaaaa'
        noti_date = 'ddddd'

        notice[noti_person] = {
            'noti_message': noti_message,
            'noti_date': noti_date
        }
        save_info(notice)

    else:
        print(f'📜 You have {len(notice)} notifications.')



notification()