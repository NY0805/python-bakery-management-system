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

            # Redeem cash voucher option
            redeem_cash_voucher(customer_info)
            break
    else:
        print(f"User {username} does not exist.")


def redeem_cash_voucher(customer_info):
    username = customer_info['username']
    points = customer_info['loyalty_points']
    status = customer_info['status']
    points_per_voucher = REDEEM_RATES.get(status)

    if points_per_voucher is None:
        print("Standard users cannot redeem cash vouchers.")
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
            else:
                print("|⚠️Invalid number of vouchers!|")
        else:
            print("No vouchers redeemed.")
    else:
        print(f"Your points are not enough! You need at least {points_per_voucher} points per voucher.")


def update_loyalty_rewards(username, total_spending, order_id):
    """Update or create customer loyalty rewards based on total spending."""
    # Load existing customer data
    customers = load_customer_data()

    # Check if the customer already exists
    if username in customers.values():
        # Find the existing customer's ID
        customer_id = [cid for cid, info in customers.items() if info["username"] == username][0]
        loyalty_points, status = determine_loyalty_points(total_spending)

        # Update existing customer's total spending and loyalty points
        customers[customer_id]["total_spending (RM)"] += total_spending
        customers[customer_id]["loyalty_points"] += loyalty_points
        customers[customer_id]["status"], customers[customer_id]["redeem_rate (RM)"] = determine_loyalty_points(
            customers[customer_id]["total_spending (RM)"])

        # Append the new order ID to the existing list of order IDs
        if "order_id" not in customers[customer_id]:
            customers[customer_id]["order_id"] = []
        customers[customer_id]["order_id"].append(order_id)

    else:
        # New customer, calculate loyalty points and status
        loyalty_points, status = determine_loyalty_points(total_spending)
        redeem_rate = REDEEM_RATES[status]

        # Create new customer entry
        customer_id = str(len(customers) + 1)  # Create a new customer ID
        customers[customer_id] = {
            "username": username,
            "total_spending (RM)": total_spending,
            "loyalty_points": loyalty_points,
            "status": status,
            "redeem_rate (RM)": redeem_rate,
            "order_id": [order_id]  # Initialize with the current order ID
        }

    # Save updated customer data
    save_customer_data(customers)
    print(f"Customer {username}'s loyalty rewards updated successfully!")


def loyalty_rewards():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\tCUSTOMER LOYALTY REWARDS')
        print('-----------------------------------------------')
        print()
        print("1. View and Redeem Loyalty Rewards")
        print("2. Exit to main menu")

        choice = input("Select your option: ")

        if choice == '1':
            view_loyalty_rewards()
        elif choice == '2':
            print("Thank you for visiting Customer Loyalty Program. Goodbye!")
            break
        else:
            print("|⚠️Invalid option! Please try again.|")

