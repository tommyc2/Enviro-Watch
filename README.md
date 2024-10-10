# Enviro-Watch
A smart IoT device that monitors air quality, gas levels &amp; temperature. It measures room temperature, pressure, Gas levels (carbon dioxide etc.).

## Sensors/Devices needed

- MQ-2 or any MQ Sensor (Python package: gas-detection)
- BME sensor (for temperature, humidity, pressure etc.)
- ADC (analog to digital)
- Raspberry Pi
- LCD Screen (I2C)
- Breadboard

## Plans

Process data using python --> send to mongodb online database
Web app requests data from DB and displays the data on basic web dashboard

or 

Data is processed using python --> communicate to Javascript web app and display data on ReactJS dashboard/IoT platform

Ways of sending data to dashboard

- Flask
- SocketIO (WebSocket)
- MQTT (Broker)
- HTMl (rendering web dashboard)
