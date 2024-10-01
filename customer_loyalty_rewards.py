import json

# Constants for points and rewards in RM
BASE_POINTS_PER_RM = 10  # Points earned per RM spent
BRONZE_REQUIREMENT = 500  # Points needed for Bronze status
SILVER_REQUIREMENT = 1000  # Points needed for Silver status
GOLD_REQUIREMENT = 2000  # Points needed for Gold status
FREE_SHIPPING_THRESHOLD = 350  # Points needed for free shipping


def load_customer_data():
    try:
        file = open('customer_loyalty_rewards.txt', 'r')  # open the file and read
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


def save_customer_data(customers):
    with open('customer_loyalty_rewards.txt', 'w') as file:
        json.dump(customers, file, indent=4)


def calculate_points(transaction_value):
    points_earned = transaction_value * BASE_POINTS_PER_RM
    print(f"Points earned for RM{transaction_value} purchase: {points_earned}")
    return points_earned


def update_loyalty_status(points_balance):
    if points_balance >= GOLD_REQUIREMENT:
        return "Gold"
    elif points_balance >= SILVER_REQUIREMENT:
        return "Silver"
    elif points_balance >= BRONZE_REQUIREMENT:
        return "Bronze"
    else:
        return "Standard"


def check_free_shipping(username):
    customers = load_customer_data()
    if username in customers:
        customer = customers[username]
        points_balance = customer['loyalty_points']
        status = customer.get('status', 'Standard')

        # Gold members automatically have free shipping
        if status == "Gold":
            print("As a Gold member, you are eligible for free shipping!")
        elif points_balance >= FREE_SHIPPING_THRESHOLD:
            print("You are eligible for free shipping!")
        else:
            print(f"You need {FREE_SHIPPING_THRESHOLD - points_balance} more points to be eligible for free shipping.")
    else:
        print("|⚠️Customer cannot be found!|")


def update_purchase_history(username, purchase_amount):
    customers = load_customer_data()
    points_earned = calculate_points(purchase_amount)

    if username in customers:
        customer = customers[username]
        customer['total_spending (RM)'] += purchase_amount  # Update total spending
        customer['loyalty_points'] += points_earned
    else:
        customer = {
            'total_spending (RM)': purchase_amount,
            'loyalty_points': points_earned,
            'status': 'Standard'  # New customers start with "Standard" status
        }

    # Update status based on new points balance
    customer['status'] = update_loyalty_status(customer['loyalty_points'])

    # Update customer data
    customers[username] = customer
    save_customer_data(customers)


def view_loyalty_rewards():
    username = input("Enter your username: ").strip().lower()  # Strip whitespace and convert to lowercase
    customers = load_customer_data()  # Load the customer data

    # Loop through all customer records
    for customer_id, customer_info in customers.items():
        # If a matching username is found
        if customer_info['username'].strip().lower() == username:
            print(f"Customer {customer_info['username']} has a total spending of RM {customer_info['total_spending (RM)']}.")
            print(f"Loyalty points: {customer_info['loyalty_points']}")
            print(f"Status: {customer_info['status']}")
            return

    # If no matching username is found
    print("|⚠️Customer cannot be found!|")



def loyalty_rewards():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'CUSTOMER LOYALTY REWARDS')
        print('-----------------------------------------------')
        print()
        print("1. Update Purchase History")
        print("2. View Loyalty Rewards")
        print("3. Check Free Shipping Eligibility")
        print("4. Exit to main menu")

        choice = input("Select your option:  ")

        if choice == '1':
            username = input("Enter your username: ")
            try:
                purchase_amount = float(input("Enter the purchase amount in RM: "))
                update_purchase_history(username, purchase_amount)
            except ValueError:
                print("Invalid input. Please enter a valid number for the purchase amount.")

        elif choice == '2':
            view_loyalty_rewards()

        elif choice == '3':
            username = input("Enter your username: ")
            check_free_shipping(username)

        elif choice == '4':
            print("Thank you for using the Customer Loyalty Program. Goodbye!")
            break

        else:
            print("|⚠️Invalid option! Please try again.|")


loyalty_rewards()



