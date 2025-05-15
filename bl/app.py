# WORKS FOR VTN RUNNING ON HA 
# seems to create two events (program exists)
# Not yet sure how to delete events ...
# make sure code doesn't create multiple events when in HA. 

import flask
import requests
import json
from datetime import datetime, timedelta
import threading
import time
import pprint
import random

VTN_URL = "http://localhost:8080/openadr3/3.0.1"

# How many seconds should represent an hour for faster than time simulation
# If you just want to use actual hours, set this to 3600
SECONDS_AS_HOUR = 5


HEADERS = {
    "Content-type": "application/json",
    "Authorization": "Bearer bl_token"
}

EVENT_TYPES = ["ALERT_FLEX_ALERT", 
            "ALERT_GRID_EMERGENCY",
            "ALERT_POSSIBLE_OUTAGE",
            "ALERT_BLACK_START",
            ]

# Each event and what hour they should start
SCHEDULES = {
    6:"ALERT_FLEX_ALERT",
    7:"ALERT_GRID_EMERGENCY",
    8:"ALERT_POSSIBLE_OUTAGE",
    9:"ALERT_BLACK_START"}

def _create_program() -> bool:
    data = load_json("program.json")
    response = requests.post(
        f"{VTN_URL}/programs",
        headers=HEADERS,
        json=data
    )
    if response.status_code == 201:
        print("Created program")
        return True
    # The program was already on the VTN
    if response.status_code == 409:
        print("Program already exists")
        return True

    print("Failed to create program")
    print("Create program, status code:", response.status_code)
    print("Create program, response body:", response.json())
    return False

# This event publishes emergency information to VENs
def _create_emergency_event():
    """post example price, optionally adjusting order of intervals"""
    data = load_json("event_minimal.json")

    hour = get_hour()
    if hour not in SCHEDULES.keys():
        print("No event scheduled")
        return 
    event_type = SCHEDULES[hour]

    data["intervals"][0]["payloads"][0]["type"] = event_type
    data["intervalPeriod"]['start'] = create_date_string(hour)
    
    response = requests.post(
        f"{VTN_URL}/events",
        headers=HEADERS,
        json=data
    )
    if response.status_code == 201:
        print("Created emergency event")
        return True
    print("Failed to create emergency event")
    print("Create event, status code:", response.status_code)
    print("Create event, response body:", response.json())


def get_hour():
    # seconds_as_hour says how many seconds should representan hour for faster-than-time simulation
    now = datetime.now()
    return int(now.timestamp() // SECONDS_AS_HOUR % 24)

def create_date_string(hour):
    # Use today's date as the base date
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Adjust the hour and format as ISO 8601 with milliseconds and 'Z'
    date_string = (base_date + timedelta(hours=hour)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    
    return date_string

def _delete_event(event_id = 0) -> bool:
    response = requests.delete(
        f"{VTN_URL}/events/{event_id}",
        headers=HEADERS,
    )
    if response.status_code == 200:
        print("Okay")
        return True
    # The program was already on the VTN
    if response.status_code == 400:
        print("bad request")
        return True

    print("Failed to delete event")
    print("status code:", response.status_code)
    print("response body:", response.json())
    return False
def _delete_all_events():
    response = requests.get(
        f"{VTN_URL}/events",
        headers=HEADERS,
    )
    events = response.json()
    if events == []:
        print('No events to delete')
        return
    for event in events:
        print(f"Deleting event {event['id']}")
        _delete_event(event["id"])
        
    last_id = events[-1]["id"]
    
    return last_id

def _post_events_perpetually():
    while True:
        _create_emergency_event()
        time.sleep(5)
        # _delete_all_events()

def load_json(file_name):
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data


if __name__ == "__main__":
    _create_program()
    _delete_all_events()
    _post_events_perpetually()
    # Start the worker in a separate thread
    # thread = threading.Thread(target=_post_events_perpetually, daemon=True)
    # thread.start()
