# content of test_sample.py
# from app.py import handle_method_request

from counterfit_connection import CounterFitConnection


# DO NOT DELETE THESE COMMENTED IMPORTS

# Required to mock calls to open() and print()
from azure.iot.device.iothub.models.methods import MethodRequest
from mockito import when, mock

# from mockito import unstub, verify
# from io import StringIO
# import builtins
# from '../soil-moisture-sensor/app' import app

import app

# from counterfit_connection import CounterFitConnection

# import time
from counterfit_shims_grove.adc import ADC
from azure.iot.device import IoTHubDeviceClient, MethodResponse

from counterfit_shims_grove.grove_relay import GroveRelay


# from counterfit_shims_grove.grove_relay import GroveRelay
# import json
# from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

import sys

sys.path.insert(1, "/soil-moisture-sensor/app.py")

# from '../soil-moisture-sensor/app' import adc_read


# test_process - testing correct json is output with a valid integer input
def test_process():
    print(app.process(6))
    assert str(app.process(6)) == '{"soil_moisture": 6}'


# adc_read - testing function behaves as expected with valid input
def test_adc_read_expected_value():
    mock_adc = mock(ADC)
    when(mock_adc).read(0).thenReturn(5)

    print(app.adc_read(0, mock_adc))

    assert app.adc_read(0, mock_adc)[0] == 5
    assert app.adc_read(0, mock_adc)[1] is True


# adc_read - testing function breaks with character input
def test_adc_read_character_input():
    print(app.adc_read("a", 0))
    assert app.adc_read("a", 0)[1] is False


# adc_read - testing function breaks with invalid int input
def test_adc_read_invalid_int_input():
    print(app.adc_read(50, 0))
    assert app.adc_read(50, 0)[1] is False


# send - mock the send_message method and check that we get expected returns
def test_send_if_device_client_is_successful():
    mock_device_client = mock(IoTHubDeviceClient)
    when(mock_device_client).send_message("message").thenReturn(True)

    print(app.send("message", mock_device_client))
    assert (app.send("message", mock_device_client)) is True


# send - mock the send_message method and check that we get expected returns
def test_send_if_device_client_returns_error():
    mock_device_client = mock(IoTHubDeviceClient)
    when(mock_device_client).send_message("Error").thenReturn(False)

    print(app.send("Error", mock_device_client))
    assert (app.send("Error", mock_device_client)) is False


# handle_method_request_on
def test_handle_method_request():
    mock_relay = mock(GroveRelay(5))
    when(mock_relay).on().thenReturn("Relay has been switched on")

    mock_request_on = mock(MethodRequest(1, "relay_on", "body"))
    mock_request_on.request_id = 1
    mock_request_on.name = "relay_on"

    mock_reponse = mock(MethodResponse(mock_request_on, 200))
    when(mock_reponse).create_from_method_request(mock_request_on, 200).thenReturn(
        "Response: on, 200"
    )

    mock_device_client = mock(IoTHubDeviceClient)
    when(mock_device_client).send_method_response(mock_reponse).thenReturn(True)

    # assert (app.handle_method_request(mock_request_on, mock_relay, mock_device_client)[0]) == True
    assert (
        app.handle_method_request(mock_request_on, mock_relay, mock_device_client)[1]
    ) == "Relay has been switched on"


def test_main():
    mock_counterFitConnection = mock(CounterFitConnection)
    when(mock_counterFitConnection.init).thenReturn("success")
    app.CounterFitConnection.assert_called_with("127.0.0.1", 5000)

    mock_adc = mock(ADC)
    when(mock_adc).read(0).thenReturn(5)

    mock_device_client = mock(IoTHubDeviceClient)
    when(mock_device_client).create_from_connection_string("").thenReturn

    assert (app.get("soil_moisture"))[0] == 5
