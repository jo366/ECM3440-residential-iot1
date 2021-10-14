# content of test_sample.py
# from app.py import handle_method_request


# DO NOT DELETE THESE COMMENTED IMPORTS

# Required to mock calls to open() and print()
from mockito import when, mock

# from mockito import unstub, verify
# from io import StringIO
# import builtins
import app
# from counterfit_connection import CounterFitConnection

# import time
from counterfit_shims_grove.adc import ADC
# from counterfit_shims_grove.grove_relay import GroveRelay
# import json
# from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse


def test_answer():
    assert 1 == 1


def test_client_init():
    mock_adc = mock(ADC)
    when(mock_adc).read(0).thenReturn(5)
    assert mock_adc.read(0) == 5
    print(app.process(6))
    assert str(app.process(6)) == "{\"soil_moisture\": 6}"
