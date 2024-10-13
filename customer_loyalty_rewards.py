import json

# Constants for points and rewards in RM
BASE_POINTS_PER_RM = 10  # Points earned per RM spent
BRONZE_REQUIREMENT = 500  # Points needed for Bronze status
SILVER_REQUIREMENT = 1000  # Points needed for Silver status
GOLD_REQUIREMENT = 2000  # Points needed for Gold status

# Constants for redeemable cash voucher rate based on status
VOUCHER_VALUE = 10  # RM10 per voucher
REDEEM_RATES = {
    "MORNING GLORY'S GOLD": 70,  # Gold users need 70 points for each RM10 voucher
    "MORNING GLORY'S SILVER": 90,  # Silver users need 90 points for each RM10 voucher
    "MORNING GLORY'S BRONZE": 120,  # Bronze users need 120 points for each RM10 voucher
    "Standard": None  # Standard users cannot redeem vouchers
}


def load_customer_data():
    try:
        with open('customer_loyalty_rewards.txt', 'r') as file:
            content = file.read().strip()
            if content:
                return json.loads(content)  # Load existing customer data
            else:
                return {}
    except FileNotFoundError:
        return {}


def save_customer_data(customers):
    with open('customer_loyalty_rewards.txt', 'w') as file:
        json.dump(customers, file, indent=4)


def update_customer_info(username, customer_info):
    customers = load_customer_data()  # Load existing customer data

    # Iterate through customers to find the one with the matching username
    for customer_id, info in customers.items():
        if info["username"] == username:
            # Update existing customer information
            customers[customer_id].update(customer_info)
            print(f"Updated information for {username}.")
            break
    else:
        print(f"User {username} does not exist. No update made.")
        return  # Exit the function if the user doesn't exist

    save_customer_data(customers)  # Save the updated customer data


def redeem_cash_voucher(customer_info):
    username = customer_info['username']
    points = customer_info['loyalty_points']
    status = customer_info['status']
    points_per_voucher = REDEEM_RATES.get(status)

    if points_per_voucher is None:
        print("Sorry, Standard users cannot redeem cash vouchers.")
        return

    max_vouchers = points // points_per_voucher
    if max_vouchers > 0:
        print(f"\nYou have {points} loyalty points.")
        print(f"As a {status} member, you can redeem up to {max_vouchers} cash vouchers (Each RM{VOUCHER_VALUE}).")
        choice = input("Would you like to redeem your points for cash vouchers? yes=y no=n (y/n): ").lower()
        if choice == 'y':
            num_vouchers = int(input(f"How many vouchers would you like to redeem (up to {max_vouchers})? "))
            if 0 < num_vouchers <= max_vouchers:
                customer_info['loyalty_points'] -= num_vouchers * points_per_voucher  # Deduct points
                print(f"Success! You have redeemed {num_vouchers} voucher(s) worth RM{num_vouchers * VOUCHER_VALUE}.")

                # Update customer info in the file
                update_customer_info(username, customer_info)  # Update the existing customer data
            else:
                print("|⚠️Invalid number of vouchers!|")
        else:
            print("No vouchers redeemed.")
    else:
        print(f" Your points are not enough! You need at least {points_per_voucher} points per voucher.")


def view_loyalty_rewards():
    username = input("Enter your username: ").strip()  # Prompt user for username
    customers = load_customer_data()

    for customer_id, customer_info in customers.items():
        if customer_info['username'] == username:  # Find user by username
            print('\n --Loyalty Rewards Information-- ')
            print(f"Username: {customer_info['username']}")
            print('─' * 47)
            print(f"Total Spending (RM): {customer_info['total_spending (RM)']}")
            print(f"Loyalty Points: {customer_info['loyalty_points']}")
            print(f"Status: {customer_info['status']}")
            print(f"Redeem Rate: {customer_info['redeem_rate (RM)']}")  # Use redeem_rate
            redeem_cash_voucher(customer_info)
            break
    else:
        print(f"User {username} does not exist. Please check your username.")


def loyalty_rewards():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\tCUSTOMER LOYALTY REWARDS')
        print('-----------------------------------------------')
        print()
        print("1. View Loyalty Rewards")
        print("2. Exit to main menu")

        choice = input("Select your option: ")

        if choice == '1':
            view_loyalty_rewards()
        elif choice == '2':
            print("Thank you for visiting Customer Loyalty Program. Goodbye!")
            break
        else:
            print("|⚠️Invalid option! Please try again.|")

# Start the loyalty rewards program
loyalty_rewards()
