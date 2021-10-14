# Import required modules.
from counterfit_connection import CounterFitConnection # For faking IoT devices
import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

# Connect to Counterfit using local host.
# @TODO: Add deployment hosting environment.
CounterFitConnection.init('127.0.0.1', 5000)

# Connection string for the AWS IoT Hub.
# @TODO: Add as a secret.
connection_string = '<connection_string>'

adc = ADC()
relay = GroveRelay(5)

# Create a new IoT device client for the Azure IoT Hub.
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

# Connect to the Azure IoT Hub.
print('Connecting')
device_client.connect()
print('Connected')

# -----------------------------------------------------------------------------
# Method Name: handle_method_request
# Description: No clue.
# -----------------------------------------------------------------------------
def handle_method_request(request):
    print("Direct method received - ", request.name)
    
    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)

    # Send a response to a method request via the Azure IoT Hub.
    device_client.send_method_response(method_response)

# Call the hand_method_request method when a new request is received.
device_client.on_method_request_received = handle_method_request

# Loop indefinitely every 10 seconds.
while True:
    # Read the analogue value from the sensor and print it out to the console.
    soil_moisture = adc.read(0)
    print("Soil moisture:", soil_moisture)

    # Send a message with the read sensor value to the Azure device client..
    message = Message(json.dumps({ 'soil_moisture': soil_moisture }))
    device_client.send_message(message)

    time.sleep(10)