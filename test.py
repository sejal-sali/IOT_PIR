import RPi.GPIO as GPIO
import time

SENSOR_ENTRANCE_PIN = 14
SENSOR_EXIT_PIN = 15     

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_ENTRANCE_PIN, GPIO.IN)
GPIO.setup(SENSOR_EXIT_PIN, GPIO.IN)


def check_sensor(sensor_pin):
    return GPIO.input(sensor_pin)

    
# Defined GPIO pins for pressure sensors (seat sensors)
SEAT_SENSOR_PINS = [23]
# Set up GPIO pins for pressure sensors
for pin in SEAT_SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN)

# Initialize previous state of seat occupancy
previous_occupancy = [False] * len(SEAT_SENSOR_PINS)

# Function to read seat occupancy
def read_seat_occupancy(pin):
    return GPIO.input(pin)

# Tester function for pressure plates
def test_pressure_plates():
    print("Testing pressure plate sensors...")
    for i, pin in enumerate(SEAT_SENSOR_PINS):
        status = 'Occupied' if read_seat_occupancy(pin) else 'Empty'
        print(f"Seat {i} (Pin {pin}): {status}")


try:
    test_pressure_plates()
    last_entrance_state = check_sensor(SENSOR_ENTRANCE_PIN)
    last_exit_state = check_sensor(SENSOR_EXIT_PIN)

    while True:
        current_entrance_state = check_sensor(SENSOR_ENTRANCE_PIN)
        current_exit_state = check_sensor(SENSOR_EXIT_PIN)

        # Check for entrance
        if current_entrance_state != last_entrance_state:
            last_entrance_state = current_entrance_state
            if current_entrance_state:
                print("Entrance motion detected!")

        # Check for exit
        if current_exit_state != last_exit_state:
            last_exit_state = current_exit_state
            if current_exit_state:
                print("Exit motion detected!")

        time.sleep(0.001)  # Small delay to prevent CPU overload

except KeyboardInterrupt:
    GPIO.cleanup()