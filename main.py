import threading
import time
import bme680
from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
import time
from database import save_to_database
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
socketio = SocketIO(app)

if (load_dotenv()):
    print("Environment variable imported!")
else:
    print("Failed to import environment variable")

event_name = "air_quality_is_bad"
webhook_key = os.getenv("IFTTT_WEBHOOK_KEY")
url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{webhook_key}"

@app.route('/')
def index():
    return render_template("index.html")

def send_ifttt(data):
    payload = { "value1": data }
    response = requests.post(url, json=payload)
    print(response.status_code)

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
        

def main():
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
        
        # Calculations for Air Quality (IAQ)
        # Source: bme680-python library --> indoor-air-quality
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
                
                time.sleep(3)

                # Print values to terminal
                print("------------------------------------------")
                print(f"Air Quality Score: {air_quality_rating}")
                print(f"T: {temperature} C, Humidity: {humidity}% , Pressure {pressure} hPa, Gas resistance: {gas_levels} ohms")
                print("------------------------------------------")

                # Emit data on web socket
                socketio.emit("send_data", {"temp": temperature,"humidity": humidity,"pressure": pressure,"air_quality": air_quality_rating })

                # If air quality reading bad, send SMS to alert user
                #if (air_quality_rating == "Poor") or (air_quality_rating == "Very Poor") or (air_quality_rating == "Dangerous"):
                 #   send_ifttt(air_quality_rating)

                # Save data to MongoDB Atlas Cluster
                save_to_database(temperature,humidity,pressure,air_quality_rating)

    except Exception as error:
        print(error)

@app.before_first_request
def handleSensorSetup():
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)



