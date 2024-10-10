import paho.mqtt.client as paho
import time
import json

client = paho.Client()

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNECTION received with code %s." % rc)

def on_message(client, obj, msg):
    print("Topic:" + msg.topic + ",Payload:" + msg.payload)

def on_publish(client, userdata, mid):
    print("mid: " + str(mid))
 

client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883)
client.loop_start()

def main():
    while True:
        test_data = 100
        client.publish('/data', payload=str(test_data))
        time.sleep(2)

main()