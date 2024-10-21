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

    # Initialize variables to check for valid purchase and product name
    valid_purchase_found = False
    product_name = None

    # Load the order list from 'customer_order_list.txt' to check the user's purchase history
    order_list = load_order_list()

    # Check if the user has completed any purchases
    for order_id, order_data in order_list.items():  # Use .items() method to iterate through the dictionary
        if order_data["username"] == logged_in_username:  # Match the current order with the logged-in user's username
            if order_data["status"] == "Order Placed":
                valid_purchase_found = True
                order_date = order_data['order_date']
                product_name = order_data['items_ordered'][0]  # Get the first product name
                review_text = input('Enter your review: ')
                rating = input('Rate your product (1-5): ')
                break  # Exit the loop after finding a valid order

    # Check if no valid purchase was found
    if not valid_purchase_found:  # Use if instead of else if
        print('|⚠️ You have not completed any purchases. Please buy something before writing a review!|')
        return

    # Load existing reviews
    reviews = load_review()

    # Update the review for the user
    reviews[logged_in_username] = {
        'product_name': product_name,
        'review': review_text,
        'rating': int(rating),  # Convert rating to an integer
        'order_date': order_date
    }

    # Save the updated reviews
    save_reviews(reviews)
    print()
    print('***** Thank you for your feedback! *****')
    print('Your review has been successfully received.')

    reviews = load_review()

    # Save the updated reviews
    save_reviews(reviews)
    print()
    print('***** Thank you for your feedback! *****')
    print('Your review has been successfully received.')  # Display the message after the review has been saved


#submit_review