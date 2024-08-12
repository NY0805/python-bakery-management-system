def customer():
    ans = input('Do you have an account (yes/no)? ')
    if ans == 'yes':
        print('Please login for further action.')
        user_account = input('Please enter your username: ')
        user_credentials = input('Please enter your password: ')

        info = {
            'username': user_account,
            'password': user_credentials
        }
        action = input('What action do you want (manage/update)? ')
        if action == 'manage':
            a = input('username / password? ')
            print(info[a])

def manager():
    print('Services:')
    print('a. system administration')
    print('b. order management')
    print('c. financial management')
    print('d. inventory control')
    print('e. customer feedback')
    choice = input('What service do you want (a, b, ,c, d, e)? ')
    if choice == 'a':
        print('x')

print('**********************************')
print('WELCOME TO 《MORNING GLORY BAKERY》')
print('**********************************')
print('Role: ')
print('1. Manager')
print('2. Customer')
print('3. Cashier')
print('4. Baker(s)')
role = int(input('Please select a role (1, 2, 3, 4): '))

if role == 2:
    customer()
elif role == 1:
    manager()

