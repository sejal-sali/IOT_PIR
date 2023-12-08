# Github copilot used for this file to check errors and fixes from errors

import RPi.GPIO as GPIO
import time
import pymongo
from pymongo import MongoClient
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import os
from dotenv import load_dotenv
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
import json

load_dotenv()

pnconfig = PNConfiguration()

pnconfig.subscribe_key = os.environ.get('PUBNUB_SUBSCRIBE_KEY')
pnconfig.publish_key = os.environ.get('PUBNUB_PUBLISH_KEY')
pnconfig.user_id = "john_iot_pi_zero"
pubnub = PubNub(pnconfig)

my_channel = "johns_sd3b_pi"

def my_publish_callback(envelope, status):
    #Check whether request successfully completed or not
    if not status.is_error():
        pass
    else:
        pass


class MySubscribeCallback(SubscribeCallback):
    def presense(self, pubnub, presence):
        pass

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass
        elif status.category == PNStatusCategory.PNConnectedCategory:
            #pubnub.publish().channel(my_channel).message("Hello world").pn_async(my_publish_callback)
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass

    def message(self, pubnub, message):
        print(message.message)
        received = message.message
        if "buzzer" in received.keys():
            if received["buzzer"] == "on":
                data["alarm"] = True
            else:
                data["alarm"] = False

pubnub.add_listener(MySubscribeCallback())

def publish(channel, message):
    pubnub.publish().channel(channel).message(message).pn_async(my_publish_callback)


#app = Flask(__name__)
alive = 0
data = {}


client = MongoClient('mongodb://localhost:3000/')
db = client.bus_data
collection = db.seat_weights
motion_data = db.motion_data


# GPIO setup for motion sensors
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Defined GPIO pins for motion sensors
SENSOR_ENTRANCE_PIN = 14  
SENSOR_EXIT_PIN = 15  


# Set up GPIO pins for motion sensors
GPIO.setup(SENSOR_ENTRANCE_PIN, GPIO.IN)
GPIO.setup(SENSOR_EXIT_PIN, GPIO.IN)

# Motion sensor counters
entrance_counter = 0
exit_counter = 0

def entrance(channel):
    global entrance_counter
    entrance_counter += 1
    print("Entrance detected")
    motion_data.insert_one({"action": "entrance", "timestamp": time.time()})
    print(f"People entered: {entrance_counter}")

def exit(channel):
    global exit_counter
    exit_counter += 1
    print("Exit detected")
    motion_data.insert_one({"action": "exit", "timestamp": time.time()})
    print(f"People exited: {exit_counter}")

        # Add event detection for motion sensors
GPIO.add_event_detect(SENSOR_ENTRANCE_PIN, GPIO.RISING, callback=entrance, bouncetime=200)
GPIO.add_event_detect(SENSOR_EXIT_PIN, GPIO.RISING, callback=exit, bouncetime=200)

SEAT_SENSOR_PINS = [23]  
# Set up GPIO pins for pressure sensors
for pin in SEAT_SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN)
# Initialize previous state of seat occupancy
previous_occupancy = [False] * len(SEAT_SENSOR_PINS)  # Assuming all seats start as unoccupied

def read_seat_occupancy(pin):
    occupancy = GPIO.input(pin)
    print(f"Reading from pin {pin}: {'Occupied' if occupancy else 'Empty'}")
    return occupancy

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

if __name__ == '__main__':
    pubnub.subscribe().channels(my_channel).execute()