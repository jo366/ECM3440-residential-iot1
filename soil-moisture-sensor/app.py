from counterfit_connection import CounterFitConnection
import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse


def handle_method_request(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)


def adc_read(channel):
    soil_moisture = adc.read(channel)
    return soil_moisture


def process(soil_moisture):
    message = Message(json.dumps({'soil_moisture': soil_moisture}))
    return message


def send(message, device_client):
    device_client.send_message(message)


if __name__ == "__main__":

    CounterFitConnection.init('127.0.0.1', 5000)
    connection_string = ''  # validate this fits the expected format

    adc = ADC()
    relay = GroveRelay(5)

    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

    print('Connecting')
    device_client.connect()
    print('Connected')

    device_client.on_method_request_received = handle_method_request
    print("I got here")
    while True:
        soil_moisture = adc_read()
        message = process(soil_moisture)
        send(message, device_client)
        print(message)
        time.sleep(10)
