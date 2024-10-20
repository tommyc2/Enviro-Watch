from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
from time import sleep
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Function to send data to dashboard
# Note: Does not transmit gas resistance as this is not user friendly nor necessary
def send_data_to_dashboard(temp,humidity,pressure,air_quality):
    while True:
        sleep(2)

        socketio.emit("send_data", {
            "temp": temp, # degrees Celsius
            "humidity": humidity, # %
            "pressure": pressure, # hPa
            "air_quality": air_quality # Excellent, Good, Okay, Poor, Very Poor
            })

@app.route('/')
def index():
    return render_template("index.html")

try:
    send_data_thread = threading.Thread(target=send_data_to_dashboard, daemon=True)
    send_data_thread.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
except Exception as e:
    print("Error:", e)
