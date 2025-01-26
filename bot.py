import requests
import json
import random
import time
import threading
from CryptoAirdropHindi import CryptoAirdropHindi  # Correct import

# Assuming CryptoAirdropHindi is a function you want to call
CryptoAirdropHindi()  # Calling the function properly

# Load API key and URL from 'account.txt'
with open('account.txt', 'r') as file:
    api_key = file.readline().strip()
    api_url = file.readline().strip()

# Load user messages from 'message.txt'
with open('message.txt', 'r') as file:
    user_messages = file.readlines()

# Clean up user messages
user_messages = [msg.strip() for msg in user_messages]

def send_request(message):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    }

    while True:
        try:
            # Make the POST request to the API
            response = requests.post(api_url, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                try:
                    response_json = response.json()
                    print(f"Response for message: '{message}'")
                    print(response_json)
                    break 
                except json.JSONDecodeError:
                    print(f"Error: Received invalid JSON response for message: '{message}'")
                    print(f"Response Text: {response.text}")
            else:
                print(f"Error: {response.status_code}, {response.text}. Retrying...")
                time.sleep(5)  # Wait before retrying if the status code is not 200
        except requests.exceptions.RequestException as e:
            print(f"Request failed with error: {e}. Retrying...")
            time.sleep(5)  # Wait before retrying in case of an exception

def start_thread():
    while True:
        random_message = random.choice(user_messages)
        send_request(random_message)

try:
    num_threads = int(input("Enter the number of threads you want to use: "))
    if num_threads < 1:
        print("Please enter a number greater than 0.")
        exit()
except ValueError:
    print("Invalid input. Please enter an integer.")
    exit()

threads = []

# Create and start the specified number of threads
for _ in range(num_threads):
    thread = threading.Thread(target=start_thread)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All requests have been processed.")
