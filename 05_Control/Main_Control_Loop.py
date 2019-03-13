import paho.mqtt.client as mqtt
import json
import time
from threading import Lock

from classes.Locked_Variables import Locked_Values


scale_value = Locked_Values("Scale",1)
robot_current_position = Locked_Values("Robot Istpositionen", 3)
haptic_current_position = Locked_Values("Haptic Istpositionen", 3)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/#")

#def on_message(client, userdata, msg):
#    print(msg.topic + " " + str(msg.payload))

def on_message_scale(client, userdata, msg):
    str_msg = (msg.payload).decode('utf8')
    # print(str_msg)
    j = json.loads(str_msg)
    Fn = float(j["F_n"])
    scale_value.write_value([float((Fn))])
    #print(msg.topic + " " + str(msg.payload))
    #print("Update")

def on_message_pen(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    #j = json.load(msg.payload)
    #print(j["f1"])
    """
    TODO funktion definieren
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
def on_message_robot(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    """
    TODO funktion definieren
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
def on_message_haptic(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    #TODO Feder wieder rausnehmen
    str_msg = (msg.payload).decode('utf8')
    #print(str_msg)
    j = json.loads(str_msg)
    px = float(j["Px"])
    py = float(j["Py"])
    pz = float(j["Pz"])
    haptic_values = [px, py, pz]
    haptic_current_position.write_value(haptic_values)
    K=-200
    x = '{\"Fx\":' + str(K*px) + ', \"Fy\":'+str(K*py)+', \"Fz\":'+str(K*pz)+'}'
    #y = json.loads(x)
    client.publish("Sollwerte", x)
    """
    TODO funktion definieren
    :param client:
    :param userdata:
    :param msg:
    :return:
    """

broker_address="130.216.153.37"
user = "summer2019"
pw = "softtissue"

client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add("Force_n", on_message_scale)

# TODO Funktionen definieren
client.message_callback_add("Flex_pen", on_message_pen)
client.message_callback_add("Pos_m", on_message_haptic)
# client.message_callback_add("Current_Positions_Robot", on_message_robot)


#client.on_message = on_message

client.username_pw_set(user, pw)
print("Connect")
client.connect(broker_address)
client.loop_start()
client.subscribe("Force_n")
client.subscribe("Pos_m")
client.subscribe("Flex_pen")
#client.loop_start()


# Main Control Loop
fx= 0.1
while(True):
    # some Test JSON:
    fx= fx + 0.1

    if fx > 2:
        fx = -2
    x = '{\"Fx\":' +str(fx)+', \"Fy\":0.1, \"Fz\":0.1}'
    #print(x)
    # parse x:
    y = json.loads(x)
    #client.publish("Sollwerte", json.dumps(y))
    time.sleep(0.1)

    print(scale_value.read_value())
    #robot_current_position.write_value([1,2,3])
    #print(robot_current_position.read_value())

