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


# Define the function that saves customers' orders data to the file
def save_reviews(new_review):
    file = open('customer_reviews.txt', 'w')  # open the file to write
    json.dump(new_review, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


review = load_review()


# Validate that the rating input is a valid number between 1 and 5
def validation_rating(rating):
    try:
        if rating.isdigit() and int(rating) in range(1, 6):
            return True
        else:
            return False
    except ValueError:
        return False


# Allow the customer to submit a review for a product they purchased
def submit_review():
    print('\n-----------------------------------------------')
    print('\t\t\t', '', 'PRODUCT REVIEW')
    print('-----------------------------------------------')

    # Collect details from the customer
    username = input('Enter your username: ')
    product_name = input('Enter the product name: ')
    review_text = input('Enter your review: ')
    rating = input('Rate your product (1-5): ')

    # Validate the rating to ensure it's between 1 and 5
    if not validation_rating(rating):
        print('|⚠️Invalid rating. Please enter a number between 1 and 5!|')
        rating = input('Rate your product (1-5): ')

    # Create a dictionary to store the customer's review details
    review[username] = {
        'product_name': product_name,
        'review': review_text,
        'rating': int(rating)
    }

    # Save the new review
    save_reviews(review)
    print()
    print('***** Thank you for your feedback! *****')
    print('Your review has been successfully received.')


#submit_review()