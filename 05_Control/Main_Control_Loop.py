import paho.mqtt.client as mqtt
import json
import time
import math
from threading import Lock

from classes.Locked_Variables import Locked_Values

alpha=135.0/180.0*math.pi
c_r=math.cos(alpha)
s_r=math.sin(alpha)


#Initialize the locked variables
scale_current_force = Locked_Values("Scale",1, "Force_n")                                             #Scale Value Normal Force [N]
robot_current_position = Locked_Values("Robot Istpositionen", 3, "Robot_CurrentPos")                #Robot Current Position x,y,z // [m,m,m]
haptic_current_position = Locked_Values("Haptic Istpositionen", 3, "Pos_m")                         #Haptic device Current Position x,y,z // [m,m,m]
robot_target_position = Locked_Values("Robot Target Position", 3, "Robot_m")                #Robot Target position x,y,z // [m,m,m]
haptic_target_forces = Locked_Values("Haptic Target Forces", 3,"Sollwerte")                          #Haptic Target Forces Fx,Fy,Fz // [N,N,N]
pen_current_force = Locked_Values("Scale",2,"Flex_pen")
mainLoopFlag = True
deadmanswitch = False

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
    str_msg = (msg.payload).decode('utf8')           #Decode to Message to utf8
    print(str_msg)
    j = json.loads(str_msg)                          #Translate the String in a Json Format (as in Description)
    px = float(j["Px"])                              #Readout the x Position
    py = float(j["Py"])                              #Readout the y Position
    pz = float(j["Pz"])                              #Readout the z Position
    haptic_values = [px, py, pz]
    haptic_current_position.write_value(haptic_values)# write the current Positions to the attomic variables of the scale
    #K=-200
    #x = '{\"Fx\":' + str(K*px) + ', \"Fy\":'+str(K*py)+', \"Fz\":'+str(K*pz)+'}'

    #client.publish("Sollwerte", x)

def on_message_saftybutton(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    # j = json.load(msg.payload)
    # print(j["f1"])

    """Callback for Message of the pen
        Writes to the attomic values of the scale variables
                        Args:
                            msg: String Data of the Scale Message TODO {}
                        Returns:
                          Prints out if the the error message
                        """
    global deadmanswitch
    str_msg = (msg.payload).decode('utf8')  # Decode to Message to utf8
    j = json.loads(str_msg)                 # Translate the String in a Json Format (as in Description)
    deadmanswitch = bool(j["Button"])       # Save value to global variable





client = mqtt.Client()                      # Define MQTT Client
client.on_connect = on_connect              # Register callback function for the connect
client.on_disconnect = on_disconnect        # Register callback function for the disconnect (safty)

#Register the specific message callbacks
client.message_callback_add(scale_current_force.topic, on_message_scale)    #Scale
client.message_callback_add(pen_current_force.topic, on_message_pen)        #Pen
client.message_callback_add(haptic_current_position.topic, on_message_haptic)#haptic
client.message_callback_add("SafetyButton", on_message_saftybutton)          #saftybutton
# TODO Funktionen definieren für Roboter Current Values
# client.message_callback_add("Current_Positions_Robot", on_message_robot)


#client.on_message = on_message

client.username_pw_set(user, pw)                    # Set the Username and Password

client.connect(broker_address)                      # Connect to broker
client.loop_start()                                 # Start Loop as a separate Thread
client.subscribe(scale_current_force.topic)         # Subscribe to Topic of Scale
client.subscribe(haptic_current_position.topic)     # Subscribe to Topic of Haptic
client.subscribe(pen_current_force.topic)           # Subscribe to Topic of Pen
client.subscribe("SafetyButton")                    # Subscribe to Topic of SafetyButton of Haptic
#client.loop_start()


# Main Control Loop
fx= 0.1
print(mainLoopFlag)
t=time.time()
while(mainLoopFlag):
    """
    Main Control Loop. Can be stoppen via global var mainLoopFlag
    Frequency of the control loop can be defined. The actual frequency may be slower than the defined one
    Programmed with IPO-Model
    
    Input: Reads the actual State of all the Devices
    Process: Processes the output values based on the actual State
    Output: Writes the Output Values
        
        Args:
            frequency: [Hz]
        
    """
    frequency = 125
    period = 1/frequency

    t+=period

    """
    INPUT
    -------------------------------------------------------------------
        Read all the Input Data to local state variables
        So no change of variables during one processing step is possible
    -------------------------------------------------------------------    
    """

    stateVar_haptic = haptic_current_position.read_value()
    stateVar_scale = scale_current_force.read_value()
    stateVar_pen = pen_current_force.read_value()
    stateVar_robot = robot_current_position.read_value()

    """
    PROCESS
    -------------------------------------------------------------------
        Process the data 
    -------------------------------------------------------------------    
    """

    #print(robot_current_position.read_value())


    # some Test JSON:
    #fx= fx + 0.1

    #if fx > 2:
    #    fx = -2
    """
        Haptic Device Start
        ------------------------------------------------------------------- 
    """
    fx = stateVar_scale[0]
    # DUMMYWERTE für das haptic device
    Hstr = '{\"Fx\":' + str(fx) + ', \"Fy\":0.0, \"Fz\":0.0}'
    # print(Hstr)
    Hjsn = json.loads(Hstr)
    # print(Hstr)

    Hstr_zero = '{\"Fx\":0.0, \"Fy\":0.0, \"Fz\":0.0}'
    Hjsn_zero = json.loads(Hstr_zero)
    """ 
        -------------------------------------------------------------------
    """


    # Sollwerte für den Roboter
    # Direkt die Statevariablen des haptic device durchschicken
    rx_t = stateVar_haptic[0]
    ry_t = stateVar_haptic[1]
    rz_t = stateVar_haptic[2]

    # Koordinatentrafo
    rx = c_r * rx_t - s_r * ry_t
    ry = s_r * rx_t + c_r * ry_t
    rz=rz_t
    Rstr = '{\"Px\":' + str(rx) + ', \"Py\":' + str(ry)+ ', \"Pz\":' + str(rz)+'}'
    Rjsn = json.loads(Rstr)

    # print(scale_current_force.read_value())
    #robot_current_position.write_value([1,2,3])
    #print(robot_current_position.read_value())
    #print("t " + str(t))
    #print("Period " + str(t - time.time()))

    """
        OUTPUT
        -------------------------------------------------------------------
            Deprocess the output data and publish the data over MQTT
        -------------------------------------------------------------------    
        """
    # print(deadmanswitch)
    if(deadmanswitch):
        # Write Robot Values
        client.publish("Robot_m", json.dumps(Rjsn))
        # print(Rstr)
        # Write Haptic Values
        client.publish("Sollwerte", json.dumps(Hjsn))
    else:
        # Write Haptic Values Zero
        client.publish("Sollwerte", json.dumps(Hjsn_zero))

    #print("Period: " + str(t - time.time()) + "s")
    time.sleep(max(0, t - time.time()))     #wait function for keep frequency of the loop

