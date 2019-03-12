import paho.mqtt.client as mqtt
import time
from threading import Lock

from classes import Locked_Variables



scale_value = ScaleValues()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/#")

#def on_message(client, userdata, msg):
#    print(msg.topic + " " + str(msg.payload))

def on_message_scale(client, userdata, msg):
    scale_value.write_value(float((msg.payload)))
    #print(msg.topic + " " + str(msg.payload))




broker_address="130.216.153.37"
user = "summer2019"
pw = "softtissue"

client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add("Force_n", on_message_scale)
#client.on_message = on_message

client.username_pw_set(user, pw)
client.connect(broker_address)

client.subscribe("Force_n")
client.loop_start()
while(True):
    print(scale_value.read_value())

