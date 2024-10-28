import json

# Constants for the loyalty program
BASE_POINTS_PER_RM = 10  # Points earned per RM spent
GOLD_REQUIREMENT = 2000
SILVER_REQUIREMENT = 1000
BRONZE_REQUIREMENT = 500
REDEEM_RATES = {
    "MORNING GLORY'S GOLD": 1000,
    "MORNING GLORY'S SILVER": 900,
    "MORNING GLORY'S BRONZE": 800,
    "Standard": None               # Standard customers cannot redeem points
}
# Each cash voucher is worth RM10 in the loyalty program


def determine_loyalty_points(total_price):  # Calculate loyalty points based on customer's total spending
    # Ensure total_price is a number
    if not isinstance(total_price, (int, float)):
        raise ValueError(f"Invalid total price: {total_price} (must be a number)")

    # Calculate loyalty points
    points = int(total_price * BASE_POINTS_PER_RM)
    return points  # Directly return points


def update_customer_status(points): # Determine customer status based on their loyalty points
    if points >= GOLD_REQUIREMENT:
        return "MORNING GLORY'S GOLD"
    elif points >= SILVER_REQUIREMENT:
        return "MORNING GLORY'S SILVER"
    elif points >= BRONZE_REQUIREMENT:
        return "MORNING GLORY'S BRONZE"
    else:
        return "Standard"


