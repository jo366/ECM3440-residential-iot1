import requests


def counterfit_set():
    # TODO work out how to grab the URL for the running counterfit app, maybe we deploy and keep it static.
    # This first post will set the value of the sensor to be 0 or create it if it isn't running.
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

    # Sleep here for the number of seconds between the app checking plus 2?
    # Now we need to check the IOT hub and we should see a 0 coming out.
    # TODO - How do you tail the IOT hub?

    r = requests.post(
        "http://127.0.0.1:5000/integer_sensor_settings",
        json={
            "port": "0",
            "value": 102,  # Make this a random value?
            "is_random": False,
            "random_min": 0,
            "random_max": 1023,
        },
    )
    print(r)

    # Sleep here for the number of seconds between the app checking plus 2?
    # Now we need to check the IOT hub and we should see a whatever the random thing is coming out.
    # TODO - How do you tail the IOT hub?


counterfit_set()
