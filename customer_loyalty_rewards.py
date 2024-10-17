import json

# Constants for points and rewards in RM
BASE_POINTS_PER_RM = 10  # Points earned per RM spent
BRONZE_REQUIREMENT = 500  # Points needed for Bronze status
SILVER_REQUIREMENT = 1000  # Points needed for Silver status
GOLD_REQUIREMENT = 2000  # Points needed for Gold status

# Constants for redeemable cash voucher rate based on status
REDEEM_RATES = {
    "MORNING GLORY'S GOLD": 70,  # Gold users need 70 points for each RM10 voucher
    "MORNING GLORY'S SILVER": 90,  # Silver users need 90 points for each RM10 voucher
    "MORNING GLORY'S BRONZE": 120,  # Bronze users need 120 points for each RM10 voucher
    "Standard": None  # Standard users cannot redeem vouchers
}


def load_customer_data():
    """Load customer loyalty data from a file."""
    try:
        with open('customer_loyalty_rewards.txt', 'r') as file:
            content = file.read().strip()
            if content:
                return json.loads(content)  # Load existing customer data
            else:
                return {}
    except FileNotFoundError:
        return {}  # Return empty dictionary if file not found


def save_customer_data(customers):
    """Save customer loyalty data to a file."""
    with open('customer_loyalty_rewards.txt', 'w') as file:
        json.dump(customers, file, indent=4)


def determine_loyalty_points(total_spending):
    """Determine loyalty points and status based on total spending."""
    loyalty_points = int(total_spending * BASE_POINTS_PER_RM)
    if loyalty_points >= GOLD_REQUIREMENT:
        return loyalty_points, "MORNING GLORY'S GOLD"
    elif loyalty_points >= SILVER_REQUIREMENT:
        return loyalty_points, "MORNING GLORY'S SILVER"
    elif loyalty_points >= BRONZE_REQUIREMENT:
        return loyalty_points, "MORNING GLORY'S BRONZE"
    else:
        return loyalty_points, "Standard"


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
            print(f"Redeem Rate: {customer_info['redeem_rate (RM)']} points per voucher")  # Display redeem rate
            return customer_info

    print(f"User {username} does not exist.")
    return None


def redeem_cash_voucher(customer_info):  # Allow customer to redeem cash vouchers using their loyalty points
    username = customer_info['username']
    points = customer_info['loyalty_points']
    status = customer_info['status']
    points_per_voucher = REDEEM_RATES.get(status)

    if points_per_voucher is None:
        print("Standard users cannot redeem cash vouchers.")
        return

    max_vouchers = points // points_per_voucher  # Calculate the maximum number of vouchers
    if max_vouchers > 0:
        print(f"\nYou have {points} loyalty points.")
        print(f"As a {status} member, you can redeem up to {max_vouchers} cash vouchers (Each RM10).")
        choice = input("Would you like to redeem your points for cash vouchers? yes=y no=n (y/n): ").lower()
        if choice == 'y':
            try:
                num_vouchers = int(input(f"How many vouchers would you like to redeem (up to {max_vouchers})? "))
                if 0 < num_vouchers <= max_vouchers:
                    customer_info['loyalty_points'] -= num_vouchers * points_per_voucher  # Deduct points
                    print(f"Success! You have redeemed {num_vouchers} voucher(s) worth RM{num_vouchers * 10}.")

                    # Save the updated customer data
                    customers = load_customer_data()
                    for customer_id, info in customers.items():
                        if info['username'] == username:
                            customers[customer_id]['loyalty_points'] = customer_info['loyalty_points']  # Update points
                            save_customer_data(customers)  # Save to file
                            print("Your updated loyalty points have been saved.")
                            break
                else:
                    print("|⚠️Invalid number of vouchers!|")
            except ValueError:
                print("|⚠️Please enter a valid number!|")
        else:
            print("No vouchers redeemed.")
    else:
        print(f"Your points are not enough! You need at least {points_per_voucher} points per voucher.")



def loyalty_rewards():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\tCUSTOMER LOYALTY REWARDS')
        print('-----------------------------------------------')
        print()
        print("1. View Loyalty Rewards")
        print("2. Redeem Cash Vouchers")
        print("3. Exit to main menu")

        choice = input("Select your option: ")

        if choice == '1':
            customer_info = view_loyalty_rewards()

        elif choice == '2':
            username = input("Enter your username: ").strip()
            customers = load_customer_data()
            for customer_id, customer_info in customers.items():
                if customer_info['username'] == username:
                    redeem_cash_voucher(customer_info)
                    break
            else:
                print(f"Invalid username. Please try again.")

        elif choice == '3':
            print("Thank you for visiting Customer Loyalty Program. Goodbye!")
            break

        else:
            print("|⚠️Invalid option! Please try again.|")


#loyalty_rewards()
