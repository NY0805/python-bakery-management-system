import json

def create_account():
    # Getting user input
    username = input("Enter username: ")
    password = input("Enter password: ")
    age = input("Enter your age: ")
    gender = input("Select your gender (M for male, F for female): ")
    if
    contact_no = input("Enter your contact number: ")
    email = input("Enter your email: ")

    # Manage customers' personal information in the dictionary
    personal_info = {
        "username":username,
        "password":password,
        "age": age,
        "gender": gender,
        "contact_no": contact_no,
        "email": email
    }

    # Try to open and read the accounts.txt file
    try:
        with open('accounts.txt', 'r') as file:
            accounts = file.readlines()
            # Check if the username already exists
            for account in accounts:
                stored_username = account.split(',')[0]
                if stored_username == username:
                    print("Username already exists.")
                    return
    except FileNotFoundError:
        # If the file doesn't exist, treat it as an empty file
        accounts = []

    # If the username is new, add the new account information
    with open('accounts.txt', 'a') as file:
        file.write(f"{username},{password},{personal_info['age']},{personal_info['gender']},{personal_info['contact_no']},{personal_info['email']}\n")

    print("Welcome,your account has been created successfully!")

# Run the function to create an account
create_account()

hgh