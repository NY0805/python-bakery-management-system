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


def customer_feedback():
    while True:
        print('\n', '\t'*15, 'CUSTOMER FEEDBACK')
        print('-' * 140)
        header = ['Username']  # create a list for headers and append the first item in the list
        for review_details in review.values():  # access the values of order_list
            for sub_key, sub_value in review_details.items():  # access the subkey and sub value in the value of order_list
                header.append(sub_key.title().replace('_', ' '))  # append other details of orders into the header list and replace all underscore with space to enhance readability
            break

        print(f'{header[0]:<19}{header[1]:<24}{header[2]:<90}{header[3]}')  # display the headers
        print('-' * 140)

        for user, review_details in review.items():
            products = review_details['product_name'].split(', ')
            print(f'{user:<19}{products[0]:<24}{review_details["review"]:<90}{review_details["rating"]}')
            for product in products[1:]:
                print(f'{"":<19}{product:<24}{"":<90}{""}')
            print('')
        print('-' * 140)

        while True:
            response = input('\nEnter customer\'s username to respond to their reviews (or enter "cancel" to return back):\n>>> ')
            if response == 'cancel':
                print('\nExiting to Manager Privilege......')
                break

            elif response not in review.keys():
                print('\n+------------------------------------------------------+')
                print('|⚠️ Customer doesn\'t exist. Please choose another one. |')
                print('+------------------------------------------------------+')
            else:
                respond_text = input('\nEnter response text:\n>>> ')

                previous_number = None
                while True:
                    try:
                        # Generate a random number between 1000 and 9999
                        reply_number = random.randint(1000, 9999)
                        # Try checking for duplicates in 'report_number'
                        if reply_number in manager_response['reply_number']:
                            continue  # If duplicate found, generate again
                        else:
                            previous_number = reply_number
                            break  # Exit the loop when a unique number is found
                    except KeyError:
                        # Handle the case where 'report_number' key does not exist
                        print('\nGenerating reply number...')
                        reply_number = random.randint(1000, 9999)
                        previous_number = reply_number  # Assign the generated number
                        break  # Exit loop since we don't need to check for duplicates in this case

                for user, review_details in review.items():
                    if response == user:
                        manager_response[f'REPLY-{previous_number}'] = {
                            "username": user,
                            "products": review_details['product_name'],
                            "review": review_details['review'],
                            "rating": review_details['rating'],
                            "reply": respond_text
                        }

                save_info(manager_response)

                print('\nReply has been sent!')
                continue_reply = input('Continue to reply customers? (y=yes, n=no)\n>>> ')
                while continue_reply not in ['y', 'n']:
                    print('\n+------------------------------------+')
                    print('|⚠️ Invalid input. Please enter again. |')
                    print('+--------------------------------------+\n')
                    continue_reply = input('Continue to reply customers? (y=yes, n=no)\n>>> ')

                if continue_reply == 'y':
                    continue

                print('\nExiting to Manager Privilege......')
                break

        break

#customer_feedback()
