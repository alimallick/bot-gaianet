import requests
import json
import random
import time
import threading

with open('account.txt', 'r') as file:
    api_key = file.readline().strip()
    api_url = file.readline().strip()

with open('message.txt', 'r') as file:
    user_messages = file.readlines()

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
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"Request failed with error: {e}. Retrying...")
            time.sleep(5)

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

for _ in range(num_threads):
    thread = threading.Thread(target=start_thread)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All requests have been processed.")
