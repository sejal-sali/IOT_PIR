import RPi.GPIO as GPIO
import time

SENSOR_ENTRANCE_PIN = 14
SENSOR_EXIT_PIN = 15     

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_ENTRANCE_PIN, GPIO.IN)
GPIO.setup(SENSOR_EXIT_PIN, GPIO.IN)

def entrance(channel):
    print("Entrance motion detected!")

def exit(channel):
    print("Exit motion detected!")

GPIO.add_event_detect(SENSOR_ENTRANCE_PIN, GPIO.RISING, callback=entrance, bouncetime=200)
GPIO.add_event_detect(SENSOR_EXIT_PIN, GPIO.RISING, callback=exit, bouncetime=200)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()