def load_customer_data(): # Load customer data from the customer.txt file
    try:
        with open("customer.txt", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_customer_data(data): # Save customer data to the customer.txt file
    with open("customer.txt", "w") as file:
        json.dump(data, file, indent=4)


def load_loyalty_rewards(): # Load customer loyalty rewards data from the customer_loyalty_rewards.txt file
    try:
        with open('customer_loyalty_rewards.txt', 'r') as file:
            content = file.read().strip()
            if content:
                return json.loads(content)
            else:
                return {}
    except FileNotFoundError:
        return {}


def save_loyalty_rewards(rewards): # Save customer loyalty rewards data to the customer_loyalty_rewards.txt file
    with open('customer_loyalty_rewards.txt', 'w') as file:
        json.dump(rewards, file, indent=4)


def process_payment(username, total_price):  # Process payment and update the user's loyalty points and status
    rewards = load_loyalty_rewards()  # Load loyalty rewards data
    customers = load_customer_data()  # Load customer data

    # Ensure total_price is a valid number
    try:
        total_price = float(total_price)
    except ValueError:
        print(f"|⚠️Error: total_price must be a valid number, got {total_price}|")
        return

    # Check if user exists in customer_loyalty_rewards.txt
    user_rewards = [order_id for order_id, data in rewards.items() if data['username'] == username]

    if not user_rewards:
        # New user, initialize their data in customer_loyalty_rewards.txt
        new_order_id = str(len(rewards) + 1)  # Generate a new order ID
        rewards[new_order_id] = {
            "username": username,
            "total_spending (RM)": total_price,
            "loyalty_points": determine_loyalty_points(total_price),  # Directly use the return value
            "status": "MORNING GLORY'S STANDARD",
            "redeem_rate (RM)": 0,
            "voucher_redeem": 0,
            "redeem_history": []
        }
        print(f"New user {username} added to loyalty rewards.")

        # Also update customer.txt with new loyalty points
        if username in customers:
            customers[username]['loyalty_points'] = rewards[new_order_id]['loyalty_points']
            save_customer_data(customers)
            print("Customer loyalty points updated in customer.txt.")

    else:
        # Existing user, update their spending and loyalty points
        for order_id in user_rewards:  # Only iterate over user's orders
            history = rewards[order_id]
            points_change = determine_loyalty_points(total_price)  # Get points change directly
            history['total_spending (RM)'] += total_price
            history['loyalty_points'] += points_change  # Correctly update points

            # Update customer.txt with the new points
            if username in customers:
                customers[username]['loyalty_points'] = history['loyalty_points']
                save_customer_data(customers)
                print("Customer loyalty points updated in customer.txt.")
            break  # No need to continue once we've updated

    # Save updated loyalty rewards
    save_loyalty_rewards(rewards)
    print("Order placed. Please proceed to payment for the receipt.")


def update_customer_loyalty_points(customer_name, points_change): # Update loyalty points for a specific customer
    try:
        with open("customer.txt", "r") as file:
            customer_data = json.load(file)

        for customer_id, customer in customer_data.items():
            if customer['customer_username'] == customer_name:
                customer['loyalty_points'] += points_change
                new_status = update_customer_status(customer['loyalty_points'])
                if new_status != customer['status']:
                    print(f"Updating status from {customer['status']} to {new_status}")
                    customer['status'] = new_status
                break

        save_customer_data(customer_data)
        update_loyalty_rewards(customer_name, points_change, new_status)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")


def update_loyalty_rewards(username, points_change, new_status): # Update loyalty rewards for a user
    rewards = load_loyalty_rewards()

    for order_id, history in rewards.items():
        if history['username'] == username:
            history['loyalty_points'] += points_change
            history['status'] = new_status
            break

    save_loyalty_rewards(rewards)
    print("Loyalty rewards updated.")


def redeem_cash_voucher(username): # Allow customers to redeem cash vouchers using loyalty points
    rewards = load_loyalty_rewards()

    for order_id, history in rewards.items():
        if history['username'] == username:
            points = history['loyalty_points']
            status = history['status']
            points_per_voucher = REDEEM_RATES.get(status)

            if points_per_voucher is None:
                print("Standard users cannot redeem cash vouchers.")
                return

            max_vouchers = points // points_per_voucher # Each cash voucher is worth RM10 in the loyalty program
            if max_vouchers > 0:
                print(f"You have {points} loyalty points.")
                print(f"As a {status} member, you can redeem up to {max_vouchers} vouchers (Each RM10).")
                choice = input("Would you like to redeem vouchers? (yes=y, no=n): ").lower()

                if choice == 'y':
                    try:
                        num_vouchers = int(input(f"How many vouchers? (up to {max_vouchers}): "))
                        if 0 < num_vouchers <= max_vouchers:
                            total_points_deducted = num_vouchers * points_per_voucher
                            history['loyalty_points'] -= total_points_deducted
                            print(f"Success! Redeemed {num_vouchers} voucher(s) worth RM{num_vouchers * 10}.")

                            if 'voucher_redeem' not in history:
                                history['voucher_redeem'] = 0
                            history['voucher_redeem'] += num_vouchers

                            if 'redeem_history' not in history:
                                history['redeem_history'] = []
                            history['redeem_history'].append({
                                'redeem_count': num_vouchers,
                                'points_used': total_points_deducted,
                                'remaining_points': history['loyalty_points']
                            })

                            rewards[order_id]['loyalty_points'] = history['loyalty_points']
                            rewards[order_id]['voucher_redeem'] = history['voucher_redeem']
                            save_loyalty_rewards(rewards)

                            customers = load_customer_data()
                            for customer_id, info in customers.items():
                                if info['customer_username'] == username:
                                    customers[customer_id]['loyalty_points'] = history['loyalty_points']
                                    save_customer_data(customers)
                                    break
                        else:
                            print("Invalid number of vouchers.")
                    except ValueError:
                        print("Invalid input.")
                else:
                    print("No vouchers redeemed.")
            else:
                print(f"|⚠️Not enough points. You need {points_per_voucher} points per voucher.|")
            return

    print(f"User {username} does not exist in the loyalty rewards system.")


def log_redeem_history(username, total_spend, points_earned, status): # Log the redeem history for a customer
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


def view_loyalty_rewards(username): #Display loyalty rewards information for a specific user
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
                # Display redemption history

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


#loyalty_rewards()
