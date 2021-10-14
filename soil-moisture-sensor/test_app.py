# content of test_sample.py
# from app.py import handle_method_request


# DO NOT DELETE THESE COMMENTED IMPORTS

# Required to mock calls to open() and print()
from mockito import when, mock

# from mockito import unstub, verify
# from io import StringIO
# import builtins
# from '../soil-moisture-sensor/app' import app

import app

# from counterfit_connection import CounterFitConnection

# import time
from counterfit_shims_grove.adc import ADC

# from counterfit_shims_grove.grove_relay import GroveRelay
# import json
# from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

import sys

sys.path.insert(1, "/soil-moisture-sensor/app.py")

# from '../soil-moisture-sensor/app' import adc_read


def test_answer():
    assert 1 == 1


def test_client_init():
    mock_adc = mock(ADC)
    when(mock_adc).read(0).thenReturn(5)
    assert mock_adc.read(0) == 5


def test_process():
    print(app.process(6))
    assert str(app.process(6)) == '{"soil_moisture": 6}'


# @TODO: write tests

# UNIT TESTS
# adc_read: make sure its only integer - Ash
# send: Person 2 - add a return - James & Ash
# process: DONE
# handle_method_request: Khadija - might need to be split up?

# File structure - Jacob

# INTEGRATION TESTS
# @TODO


# Might be useful for adc_read:
# assert type(n) == int, "Incorrect input"
#     return n
