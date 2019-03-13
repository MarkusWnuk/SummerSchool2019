import paho.mqtt.client as mqtt
import json
import time
from threading import Lock

from classes.Locked_Variables import Locked_Values

#Initialize the locked variables
scale_current_force = Locked_Values("Scale",1, "Force_n")                                             #Scale Value Normal Force [N]
robot_current_position = Locked_Values("Robot Istpositionen", 3, "Robot_CurrentPos")                #Robot Current Position x,y,z // [m,m,m]
haptic_current_position = Locked_Values("Haptic Istpositionen", 3, "Pos_m")                         #Haptic device Current Position x,y,z // [m,m,m]
robot_target_position = Locked_Values("Robot Target Position", 3, "Robot_TargetPos")                #Robot Target position x,y,z // [m,m,m]
haptic_target_forces = Locked_Values("Haptic Target Forces", 3,"Sollwerte")                          #Haptic Target Forces Fx,Fy,Fz // [N,N,N]
pen_current_force = Locked_Values("Scale",2,"Flex_pen")
mainLoopFlag = True

# Information about the Broker
broker_address="130.216.153.37"
user = "summer2019"
pw = "softtissue"

#Callback for Connect
def on_connect(client, userdata, flags, rc):
    """Callback for the connect of the MQTT client
                Raises:
                    Prints the error code of the connection
                Returns:
                  Prints out if the connect worked
                """
    print("Connected with result code " + str(rc))
    #client.subscribe("test/#")


def on_disconnect(client, userdata, rc):
    """Callback for the disconnect of the MQTT client
    changes the mainLoopFlag to False --> Breaks the main loop
                    Raises:
                        Exception of the disconnect reason
                    Returns:
                      Prints out if the the error message
                    """
    global mainLoopFlag             #Flag to start and stop the main Control Loop
    print("Error:Client is disconnected")
    mainLoopFlag = False            # Stops the main Loop by setting the Flag to False
    raise Exception("disconnecting reason  " + str(rc))



#def on_message(client, userdata, msg):
#    print(msg.topic + " " + str(msg.payload))

def on_message_scale(client, userdata, msg):
    """Callback for Message of the scale
    Writes to the attomic values of the scale variables
                    Args:
                        msg: String Data of the Scale Message {F_n:<value>}
                    Returns:
                      Prints out if the the error message
                    """
    str_msg = (msg.payload).decode('utf8')      #Decode to Message to utf8
    # print(str_msg)
    j = json.loads(str_msg)                     #Translate the String in a Json Format (as in Description)
    Fn = float(j["F_n"])                        #Readout the Normalforce
    scale_current_force.write_value([float((Fn))]) #write the Normal Force to the attomic variable of the scale
    #print(msg.topic + " " + str(msg.payload))
    #print("Update")

def on_message_pen(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    #j = json.load(msg.payload)
    #print(j["f1"])
    """Callback for Message of the pen
    Writes to the attomic values of the scale variables
                    Args:
                        msg: String Data of the Scale Message TODO {}
                    Returns:
                      Prints out if the the error message
                    """
    # TODO Read/Decode the msg.payload
    # TODO #Translate the String in a Json Format (as in Description)
    # TODO # Readout the Forces
    # TODO # write the Normal Force to the attomic variables of the scale
def on_message_robot(client, userdata, msg):
    #rint(msg.topic + " " + str(msg.payload))
    """Callback for Message of the robot current positions
    Writes to the attomic values of the scale variables
                    Args:
                        msg: String Data of the Scale Message TODO {}
                    Returns:
                      Prints out if the the error message
                    """
    # TODO Read/Decode the msg.payload
    # TODO #Translate the String in a Json Format (as in Description)
    # TODO # Readout the Current Positions
    # TODO # write the Normal Force to the attomic variable of the scale

def on_message_haptic(client, userdata, msg):
    """Callback for Message of the haptic current positions
    Writes to the attomic values of the haptic variables
                    Args:
                        msg: String Data of the Scale Message TODO {}
                    Returns:
                      Prints out if the the error message
                    """
    #print(msg.topic + " " + str(msg.payload))
    #TODO Feder wieder rausnehmen
    str_msg = (msg.payload).decode('utf8')           #Decode to Message to utf8
    #print(str_msg)
    j = json.loads(str_msg)                          #Translate the String in a Json Format (as in Description)
    px = float(j["Px"])                              #Readout the x Position
    py = float(j["Py"])                              #Readout the y Position
    pz = float(j["Pz"])                              #Readout the z Position
    haptic_values = [px, py, pz]
    haptic_current_position.write_value(haptic_values)# write the current Positions to the attomic variables of the scale
    #K=-200
    #x = '{\"Fx\":' + str(K*px) + ', \"Fy\":'+str(K*py)+', \"Fz\":'+str(K*pz)+'}'

    #client.publish("Sollwerte", x)



client = mqtt.Client()                      # Define MQTT Client
client.on_connect = on_connect              # Register callback function for the connect
client.on_disconnect = on_disconnect        # Register callback function for the disconnect (safty)

#Register the specific message callbacks
client.message_callback_add(scale_current_force.topic, on_message_scale)
# TODO Funktionen definieren
client.message_callback_add(pen_current_force.topic, on_message_pen)
client.message_callback_add(haptic_current_position.topic, on_message_haptic)
# client.message_callback_add("Current_Positions_Robot", on_message_robot)


#client.on_message = on_message

client.username_pw_set(user, pw)                    # Set the Username and Password

client.connect(broker_address)                      # Connect to broker
client.loop_start()                                 # Start Loop as a separate Thread
client.subscribe(scale_current_force.topic)         # Subscribe to Topic of Scale
client.subscribe(haptic_current_position.topic)     # Subscribe to Topic of Haptic
client.subscribe(pen_current_force.topic)           # Subscribe to Topic of Pen
#client.loop_start()


# Main Control Loop
fx= 0.1
print(mainLoopFlag)
while(mainLoopFlag):

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

    print(scale_current_force.read_value())
    #robot_current_position.write_value([1,2,3])
    #print(robot_current_position.read_value())

