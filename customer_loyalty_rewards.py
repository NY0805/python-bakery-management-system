import json

# Constants for loyalty program
BASE_POINTS_PER_RM = 10  # Points earned per RM spent
GOLD_REQUIREMENT = 2000
SILVER_REQUIREMENT = 1000
BRONZE_REQUIREMENT = 500
REDEEM_RATES = {
    "MORNING GLORY'S GOLD": 100,
    "MORNING GLORY'S SILVER": 90,
    "MORNING GLORY'S BRONZE": 80,
    "Standard": None
}


def determine_loyalty_points(total_price):
    # Calculate loyalty points based on total price
    points = int(total_price * BASE_POINTS_PER_RM)
    return points


def update_customer_status(points):
    # Determine customer status based on points
    if points >= GOLD_REQUIREMENT:
        return "MORNING GLORY'S GOLD"
    elif points >= SILVER_REQUIREMENT:
        return "MORNING GLORY'S SILVER"
    elif points >= BRONZE_REQUIREMENT:
        return "MORNING GLORY'S BRONZE"
    else:
        return "Standard"  # Match your file's terminology


def load_customer_data():
    # Load customer data from customer.txt
    try:
        with open("customer.txt", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_customer_data(data):
    # Save updated customer data to txt
    with open("customer.txt", "w") as file:
        json.dump(data, file, indent=4)


def update_customer_loyalty_points(customer_name, points_change):
    """Update the loyalty points for a specific customer."""
    try:
        with open("customer.txt", "r") as file:
            customer_data = json.load(file)

        # Update the loyalty points for the specific customer
        for customer_id, customer in customer_data.items():
            if customer['customer_username'] == customer_name:
                # Calculate new loyalty points
                customer['loyalty_points'] += points_change  # Update points
                # Determine new status
                new_status = update_customer_status(customer['loyalty_points'])
                if new_status != customer['status']:
                    print(f"Updating status from {customer['status']} to {new_status}")
                    customer['status'] = new_status  # Update the status
                break

        # Save the updated customer data back to the customer.txt file
        save_customer_data(customer_data)

        print("Updated customer data saved to customer.txt.")

        # Now update the customer_loyalty_rewards.txt file
        update_loyalty_rewards(customer_name, points_change, new_status)

    except FileNotFoundError:
        print("Customer file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from customer.txt.")
    except Exception as e:
        print(f"An error occurred: {e}")


def update_loyalty_rewards(username, points_change, new_status):
    """Update loyalty rewards for the given username."""
    rewards = load_loyalty_rewards()  # Load current loyalty rewards

    for order_id, history in rewards.items():
        if history['username'] == username:
            # Update the loyalty points and status
            history['loyalty_points'] += points_change
            history['status'] = new_status  # Update the status
            break

    # Save the updated loyalty rewards back to the file
    save_loyalty_rewards(rewards)
    print("Updated loyalty rewards saved to customer_loyalty_rewards.txt.")


def load_loyalty_rewards():
    """Load customer loyalty rewards data from a file."""
    try:
        with open('customer_loyalty_rewards.txt', 'r') as file:
            content = file.read().strip()
            if content:
                return json.loads(content)
            else:
                return {}
    except FileNotFoundError:
        return {}


def save_loyalty_rewards(rewards):
    """Save customer loyalty rewards data to a file."""
    with open('customer_loyalty_rewards.txt', 'w') as file:
        json.dump(rewards, file, indent=4)


def log_redeem_history(username, total_spend, points_earned, status):
    """Log the redeem history for a customer."""
    rewards = load_loyalty_rewards()
    order_id = f"ORD{len(rewards) + 1:03d}"  # Generate a new order ID
    rewards[order_id] = {
        'username': username,
        'total_spending (RM)': total_spend,
        'loyalty_points': points_earned,  # Ensure this key is always set
        'status': status,
        'redeem_rate (RM)': REDEEM_RATES.get(status, 'N/A'),
        'voucher_redeem': total_spend // 10  # Assuming each RM10 gives 1 voucher
    }
    save_loyalty_rewards(rewards)


def redeem_cash_voucher(username):
    """Allow customer to redeem cash vouchers using their loyalty points."""
    rewards = load_loyalty_rewards()  # Load current loyalty rewards

    for order_id, history in rewards.items():
        if history['username'] == username:
            points = history['loyalty_points']
            status = history['status']
            points_per_voucher = REDEEM_RATES.get(status)

            if points_per_voucher is None:
                print("Standard users cannot redeem cash vouchers.")
                return

            max_vouchers = points // points_per_voucher  # Calculate the maximum number of vouchers
            if max_vouchers > 0:
                print(f"\nYou have {points} loyalty points.")
                print(f"As a {status} member, you can redeem up to {max_vouchers} cash vouchers (Each RM10).")
                choice = input("Would you like to redeem your points for cash vouchers? (yes=y, no=n): ").lower()

                if choice == 'y':
                    try:
                        num_vouchers = int(input(f"How many vouchers would you like to redeem (up to {max_vouchers})? "))
                        if 0 < num_vouchers <= max_vouchers:
                            total_points_deducted = num_vouchers * points_per_voucher
                            history['loyalty_points'] -= total_points_deducted
                            print(f"Success! You have redeemed {num_vouchers} voucher(s) worth RM{num_vouchers * 10}.")

                            # Update the loyalty rewards file
                            rewards[order_id]['loyalty_points'] = history['loyalty_points']
                            rewards[order_id]['voucher_redeem'] = num_vouchers  # Log vouchers redeemed
                            save_loyalty_rewards(rewards)

                            # Save the updated customer data
                            customers = load_customer_data()
                            for customer_id, info in customers.items():
                                if info['customer_username'] == username:
                                    customers[customer_id]['loyalty_points'] = history['loyalty_points']  # Update points
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
            return

    print(f"User {username} does not exist in loyalty rewards.")


def view_loyalty_rewards(username):
    # Display loyalty rewards information for a specific user
    rewards = load_loyalty_rewards()  # Load from customer_loyalty_rewards.txt

    # Check if the username exists in the rewards data
    user_rewards = [reward for order_id, reward in rewards.items() if reward['username'] == username]

    if user_rewards:
        print('\n --Loyalty Rewards Information-- ')
        print()
        print("\n--Redeem History--")
        print('-' * 150)
        header = f"{'Order ID':<10} | {'Total Spending (RM)':<20} | {'Points Earned':<15} | {'Status':<20} | {'Redeem Rate (RM)':<15} | {'Vouchers Redeemed':<15}"
        print(header)
        print('-' * 150)
        # Display the values in aligned format
        for order_id, r in rewards.items():
            if r['username'] == username:
                points_earned = r.get('loyalty_points', '-')
                voucher_redeemed = r.get('voucher_redeem', '-')
                status = r.get('status', '-')  # Get status to avoid KeyError
                redeem_rate = r.get('redeem_rate (RM)', '-')  # Get redeem rate to avoid KeyError
                print(
                    f"{order_id:<10} | {r['total_spending (RM)']:<20} | {points_earned:<15} | {status:<20} | {redeem_rate:<15} | {voucher_redeemed:<15}")

        print('-' * 150)
    else:
        print(f"No loyalty rewards found for username: {username}")


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
            username = input("Enter your username: ").strip()
            view_loyalty_rewards(username)

        elif choice == '2':
            username = input("Enter your username: ").strip()
            redeem_cash_voucher(username)

        elif choice == '3':
            print("Thank you for visiting the Customer Loyalty Program. Goodbye!")
            break

        else:
            print("|⚠️ Invalid option! Please try again.|")


loyalty_rewards()
