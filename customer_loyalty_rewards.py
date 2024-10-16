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


def determine_status(loyalty_points):
    """Determine customer status based on loyalty points."""
    if loyalty_points >= GOLD_REQUIREMENT:
        return "MORNING GLORY'S GOLD"
    elif loyalty_points >= SILVER_REQUIREMENT:
        return "MORNING GLORY'S SILVER"
    elif loyalty_points >= BRONZE_REQUIREMENT:
        return "MORNING GLORY'S BRONZE"
    else:
        return "Standard"


def update_customer_info(username, customer_info):
    customers = load_customer_data()  # Load existing customer data
    for customer_id, customer in customers.items():
        if customer['username'] == username:
            customers[customer_id] = customer_info  # Update customer info
            print(f"Information for {username} has been updated.")
            save_customer_data(customers)  # Save updated customer data to file
            return
    print(f"User {username} not found. No update performed.")


def create_new_customer():
    """Create a new customer and save to file."""
    username = input("Enter a username for the new customer: ")

    # Input total spending with validation
    while True:
        try:
            total_spending = float(input("Enter total spending (RM): "))
            break  # Exit loop if input is valid
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

    # Calculate loyalty points based on spending
    loyalty_points = int(total_spending * BASE_POINTS_PER_RM)  # Assume points based on spending

    # Determine status and redeem rate
    status = determine_status(loyalty_points)  # Determine status based on points
    redeem_rate = REDEEM_RATES[status]  # Get redeem rate based on status

    new_customer_info = {
        "username": username,
        "total_spending (RM)": total_spending,
        "loyalty_points": loyalty_points,
        "status": status,
        "redeem_rate (RM)": redeem_rate
    }

    # Load existing customers and add the new one
    customers = load_customer_data()
    customer_id = str(len(customers) + 1)  # Create a new customer ID
    customers[customer_id] = new_customer_info

    # Save updated customer data
    save_customer_data(customers)
    print(f"New customer {username} loyalty rewards created successfully!")


def update_customer_loyalty_information(username):
    """Function to update customer information."""
    customers = load_customer_data()
    for customer_id, customer_info in customers.items():
        if customer_info['username'] == username:
            print("\n-- Update Customer Information --")

            # Input total spending with validation
            while True:
                try:
                    total_spending = float(input("Enter new total spending (RM): "))
                    break  # Exit loop if input is valid
                except ValueError:
                    print("Invalid input! Please enter a numeric value.")

            # Input loyalty points with validation
            while True:
                try:
                    loyalty_points = int(input("Enter new loyalty points: "))
                    break  # Exit loop if input is valid
                except ValueError:
                    print("Invalid input! Please enter an integer value.")

            # Automatically determine new status based on updated points
            status = determine_status(loyalty_points)
            redeem_rate = REDEEM_RATES[status]  # Get redeem rate based on updated status

            # Update customer information
            customer_info['total_spending (RM)'] = total_spending
            customer_info['loyalty_points'] = loyalty_points
            customer_info['status'] = status
            customer_info['redeem_rate (RM)'] = redeem_rate  # Update redeem rate

            # Save changes
            save_customer_data(customers)  # Save updated customer data
            print(f"Customer information for {username} has been updated.")
            break
    else:
        print(f"User {username} not found. No update performed.")


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

                # Update customer info in the file
                update_customer_info(username, customer_info)  # Update the existing customer data
            else:
                print("|⚠️Invalid number of vouchers!|")
        else:
            print("No vouchers redeemed.")
    else:
        print(f"Your points are not enough! You need at least {points_per_voucher} points per voucher.")


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
        print(f"User {username} does not exist. Creating new user...")
        create_new_customer()  # Create a new customer if not found


def loyalty_rewards():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\tCUSTOMER LOYALTY REWARDS')
        print('-----------------------------------------------')
        print()
        print("1. View and Redeem Loyalty Rewards")
        print("2. Update Customer Loyalty Information")
        print("3. Create New Customer")  # Added option for creating new customer
        print("4. Exit to main menu")

        choice = input("Select your option: ")

        if choice == '1':
            view_loyalty_rewards()
        elif choice == '2':
            username = input("Enter your username: ").strip()  # Prompt for username
            update_customer_loyalty_information(username)  # Call the update function
        elif choice == '3':
            create_new_customer()  # Call the function to create a new customer
        elif choice == '4':
            print("Thank you for visiting Customer Loyalty Program. Goodbye!")
            break
        else:
            print("|⚠️Invalid option! Please try again.|")


# Start the loyalty rewards program
# loyalty_rewards()

