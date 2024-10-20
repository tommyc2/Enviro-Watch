#!/usr/bin/env python

import time
import bme680
from flask_server import send_data_to_dashboard

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

start_time = time.time()
curr_time = time.time()
burn_in_time = 10 # setting the value to 10 seconds for testing purposes

burn_in_data = [] # first set of values from the burn-in period (e.g. warm up period)

def calculate_air_quality(score):
    if (score > 90):
        return "Excellent"
    elif (score >= 75):
        return "Good"
    elif (score >= 60):
        return "Okay"
    elif (score >= 45):
        return "Poor"
    elif (score >= 25):
        return "Very Poor"
    else:
        return "Dangerous"


try:
    print('Gas Sensor warming up.....')
    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            burn_in_data.append(gas)
            time.sleep(1)

    gas_baseline = sum(burn_in_data[-50:]) / 50.0
    hum_baseline = 40.0
    hum_weighting = 0.25

    print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(
        gas_baseline,
        hum_baseline))

    while True:
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            gas_offset = gas_baseline - gas

            hum = sensor.data.humidity
            hum_offset = hum - hum_baseline

            # Calculate Humidity Score as the distance from the humidity baseline.
            if hum_offset > 0:
                hum_score = (100 - hum_baseline - hum_offset)
                hum_score /= (100 - hum_baseline)
                hum_score *= (hum_weighting * 100)

            else:
                hum_score = (hum_baseline + hum_offset)
                hum_score /= hum_baseline
                hum_score *= (hum_weighting * 100)

            # Calculate Gas Score (resistance) as the distance from the gas baseline.
            if gas_offset > 0:
                gas_score = (gas / gas_baseline)
                gas_score *= (100 - (hum_weighting * 100))

            else:
                gas_score = 100 - (hum_weighting * 100)

            # Air Quality Score
            air_quality_score = hum_score + gas_score

            # Temperature, Humidity, Pressure & Gas readings
            temperature = round(sensor.data.temperature,2)
            humidity = round(hum, 2) # percent
            pressure = round(sensor.data.pressure,2) # in hectopascals
            gas_levels = round(gas,2) # ohms
            air_quality_rating = calculate_air_quality(round(air_quality_score,2)) # returns string indicating quality level
            
            # Print values to terminal
            print("------------------------------------------")
            print(f"Air Quality Score: {air_quality_rating}")
            print(f"T: {temperature} C, Humidity: {humidity}% , Pressure {pressure} hPa, Gas resistance: {gas_levels} ohms")
            print("------------------------------------------")

            time.sleep(2)

            # Pass sensor readings into main script
            #send_data_to_dashboard(temperature,humidity,pressure,air_quality_rating)

except KeyboardInterrupt:
    pass