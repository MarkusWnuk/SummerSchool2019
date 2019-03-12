import paho.mqtt.client as mqtt
import time

counter = 1
timelast = time.time()
delaysum = 0
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    #print(time.time())
    global counter
    global delaysum
    global timelast
    timenew = time.time()
    delay = (timenew-timelast)
    delaysum = delaysum + delay
    delayave = delaysum/counter
    timelast = timenew
    counter = counter +1
    print(delay)
    print(delayave)



broker_address="130.216.153.37"
user = "summer2019"
pw = "softtissue"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(user, pw)
client.connect(broker_address)

client.subscribe("Force_n")
client.loop_forever()