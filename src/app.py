from counterfit_connection import CounterFitConnection
import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from decouple import config

API_KEY = config('KEY')


def handle_method_request(request, relay, device_client):
    print("Direct method received - ", request.name)
    relay_message = ""

    if request.name == "relay_on":
        relay_message = relay.on()
    elif request.name == "relay_off":
        relay_message = relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    success = device_client.send_method_response(method_response)

    return success, relay_message


def adc_read(channel, adc):
    valid_channel = False
    soil_moisture = 0

    if (isinstance(channel, int)) and (0 <= channel <= 7):
        soil_moisture = adc.read(channel)
        valid_channel = True

    return soil_moisture, valid_channel


def process(soil_moisture):
    message = Message(json.dumps({"soil_moisture": soil_moisture}))
    return message


def send(message, device_client):
    return device_client.send_message(message)


if __name__ == "__main__":

    connection_string = API_KEY

    CounterFitConnection.init("127.0.0.1", 5000)
    connection_string = connection_string  # validate this fits the expected format

    adc = ADC()
    relay = GroveRelay(5)

    device_client = IoTHubDeviceClient.create_from_connection_string(
        connection_string)
    device_client.connect()
    device_client.on_method_request_received = handle_method_request

    while True:
        soil_moisture = adc_read(0, adc)
        message = process(soil_moisture)
        send(message, device_client)
        print(message)
        time.sleep(10)
