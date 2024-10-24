import json


def load_review():
    try:
        file = open('customer_reviews.txt', 'r')  # open the file and read
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


def save_reviews(new_review):
    with open('customer_reviews.txt', 'w') as file:
        json.dump(new_review, file, indent=4)


def load_order_list():
    try:
        file = open('customer_order_list.txt', 'r')  # open the file and read
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


def validation_rating(rating):
    return rating.isdigit() and int(rating) in range(1, 6)


def submit_review(logged_in_username):
    print('\n-----------------------------------------------')
    print('\t\t\tPRODUCT REVIEW')
    print('-----------------------------------------------')

    order_list = load_order_list()
    recent_purchases = []
    order_date = None

    # Check the user's purchase history
    for order_data in order_list.values():
        if order_data["username"] == logged_in_username and order_data["status"] == "Order Placed":
            recent_purchases.extend(order_data['items_ordered'])
            order_date = order_data['order_date']

    if not recent_purchases:
        print('|⚠️ You have not completed any purchases. Please buy something before writing a review!|')
        return

    # Display recent purchases
    print("Your recent purchases:")
    print(f"{'No.':<5} {'Product Name':<30} {'Quantity':<10}")
    print('-' * 60)

    for i, product in enumerate(recent_purchases, start=1):
        product_name, quantity = product.split(' x ')
        print(f"{i:<5} {product_name:<30} {quantity:<10}")

    try:
        product_choice = int(input('Select a product to review (enter the number): '))
        if not (1 <= product_choice <= len(recent_purchases)):
            print("Invalid selection. Please select a valid product number.")
            return
        product_name = recent_purchases[product_choice - 1].split(' x ')[0]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    review_text = input('Enter your review: ')
    rating = input('Rate your product (1-5): ')

    # Validate rating and prompt until valid input is received
    while not validation_rating(rating):
        print("Invalid rating. Please provide a rating between 1 and 5.")
        rating = input('Rate your product (1-5): ')

    reviews = load_review()

    # Ensure the user's reviews are a list
    if logged_in_username not in reviews:
        reviews[logged_in_username] = []  # Initialize as an empty list if the user does not exist
    elif not isinstance(reviews[logged_in_username], list):
        reviews[logged_in_username] = []  # Ensure it's a list, in case it was saved incorrectly

    # Append the new review
    reviews[logged_in_username].append({
        'product_name': product_name,
        'review': review_text,
        'rating': int(rating),
        'order_date': order_date
    })

    save_reviews(reviews)
    print('\n***** Thank you for your feedback! *****')
    print('Your review has been successfully received.')
#submit_review