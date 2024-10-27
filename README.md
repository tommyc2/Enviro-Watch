<img src="https://github.com/user-attachments/assets/0ef59bc8-9500-4e6c-a5c7-156d4eddf026" alt="LOGO" width="250" height="250">

# EnviroWatch
A smart IoT device that monitors air quality & gas levels. It measures temperature, humidity, pressure & VOC (Volatile Organic Compounds).

The following technologies were used:

- Python with Flask
- SocketIO
- MongoDB Atlas
- BME680 3.3V Sensor
- HTML/CSS
- Vanilla JavaScript
- IFTTT/Twilio

The user receives a notification on their phone/device when gas levels reach a certain threshold (and beyond).

In order to run this:

### 1. Setup Board Layout 

Connect the Raspberry Pi to the BME680 sensor using jumper wires and a breadboard. This project works with the 'Environment Click' sensor. Visit: https://github.com/pimoroni/bme680-python for more info

### 1. Install necessary libraries

```bash
pip install -r requirements.txt
```

### 2. Create .ENV file and add your MongoDB Cluster URL & necessary keys
Create a .env file to store your environment variables (auth keys, mongodb cluster password etc.)

### 3. Execute script
Execute the script, typing the following command in your machine's terminal:

```bash
python3 main.py
```

or 

```bash
chmod u+x main.py
./main.py
```




