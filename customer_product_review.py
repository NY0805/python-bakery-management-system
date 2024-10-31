import json


# Load the reviews from 'customer_reviews.txt'
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


def save_reviews(new_reviews):
    # Save the updated reviews back to 'customer_reviews.txt'
    with open('customer_reviews.txt', 'w') as file:
        json.dump(new_reviews, file, indent=4)


def load_order_list():
    # Load the order list from 'customer_order_list.txt'
    try:
        file = open('customer_order_list.txt', 'r')  # open the file and read
        content = file.read().strip()  # strip() function is used to strip any unnecessary whitespaces
        file.close()  # close the file after reading
        if content:  # start to check if the file is not empty
            try:
                return json.loads(content)  # parse the content as json format into python dictionary
            except json.JSONDecodeError:
                return {}  # return empty dictionary if the content does not parse successfully
        else:
            return {}  # return empty dictionary if the file is empty
    except FileNotFoundError:
        return {}  # return empty dictionary if the file does not exist


def validation_rating(rating):
    # Check if the rating is a valid integer between 1 and 5
    return rating.isdigit() and int(rating) in range(1, 6)


def submitted_review(logged_in_username):
    print('\n-----------------------------------------------')
    print('\t\t\tPRODUCT REVIEW')
    print('-----------------------------------------------')

    order_list = load_order_list()
    recent_purchases = []
    order_date = None

    # Check the user's purchase history
    for order_data in order_list.values():
        if order_data["username"] == logged_in_username and order_data["status"] == "Payment Completed":
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
    print('')

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

    # Generate a unique review ID (incremental)
    next_review_id = str(len(reviews) + 1).zfill(3)

    # Add the new review entry under the generated review ID
    reviews[next_review_id] = {
        'username': logged_in_username,
        'product_name': product_name,
        'review': review_text,
        'rating': int(rating),
        'order_date': order_date
    }

    save_reviews(reviews)
    print('\n***** Thank you for your feedback! *****')
    print('Your review has been successfully received.')


#submitted_review