# src/coffee-bot/main.py

import json
import os
import schedule
import time
import random
import requests
from dotenv import load_dotenv
from twilio.rest import Client

# file to store message queue state
MESSAGE_FILE = "coffee_messages.json"
QUEUE_FILE = "message_queue.json"

# Config
load_dotenv()

# Twilio client
def get_twilio_client(account_sid=None, auth_token=None) -> Client:
    return Client(account_sid, auth_token)

# messages    
def get_messages(file_name):
    # check if file exists
    try:
        with open(file_name, "r") as file:
            messages = json.load(file)

        if not messages:
            raise ValueError("Failed to load messages from file")
        
        return messages
    except Exception as e:
        print(f"Failed to load messages from file: {e}")
        return None

# message queue
def save_queue_state(queue, file_name):
    try:
        with open(file_name, "w") as file:
            json.dump(queue, file)
        print("Queue state saved successfully.")
    except Exception as e:
        print(f"Unexpected error while saving queue state: {e}")

def load_queue_state(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return None

def initialize_message_queue(queue_file_name=None):
    # load queue state from file
    if queue_file_name is not None:
        queue = load_queue_state(queue_file_name)

        if queue and len(queue) > 0:
            return queue
    
    queue = get_messages(MESSAGE_FILE).copy()
    random.shuffle(queue)

    return queue

message_queue = load_queue_state(QUEUE_FILE)

def get_next_message():
    global message_queue

    if not message_queue:
        message_queue = initialize_message_queue()

    message = message_queue.pop(0)
    save_queue_state(message_queue, QUEUE_FILE)

    return message

def send_coffee_message():
    twilio_client = get_twilio_client()
    twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
    phone_numbers = os.getenv("PHONE_CONTACTS").split(",")
    message = get_next_message()

    for number in phone_numbers:
        try:
            twilio_client.messages.create(
                to=number,
                from_=twilio_phone_number,
                body=message,
            )
            print(f"Message sent to {number}: {message}")
        except Exception as e:
            print(f"failed to send message to {number}: {e}")
        
# schedule the message to be sent every day at a random time between 8 AM and 11 AM
def schedule_coffee_message():
    hour = random.randint(8, 11)
    minute = random.randint(0, 59)
    scheduled_time = f"{hour:02d}:{minute:02d}"
    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(send_coffee_message)
    print(f"Next coffee message scheduled for {scheduled_time}")

    # store scheduled time to a file for recovery after restart
    with open("scheduled_time.txt", "w") as file:
        file.write(scheduled_time)

def main():
    # send_coffee_message() // one off testing
    schedule_coffee_message()

    while True:
        schedule.run_pending()

        try:
            next_run = schedule.idle_seconds()

            if next_run is None or next_run <= 0:
                schedule_coffee_message()
                next_run = 60
            else:
                next_run = min(next_run, 1800)
        except Exception as e:
            print(f"Error in scheduling: {e}")
            next_run = 300

        print(f"Sleeping for {next_run} seconds until next check")
        time.sleep(next_run)

if os.getenv("ENV") == "production":
    main()

