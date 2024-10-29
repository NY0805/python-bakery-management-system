import json
import random
from customer_product_review import load_review


# Define the function that loads customers' orders data from the file
def load_data_from_manager_customer_feedback():
    try:
        file = open('manager_customer_feedback.txt', 'r')  # open the file and read
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


# Define the function that saves information to the file
def save_info(manager_response):
    file = open('manager_customer_feedback.txt', 'w')  # open the file to write
    json.dump(manager_response, file,indent=4)  # convert the dictionary into JSON format, 4 spaces indentation make it clearer for visualization
    file.close()  # close the file after writing


review = load_review()
manager_response = load_data_from_manager_customer_feedback()


# define the function to print content in the center within the width of 47 characters
def printed_centered(info):
    print('-' * 47)
    side_space = (47 - len(info)) // 2  # determine how much blank space to leave
    print(' ' * side_space + info + ' ' * (47 - len(info) - side_space))
    print('-' * 47)


# define the function to view customer feedback and reply to them
def customer_feedback():
    while True:
        # initialize the variables to 0, ready for the calculation later
        rating_five = 0
        rating_four = 0
        rating_three = 0
        rating_two = 0
        rating_one = 0

        # iterate through customer review, increase 1 to the respective variable
        for review_details in review.values():
            if review_details['rating'] == 5:
                rating_five += 1
            elif review_details['rating'] == 4:
                rating_four += 1
            elif review_details['rating'] == 3:
                rating_three += 1
            elif review_details['rating'] == 2:
                rating_two += 1
            else:
                rating_one += 1

        print('')
        printed_centered('CUSTOMER RATINGS OVERVIEW')
        print(f'{"⭐⭐⭐⭐⭐":<9}{"5-star rating:"} {rating_five}')
        print(f'{"⭐⭐⭐⭐":<10}{"4-star rating:"} {rating_four}')
        print(f'{"⭐⭐⭐":<11}{"3-star rating:"} {rating_three}')
        print(f'{"⭐⭐":<12}{"2-star rating:"} {rating_two}')
        print(f'{"⭐":<13}{"1-star rating:"} {rating_one}')

        choice = input('\nDo you want to view and reply to customer feedback? (y=yes, n=no)\n>>> ')
        if choice == 'y':  # if manager choose to view and reply to the feedback
            while True:
                # customer feedback will be display in table form
                print('\n\n', '\t'*17, 'CUSTOMER FEEDBACK')
                print('-' * 160)
                header = ['Review ID']  # create a list for headers and append the first item in the list
                for review_details in review.values():  # access the values of order_list
                    for sub_key, sub_value in review_details.items():  # access the subkey and sub value in the value of order_list
                        header.append(sub_key.title().replace('_', ' '))  # append other details of orders into the header list and replace all underscore with space to enhance readability
                    break

                print(f'{header[0]:<18}{header[1]:<19}{header[2]:<28}{header[3]:<88}{header[4]}')  # display the headers
                print('-' * 160)

                for user, review_details in review.items():
                    products = review_details['product_name'].split(', ')
                    print(f'{user:<18}{review_details["username"]:<19}{products[0]:<28}{review_details["review"]:<88}{review_details["rating"]}')
                    for product in products[1:]:
                        print(f'{"":<18}{"":<19}{product:<28}{"":<88}{""}')
                    print('')
                print('-' * 160)

                response = input('\nEnter the review id to respond the feedback (or enter "cancel" to return back):\n>>> ')  # prompt the manager to enter review id to reply
                if response == 'cancel':
                    print('\nExiting to customer ratings overview......')
                    break

                elif response not in review.keys():  # if review id not found in the file
                    print('\n+------------------------------------------------------+')
                    print('|⚠️ Feedback doesn\'t exist. Please choose another one. |')
                    print('+------------------------------------------------------+')
                else:
                    respond_text = input('\nEnter response text:\n>>> ')  # prompt the manager to enter response text if the review id found in the file

                    previous_number = None  # create a flag that initialize to None
                    while True:
                        try:
                            # Generate a random number between 1000 and 9999
                            reply_number = random.randint(1000, 9999)
                            # Try checking for duplicates in 'report_number'
                            if reply_number in manager_response['reply_number']:
                                continue  # If duplicate found, generate again
                            else:
                                previous_number = reply_number  # if not duplicate, assign the value to the flag
                                break  # Exit the loop
                        except KeyError:
                            # Handle the case where 'report_number' key does not exist
                            print('\nGenerating reply number...')
                            reply_number = random.randint(1000, 9999)
                            previous_number = reply_number  # Assign the generated number
                            break

                    for user, review_details in review.items():
                        if response == user:
                            manager_response[f'REPLY-{previous_number}'] = {
                                "username": review_details['username'],
                                "products": review_details['product_name'],
                                "review": review_details['review'],
                                "rating": review_details['rating'],
                                "reply": respond_text
                            }

                    save_info(manager_response)

                    print('\nReply has been sent!')  # notify the manager that the reply has been sent
                    continue_reply = input('Continue to reply customers? (y=yes, n=no)\n>>> ')
                    while continue_reply not in ['y', 'n']:
                        print('\n+------------------------------------+')
                        print('|⚠️ Invalid input. Please enter again. |')
                        print('+--------------------------------------+\n')
                        continue_reply = input('Continue to reply customers? (y=yes, n=no)\n>>> ')

                    if continue_reply == 'y':
                        continue
                    else:
                        print('\nExiting to Customer Ratings Overview......')
                        break

        elif choice == 'n':
            print('\nExiting to Manager Privilege......')
            break

        else:
            print('\n+------------------------------------+')
            print('|⚠️ Invalid input. Please enter again. |')
            print('+--------------------------------------+')

