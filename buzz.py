import RPi.GPIO as GPIO
import time
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:3000/')  # Replace with your MongoDB URI
db = client.bus_data
collection = db.seat_weights
motion_data = db.motion_data


# GPIO setup for motion sensors
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins for motion sensors
SENSOR_ENTRANCE_PIN = 12  
SENSOR_EXIT_PIN = 13   


# Set up GPIO pins for motion sensors
GPIO.setup(SENSOR_ENTRANCE_PIN, GPIO.IN)
GPIO.setup(SENSOR_EXIT_PIN, GPIO.IN)

# Motion sensor counters
entrance_counter = 0
exit_counter = 0

def entrance(channel):
    global entrance_counter
    entrance_counter += 1
    motion_data.insert_one({"action": "entrance", "timestamp": time.time()})
    print(f"People entered: {entrance_counter}")

def exit(channel):
    global exit_counter
    exit_counter += 1
    motion_data.insert_one({"action": "exit", "timestamp": time.time()})
    print(f"People exited: {exit_counter}")

        # Add event detection for motion sensors
GPIO.add_event_detect(SENSOR_ENTRANCE_PIN, GPIO.RISING, callback=entrance, bouncetime=200)
GPIO.add_event_detect(SENSOR_EXIT_PIN, GPIO.RISING, callback=exit, bouncetime=200)

SEAT_SENSOR_PINS = [18]  
# Set up GPIO pins for pressure sensors
for pin in SEAT_SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN)
# Initialize previous state of seat occupancy
previous_occupancy = [False] * len(SEAT_SENSOR_PINS)  # Assuming all seats start as unoccupied

def read_seat_occupancy(pin):
    """
    Returns True if the seat is occupied, False otherwise.
    """
    return GPIO.input(pin)

try:
    while True:
        for i, pin in enumerate(SEAT_SENSOR_PINS):
            current_occupied = read_seat_occupancy(pin)

            if current_occupied != previous_occupancy[i]:
                # State changed, log to database
                print(f"Seat {i}: {'Occupied' if current_occupied else 'Empty'}")
                collection.insert_one({"seat": i, "occupied": current_occupied, "timestamp": time.time()})
                previous_occupancy[i] = current_occupied  # Update the previous state

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()