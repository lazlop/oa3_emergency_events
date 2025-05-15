# OpenADR3 Emergency Events

A reference implementation for OpenADR3 (Open Automated Demand Response) emergency event handling, demonstrating how to create, publish, and consume emergency events using the OpenADR3 protocol.

## Overview

This project demonstrates the implementation of emergency event handling in OpenADR3, focusing on:

- Creating and publishing emergency events from a business logic (BL) component
- Receiving and processing these events in a Virtual End Node (VEN)
- Simulating different types of emergency alerts on an accelerated timeline

The system uses a Virtual Top Node (VTN) as the central communication hub, which distributes events according to the OpenADR3 protocol. The reference VTN is available by request.

## Project Structure

```
oa3_emergency_events/
├── bl/                  # Business Logic component
│   ├── app.py           # Main BL application that creates and posts events
│   ├── event_minimal.json  # Template for emergency events
│   └── program.json     # Program definition
├── ven/                 # Virtual End Node component
│   └── app.py           # VEN application that receives events
├── requirements.txt     # Project dependencies
└── README.md            # This file
```

## Emergency Event Types

The system simulates four types of emergency events:

1. **ALERT_FLEX_ALERT** - A request for voluntary energy conservation
2. **ALERT_GRID_EMERGENCY** - Notification of critical grid conditions
3. **ALERT_POSSIBLE_OUTAGE** - Warning of potential power outages
4. **ALERT_BLACK_START** - Instructions for system restoration after a blackout

These events are scheduled to occur at specific simulated hours (using an accelerated timeline where each hour is represented by 5 seconds).

## Prerequisites

- Python 3.8+
- A running VTN (Virtual Top Node) instance
  - The VTN reference implementation is available by request
  - It can be run in a virtual environment or as a Docker container

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/oa3_emergency_events.git
   cd oa3_emergency_events
   ```

2. Install dependencies and use venv if desired. Currently there are more dependencies in these files than actually used, since flask app and visualization was removed. 

   ```
   # Using pip
   pip install -r requirements.txt
   
   # Or using uv (recommended)
   uv sync
   ```

3. Activate virtual environment:
   ```
   . .venv/bin/activate
   ```

## Running the Application

### 1. Start the VTN

Ensure your VTN instance is running on `http://localhost:8080/openadr3/3.0.1` (or update the `VTN_URL` in both app.py files if using a different address).

### 2. Run the Business Logic (BL) Component

```
cd bl
python app.py
```

This will:
- Create a program on the VTN (if it doesn't exist)
- Delete any existing events
- Start posting emergency events based on the simulated time schedule

### 3. Run the Virtual End Node (VEN)

In a separate terminal:

```
cd ven
python app.py
```

This will:
- Connect to the VTN
- Continuously poll for new events
- Display event details when received

## Configuration

You can modify the following parameters in `bl/app.py`:

- `SECONDS_AS_HOUR`: Number of seconds that represent an hour in the simulation (default: 5)
- `SCHEDULES`: Dictionary mapping hours to event types
- `VTN_URL`: URL of the VTN server

## Component Details

### Business Logic (BL)

The BL component is responsible for:
- Creating a program on the VTN
- Generating emergency events based on a schedule
- Posting these events to the VTN
- Managing event lifecycle (creation and deletion)

### Virtual End Node (VEN)

The VEN component:
- Connects to the VTN
- Retrieves current events
- Processes and displays event information
- In a real-world scenario, would take actions based on the event type

### Virtual Top Node (VTN)

The VTN (not included in this repository):
- Acts as a central hub for OpenADR3 communication
- Receives events from the BL
- Distributes events to registered VENs
- Manages program and event data

## Development Notes

- The simulation uses an accelerated timeline where each hour is represented by 5 seconds
- Events are scheduled to occur at specific hours (6, 7, 8, 9)
- The BL component continuously posts events based on the current simulated hour
- The VEN component polls for new events every 5 seconds

