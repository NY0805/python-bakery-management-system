import re  # import the regular expressions(regex), a type of text pattern matching tool to check if a string contains the specified search pattern
import json  # import json text file to record data


# Define the function that loads data from the file
def load_data_from_file():
    try:
        file = open('manager.txt', 'r')  # open the file and read
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


# Define the function that saves information to the file
def save_info(info):

    file = open('manager.txt', 'w')  # open the file to write
    json.dump(info, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


# create a function for manager
def manager():

    info = load_data_from_file()  # initialize 'info' as the name of dictionary that store data loaded from file

    manager_username = input('Please enter your username: ')
    manager_password = input('Please enter your password: ')

    if manager_username in info:
        if info[manager_username]['manager_password'] == manager_password:  # ensure the password match the data in 'info'
            print('\nLogin successfully!')
            print('Welcome, ', manager_username, '!')
            print('\nServices:')
            print(
                'a. system administration\n'
                'b. order management\n'
                'c. financial management\n'
                'd. inventory control\n'
                'e. customer feedback'
            )
            choice = input('Select a choice (a, b, c, d, e): ')
            if choice in ['a', 'b', 'c', 'd', 'e']:
                if choice == 'a':
                    print('enter again.')

                elif choice == 'b':
                    print('enter again.')

                elif choice == 'c':
                    print('enter again.')

                elif choice == 'd':
                    print('enter again.')

                elif choice == 'e':
                    print('enter again.')

            else:
                print('enter again.')
        else:
            print('Username or password invalid, please enter again or try another account.\n')  # prompt user to input again if it does't match with data in file
            manager()
    else:
        if len(manager_password) < 8 or len(manager_password) > 12:  # to ensure the password entered is between 8 to 12 digits
            print('Invalid password. Please make sure it is between 8 to 12 digits!\n')
            manager()  # if fail to meet the criteria, ask user to enter again

        # automatically considered as first time login if the data entered not found in file
        else:
            print('------------------------------------------------------------------')
            print('This is your first time login, kindly complete your personal info.')
            print('------------------------------------------------------------------')
            while True:
                try:
                    age = int(input('Age: '))
                    if age < 18:
                        print('You are under the age. Required age is 18 and above.')
                        print('Please enter a valid age.')
                    else:
                        break  # Exit the loop if age is valid
                except ValueError:
                    print('Please enter a valid age.')

            while True:
                gender = input('Gender(m=male, f=female): ')
                if gender not in ['f', 'm']:
                    print('Invalid input. Please enter again.')
                else:
                    if gender == 'f':
                        gender = 'female'
                    else:
                        gender = 'male'
                    break  # Exit the loop if age is valid

            while True:
                contact_no = input('Contact number(xxx-xxxxxxx): ')
                pattern = r'^\d{3}-\d{7}$'  # define the format of contact number
                if not re.fullmatch(pattern, contact_no):
                    print('Invalid contact number. Please enter again.')
                else:
                    break  # Exit the loop if age is valid

            while True:
                try:
                    email = input('Email: ')
                    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # define the format of email
                    if not re.fullmatch(pattern, email):
                        print('Invalid email. Please enter again.')
                    else:
                        break  # Exit the loop if age is valid
                except TypeError:
                    print('Invalid. Please enter again.')

            # update the dictionary with user input
            info[manager_username] = {
                'manager_password': manager_password,
                'age': age,
                'gender': gender,
                'contact_no': contact_no,
                'email': email
            }

            # write the updates into file
            save_info(info)
            print('Information saved.\n')  # let user know their information are saved
            print('--------------------------------------------------')
            print('Thank you for completing the personal information.')
            print('--------------------------------------------------')
            print('For security purpose, please log in again to access the system.\n')
            manager()  # prompt user to login again after filled out their information


# Run the manager function
