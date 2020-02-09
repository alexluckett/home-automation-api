"""
Methods to control Energenie RF light switches from an API.

Requires the Energenie Pi-mote control board to be physically installed on the RPi.

Installation process:
1) Hold pairing button on 1 or many RF receivers
2) Call API endpoint for light group 1, 2, 3 or 4
3) Light switches will now be paired under the light group you just called
4) Repeat steps 1-3 for each group of light switches. API supports 4 total groups.
"""

import RPi.GPIO as GPIO
import time


def setup():
    GPIO.setwarnings(False)  # fail on error

    # set the pins numbering mode
    GPIO.setmode(GPIO.BOARD)

    # Select the GPIO pins used for the encoder K0-K3 data inputs
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    # Select the signal to select ASK/FSK
    GPIO.setup(18, GPIO.OUT)

    # Select the signal used to enable/disable the modulator
    GPIO.setup(22, GPIO.OUT)

    # Disable the modulator by setting CE pin lo
    GPIO.output(22, False)

    # Set the modulator to ASK for On Off Keying
    # by setting MODSEL pin lo
    GPIO.output(18, False)

    # Initialise K0-K3 inputs of the encoder to 0000
    GPIO.output(11, False)
    GPIO.output(15, False)
    GPIO.output(16, False)
    GPIO.output(13, False)


def get_signal_code(light_number, status):
    light_identifier_signal = {
        0: "011",
        1: "111",
        2: "110",
        3: "101",
        4: "100"
    }.get(light_number)

    if status.lower() == "true":
        status_identifier = "1"
    elif status.lower() == "false":
        status_identifier = "0"
    else:
        raise ValueError("light_status is invalid")

    return "{}{}".format(status_identifier, light_identifier_signal)


def send_code_to_gpio(signal_code_string):
    binary_index_to_gpio_pin = [11, 15, 16, 13]
    
    for idx, val in enumerate(reversed(signal_code_string)):
        gpio_pin = binary_index_to_gpio_pin[idx]
        gpi_pin_signal = val == "1"

        GPIO.output(gpio_pin, gpi_pin_signal)

    # let it settle, encoder requires this
    time.sleep(0.1)
    # Enable the modulator
    GPIO.output(22, True)
    # keep enabled for a period
    time.sleep(0.25)
    # Disable the modulator
    GPIO.output(22, False)


def light_action(light_number, light_status):
    try:
        setup()
        signal_code = get_signal_code(light_number, light_status)
        send_code_to_gpio(signal_code)
    finally:
        GPIO.cleanup()
