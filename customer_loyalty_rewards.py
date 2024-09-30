import json

# Constants for points and rewards in RM
BASE_POINTS_PER_RM = 10  # Points earned per RM spent
BRONZE_REQUIREMENT = 10000  # Points needed for Bronze status
SILVER_REQUIREMENT = 20000  # Points needed for Silver status
GOLD_REQUIREMENT = 40000  # Points needed for Gold status
FREE_SHIPPING_THRESHOLD = 25000  # Points needed for free shipping
DISCOUNT_PURCHASE_COUNT = 5  # Every 5 purchases earn a discount
FREE_ITEM_THRESHOLD = 100  # Total spending amount needed for a free item


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


def calculate_points(transaction_value):  # Calculate points earned based on the transaction history
    points_earned = transaction_value * BASE_POINTS_PER_RM
    print(f"Points earned for RM{transaction_value} purchase: {points_earned}")
    return points_earned


def update_loyalty_status(points_balance):  # Update the loyalty status based on points balance
    if points_balance >= GOLD_REQUIREMENT:
        return "Gold"
    elif points_balance >= SILVER_REQUIREMENT:
        return "Silver"
    elif points_balance >= BRONZE_REQUIREMENT:
        return "Bronze"
    else:
        return "Standard"


def check_free_shipping(points_balance):  # Check if the customer is eligible for free shipping
    if points_balance >= FREE_SHIPPING_THRESHOLD:
        print("You are eligible for free shipping!")


def update_purchase_history(username, purchase_amount):  # Update customer's purchase history and calculate rewards
    customers = load_customer_data()
    points_earned = calculate_points(purchase_amount)

    if username in customers:
        customer = customers[username]
        customer['total_spending (RM)'] += purchase_amount  # Update total spending
        customer['purchase_count'] += 1
        customer['loyalty_points'] += points_earned
    else:
        customer = {
            'total_spending (RM)': purchase_amount,  # Initial total spending
            'purchase_count': 1,
            'loyalty_points': points_earned
        }

    # Update customer data
    customers[username] = customer
    save_customer_data(customers)

    # Apply rewards based on purchase count and total spending amount
    if customer['purchase_count'] % DISCOUNT_PURCHASE_COUNT == 0:
        print("Congratulations! You've earned a 10% discount.")

    if customer['total_spending (RM)'] >= FREE_ITEM_THRESHOLD:
        print("Congratulations! You've earned a free item.")


def view_loyalty_rewards():  # Allow customers to check their loyalty rewards
    username = input("Enter your username: ")
    customers = load_customer_data()
    if username in customers:
        customer = customers[username]
        print(f"Customer {username} has {customer['purchase_count']} purchases and total spending (RM) {customer['total_spending (RM)']}.")
        print(f"Loyalty points: {customer['loyalty_points']}")
    else:
        print("|⚠️Customer cannot be found!|")


def loyalty_rewards():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'CUSTOMER LOYALTY REWARDS')
        print('-----------------------------------------------')
        print()
        print("1. Update Purchase History")
        print("2. View Loyalty Rewards")
        print("3. Exit to main menu")

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
            print("Thank you for using the Customer Loyalty Program. Goodbye!")
            break

        else:
            print("|⚠️Invalid option! Please try again.|")




