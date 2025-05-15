import requests
import time 
from pprint import pprint

VTN_URL = "http://localhost:8080/openadr3/3.0.1"
HEADERS = {
    "Content-type": "application/json",
    "Authorization": "Bearer bl_token"
}

def get_current_events(display_most_recent_event = True):
    """Get the current pricing event from the VTN and extract price data"""
    response = requests.get(
        f"{VTN_URL}/events",
        headers=HEADERS,
    )
    events = response.json()
    if display_most_recent_event:
        return events[-1]
    return events

def get_current_event_perpetually():
    previous_event = None
    while True:
        current_event = get_current_events()
        if current_event != previous_event:
            pprint(current_event)
        previous_event = current_event
        time.sleep(5)

if __name__ == "__main__":
    get_current_event_perpetually()
