import requests
import app
import random
from counterfit_shims_grove.adc import ADC
from counterfit_connection import CounterFitConnection

# This needs to be global as we need to capture it for use later.
myNumber = random.randrange(1, 500)


def counterfit_set():
    # This first post will set the value of the sensor to be 0
    # or create it if it isn't running.
    r = requests.post(
        "http://127.0.0.1:5000/create_sensor",
        json={
            "type": "Soil Moisture",
            "pin": 0,
            "i2c_pin": 1,
            "port": "/dev/ttyAMA0",
            "name": "sensor_1",
            "unit": "NoUnits",
            "i2c_unit": "NoUnits",
        },
    )
    assert r == "<Response [200]>"
    # This post will set the soil moisture sensor to a random value
    r = requests.post(
        "http://127.0.0.1:5000/integer_sensor_settings",
        json={
            "port": "0",
            "value": myNumber,
            "is_random": False,
            "random_min": 0,
            "random_max": 1023,
        },
    )
    assert r == "<Response [200]>"


def test_counterfit_connection():
    # This is always localhost as it is designed to run within the github actions
    CounterFitConnection.init("127.0.0.1", 5000)
    adc = ADC()

    soil_moisture = app.adc_read(0, adc)

    # This checks the process function as well, to check Counterfit doesn't change the format
    # to the number it generates by adding quotes, spaces etc.
    assert (
        str(app.process(soil_moisture))
        == '{"soil_moisture": [' + str(myNumber) + ", true]}"
    )


counterfit_set()
test_counterfit_connection()


# Sleep here for the number of seconds between the app checking plus 2?
# Now we need to check the IOT hub and we should see the number is coming out.
# TODO - How do you tail the IOT hub?
