from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
from time import sleep
import bme680_sensor as sensor
import threading

app = Flask(__name__)
socketio = SocketIO(app)

def main():
    while True:
        sleep(2)
        temp = sensor.get_temperature()
        humidity = sensor.get_humidity()
        pressure = sensor.get_pressure()

        socketio.emit("send_data", {
            "temp": temp,
            "humidity": humidity,
            "pressure": pressure,
            })

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    send_data_thread = threading.Thread(target=main, daemon=True)
    send_data_thread.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 
