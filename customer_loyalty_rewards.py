import json

# Constants for the loyalty program
BASE_POINTS_PER_RM = 10  # Points earned per RM spent
GOLD_REQUIREMENT = 2000
SILVER_REQUIREMENT = 1000
BRONZE_REQUIREMENT = 500
REDEEM_RATES = {
    "MORNING GLORY'S GOLD": 800,
    "MORNING GLORY'S SILVER": 900,
    "MORNING GLORY'S BRONZE": 1000,
    "MORNING GLORY'S STANDARD": 0
}
# Each cash voucher is worth RM10 in the loyalty program


# Function to calculate loyalty points based on customer's total spending
def determine_loyalty_points(total_price):
    # Check if total_price is a number
    if not isinstance(total_price, (int, float)):
        print(f"Invalid total price: {total_price} (must be a number)")
        return None

    # Calculate loyalty points
    points = int(total_price * BASE_POINTS_PER_RM)
    return points


# Determine customer status based on their loyalty points
def update_customer_status(points):
    if points >= GOLD_REQUIREMENT:
        return "MORNING GLORY'S GOLD"
    elif points >= SILVER_REQUIREMENT:
        return "MORNING GLORY'S SILVER"
    elif points >= BRONZE_REQUIREMENT:
        return "MORNING GLORY'S BRONZE"
    else:
        return "MORNING GLORY'S STANDARD"


def load_customer_data():
    try:
        file = open('customer.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(
                    content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


def save_customer_data(data): # Save customer data to the customer.txt file
    with open("customer.txt", "w") as file:
        json.dump(data, file, indent=4)


# Load customer loyalty rewards data from the file
def load_loyalty_rewards():
    try:
        file = open('customer_loyalty_rewards.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(
                    content)  # parse the content as json format into python dictionary and return the content if successfully parsed
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


def save_loyalty_rewards(rewards): # Save customer loyalty rewards data to the file
    with open('customer_loyalty_rewards.txt', 'w') as file:
        json.dump(rewards, file, indent=4)


# Function to update customer loyalty points and status during the payment process based on total spending
def process_payment(username, total_price):
    rewards = load_loyalty_rewards()
    customers = load_customer_data()

    # Ensure total_price is a valid number
    try:
        total_price = float(total_price)
    except ValueError:
        print(f"|⚠️Error: total_price must be a valid number, got {total_price}|")
        return

    # Check if user exists in customer_loyalty_rewards.txt file
    user_rewards = [order_id for order_id, data in rewards.items() if data['username'] == username]

    # Determine new loyalty points
    points_change = determine_loyalty_points(total_price)

    if not user_rewards:
        # Initialize new customer data in customer_loyalty_rewards.txt`file
        new_order_id = str(len(rewards) + 1)  # Generate a new order ID
        rewards[new_order_id] = {
            "username": username,
            "total_spending (RM)": total_price,
            "loyalty_points": points_change,
            "status": "MORNING GLORY'S STANDARD",
            "redeem_rate (RM)": REDEEM_RATES["MORNING GLORY'S STANDARD"],
            "voucher_redeem": 0,
            "redeem_history": []
        }
        print(f"New user {username} added to loyalty rewards.")

        # Update customer.txt file with new loyalty points
        if username in customers:
            customers[username]['loyalty_points'] = rewards[new_order_id]['loyalty_points']
            save_customer_data(customers)
            print("Customer loyalty points updated in customer.txt.")

    else:
        # Update the total spending and loyalty points for existing customer
        for order_id in user_rewards:
            history = rewards[order_id]
            history['total_spending (RM)'] += total_price
            history['loyalty_points'] += points_change

            # Update customer status and redeem rate
            new_status = update_customer_status(history['loyalty_points'])
            history['status'] = new_status
            history['redeem_rate (RM)'] = REDEEM_RATES.get(new_status, 0)

            # Update customer.txt file with the new points
            if username in customers:
                customers[username]['loyalty_points'] = history['loyalty_points']
                save_customer_data(customers)
            break

    # Save updated loyalty rewards
    save_loyalty_rewards(rewards)


def update_customer_loyalty_points(customer_name, points_change): # Update loyalty points for customer
    try:
        with open("customer.txt", "r") as file:
            customer_data = json.load(file)

        for customer_id, customer in customer_data.items():
            if customer['customer_username'] == customer_name:
                customer['loyalty_points'] += points_change
                new_status = update_customer_status(customer['loyalty_points'])
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
            if 'redeem_rate (RM)' not in history or history['redeem_rate (RM)'] == 0:
                history['redeem_rate (RM)'] = REDEEM_RATES.get(new_status, 0)
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


def redeem_history(username, total_spend, points_earned, status):
    rewards = load_loyalty_rewards()
    order_id = f"ORD{len(rewards) + 1:03d}"  # Generate a new order ID
    rewards[order_id] = {
        'username': username,
        'total_spending (RM)': total_spend,
        'loyalty_points': points_earned,
        'status': status,
        'redeem_rate (RM)': REDEEM_RATES.get(status, 'N/A'),
        'voucher_redeem': total_spend // 10  # Assuming each RM10 gives 1 voucher
    }
    save_loyalty_rewards(rewards)


def view_loyalty_rewards(username): # Display loyalty rewards information for customer
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
        for order_id, r in rewards.items():
            if r['username'] == username:
                points_earned = r.get('loyalty_points', '-')
                voucher_redeemed = r.get('voucher_redeem', '-')
                status = r.get('status', '-')
                redeem_rate = r.get('redeem_rate (RM)', '-')
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



