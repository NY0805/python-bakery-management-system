import json

# Constants for points and rewards in RM
BASE_POINTS_PER_RM = 10  # Points earned per RM spent
BRONZE_REQUIREMENT = 500  # Points needed for Bronze status
SILVER_REQUIREMENT = 1000  # Points needed for Silver status
GOLD_REQUIREMENT = 2000  # Points needed for Gold status

# Constants for discount per point based on loyalty status
DISCOUNT_PER_POINT = {
    "MORNING GLORY'S GOLD": 0.10,  # Gold users get RM0.10 discount per point
    "MORNING GLORY'S SILVER": 0.05,  # Silver users get RM0.05 discount per point
    "MORNING GLORY'S BRONZE": 0.02,  # Bronze users get RM0.02 discount per point
    "Standard": 0  # Standard users get no discount
}


def load_customer_data():
    try:
        with open('customer_loyalty_rewards.txt', 'r') as file:  # Use 'with' for better file handling
            content = file.read().strip()  # Strip any unnecessary whitespaces
            if content:  # Check if the file is not empty
                try:
                    return json.loads(content)  # Parse content as JSON
                except json.JSONDecodeError:
                    return {}  # Return empty dict if parsing fails
            else:
                return {}  # Return empty dict if the file is empty
    except FileNotFoundError:
        return {}  # Return empty dict if the file does not exist


def save_customer_data(customers):
    with open('customer_loyalty_rewards.txt', 'w') as file:
        json.dump(customers, file, indent=4)


def view_loyalty_rewards():
    username = input("Enter your username: ").strip().lower()  # Strip whitespace and convert to lowercase
    customers = load_customer_data()  # Load the customer data

    # Initialize a flag to check if a matching customer is found
    customer_found = False

    print('\n --Loyalty Rewards Information-- ')
    print()

    # Loop through all customer records
    for customer_id, customer_info in customers.items():
        # If a matching username is found
        if customer_info.get('username', '').strip().lower() == username:
            print(f"{'Username:'.ljust(25)} {customer_info['username']}")
            print('─' * 47)
            print(f"{'Total Spending (RM):'.ljust(25)} {customer_info['total_spending (RM)']:.2f}")
            print(f"{'Loyalty Points:'.ljust(25)} {customer_info['loyalty_points']}")
            print(f"{'Status:'.ljust(25)} {customer_info['status']}")
            print(f"{'Discount per Point (RM):'.ljust(25)} {customer_info['discount_per_point (RM)']:.2f}")
            customer_found = True
            break

    if not customer_found:
        # If no matching username is found
        print("|⚠️Customer cannot be found!|")

    print('-' * 85 + '\n')


def loyalty_rewards():
    while True:
        print('\n-----------------------------------------------')
        print('\t\t\t', '', 'CUSTOMER LOYALTY REWARDS')
        print('-----------------------------------------------')
        print()
        print("1. View Loyalty Rewards")
        print("2. Exit to main menu")

        choice = input("Select your option:  ")

        if choice == '1':
            view_loyalty_rewards()

        elif choice == '2':
            print("Thank you for visiting Customer Loyalty Program. Goodbye!")
            break

        else:
            print("|⚠️Invalid option! Please try again.|")


#loyalty_rewards()
