import RPi.GPIO as GPIO
import time
import pymongo


client = MongoClient('mongodb://localhost:3000/')  # Replace with your MongoDB URI
db = client.bus_data
collection = db.seat_weights
motion_data = db.motion_data

PIR_pin = 8
Buzzer_pin = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_pin, GPIO.IN)
GPIO.setup(Buzzer_pin, GPIO.OUT)

def main():
    motion_detected()
    buzz(100)
def buzz(repeat):
    for i in range(0, repeat):
        for pulse in range(40):
            GPIO.output(Buzzer_pin, True)
            time.sleep(0.0001)
            GPIO.output(Buzzer_pin, False)
            time.sleep(0.0001)
        time.sleep(0.05)

def motion_detected():
    while(True):
        if GPIO.input(PIR_pin):
            print("Motion Detected...")
            buzz(4)
            time.sleep(2)
        else:
            print("No Motion Detected...")
            time.sleep(2)

if __name__ == '__main__':
    main()