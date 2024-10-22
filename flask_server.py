from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
from time import sleep

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")

socketio.run(app, debug=True, host='0.0.0.0', port=5000)


