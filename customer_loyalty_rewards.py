import json

# Function to update purchase history
# Constants for points and rewards in RM
BASE_POINTS_PER_RM = 10  # Points earned per RM spent
BRONZE_REQUIREMENT = 10000  # Points needed for Bronze status
SILVER_REQUIREMENT = 20000  # Points needed for Silver status
GOLD_REQUIREMENT = 40000  # Points needed for Gold status
FREE_SHIPPING_THRESHOLD = 25000  # Points needed for free shipping
DISCOUNT_PURCHASE_COUNT = 5  # Every 5 purchases earn a discount
FREE_ITEM_THRESHOLD = 100  # Total spending amount needed for a free item


def load_customer_loyalty_rewards():
    try:
        file = open('baker_product_keeping.txt', 'r')  # open the file and read
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


def calculate_points(transaction_value):  # Calculate points earned based on the transaction history
    points_earned = transaction_value * BASE_POINTS_PER_DOLLAR
    print(f"Points earned for RM{transaction_value} purchase: {points_earned}")
    return points_earned


def update_loyalty_status(points_balance):
    """Update the loyalty status based on points balance."""
    if points_balance >= GOLD_REQUIREMENT:
        return "Gold"
    elif points_balance >= SILVER_REQUIREMENT:
        return "Silver"
    elif points_balance >= BRONZE_REQUIREMENT:
        return "Bronze"
    else:
        return "Standard"


def check_free_shipping(points_balance):
    """Check if the customer is eligible for free shipping."""
    if points_balance >= FREE_SHIPPING_THRESHOLD:
        print("You are eligible for free shipping!")
        # Implement the logic for sending a reward (e.g., send_reward_coupon())


def update_purchase_history(username, purchase_amount):
    """Update customer's purchase history and calculate rewards."""
    customers = load_customer_data()

    if username in customers:
        customer = customers[username]
        customer['total_spent'] += purchase_amount
        customer['purchase_count'] += 1
    else:
        customer = {
            'total_spent': purchase_amount,
            'purchase_count': 1
        }

    # Apply rewards based on purchase count and total spending amount
    if customer['purchase_count'] % DISCOUNT_PURCHASE_COUNT == 0:
        print("Congratulations! You've earned a 10% discount.")

    if customer['total_spent'] >= FREE_ITEM_THRESHOLD:
        print("Congratulations! You've earned a free item.")

    # Update customer data and save it
    customers[username] = customer
    save_customer_data(customers)


def view_loyalty_rewards():
    """Allow customers to view their loyalty rewards."""
    username = input("Enter your username: ")
    customers = load_customer_data()
    if username in customers:
        customer = customers[username]
        print(f"Customer {username} has {customer['purchase_count']} purchases and total spent RM{customer['total_spent']}.")
        # Implement additional logic to display the customer's current rewards
    else:
        print("Customer not found.")



