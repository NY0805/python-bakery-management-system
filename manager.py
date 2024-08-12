import re  # import the regular expressions(regex), a type of text pattern matching tool to check if a string contains the specified search pattern
import json  # import json text file to record data

# Create a dictionary named 'info'
info = {}


# Define the function that loads data from the file
def load_data_from_file():
    global info  # to access 'info' dictionary outside the function
    try:
        file = open('manager.json', 'r')  # open the file and read
        content = file.read().strip()  # Read the content and strip any whitespace
        if content:  # Check if the file is not empty
            info = json.loads(content)
        else:
            info = {}  # Initialize as an empty dictionary if the file is empty
    except FileNotFoundError:
        info = {}  # Initialize as an empty dictionary if the file does not exist


# Define the function that saves information to the file
def save_info():
    file = open('manager.json', 'w')  # open the file to write
    json.dump(info, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization


# create a function for manager
def manager():
    load_data_from_file()

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
        else:
            print('Username or password invalid, please enter again or try another account.')  # prompt user to input again if it does't match
            manager()
    else:
        if len(manager_password) < 8 or len(manager_password) > 12:  # to ensure the password entered is between 8 to 12 digits
            print('Invalid password. Please make sure it is between 8 to 12 digits!')
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
                gender = input('Gender(m=male, f=female, x=prefer not to say): ')
                if gender not in ['f', 'm', 'x']:
                    print('Invalid input. Please enter again.')
                else:
                    if gender == 'f':
                        gender = 'female'
                    elif gender == 'm':
                        gender = 'male'
                    else:
                        gender = 'prefer not to say'
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
            save_info()
            print('Information saved.\n')  # let user know their information are saved
            print('--------------------------------------------------')
            print('Thank you for completing the personal information.')
            print('--------------------------------------------------')
            print('For security purpose, please log in again to access the system.')
            manager()  # prompt user to login again after filled out their information


# Run the manager function
manager()