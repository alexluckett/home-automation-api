"""
Methods to shut down an LG WebOS TV remotely, providing it has an internet connection.

Some LG WebOS TVs only support turning on using HDMI CEC and do not support turning off. This provides an alternative
way of shutting them off without installing an IR blaster with a shutdown command.

Installation process:
1) Turn on LG WebOS TV and connect to internet (wifi or ethernet)
2) Assign your TV a static IP in your router, so the IP address does not change
3) Call the main function below (via the API endpoint)
4) Your TV will notify you that a device is trying to connect as a remote. Accept this prompt.
5) Done. Subsequent calls to the API will not require acceptance.
"""

from os.path import expanduser, join

from pywebostv.connection import *
from pywebostv.controls import *


def get_path_to_config_file():
    return join(expanduser("~"), ".lg_api_key")


def save_client_key(key):
    path_to_key = get_path_to_config_file()

    with open(path_to_key, 'w') as api_key_file:
        api_key_file.write(key)


def get_client_key():
    path_to_key = get_path_to_config_file()

    try:
        with open(path_to_key, 'r') as api_key_file:
            return api_key_file.readline()
    except Exception:
        print("Failed to get API key")


def main(tv_ip):
    client = WebOSClient(tv_ip)
    client.connect()

    api_key = get_client_key()

    if api_key:
        store = {"client_key": api_key}
    else:
        store = {}

    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == WebOSClient.REGISTERED:
            print("Registration successful!")
            print(store)

            save_client_key(store["client_key"])
        else:
            print("Failed to connect to tv")
            raise Exception("Failed to connect to tv")

    system = SystemControl(client)
    system.power_off()