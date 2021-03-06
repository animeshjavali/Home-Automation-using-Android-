import paho.mqtt.client as mqtt
import os, urlparse
import serial 
ser=serial.Serial('COM4')# Start serial communication.


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " "+str(msg.payload))
    if(msg.payload=="ON"):# If mqtt message is "ON", send 1 to Arduino(via UART).
    	ser.write('1')
    	print('1')
    elif(msg.payload=="OFF"):# If mqtt message is "OFF", send 2 to Arduino(via UART).
    	ser.write('2')

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
	print(string)
mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

#Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
url = urlparse.urlparse(url_str)
topic = url.path[1:] or 'my_IoT' #Define a unique topic on CloudMQTT dashboard.

# Connect
mqttc.username_pw_set('zzilcrwd', 'iL_24499QHb1')#Unique username and password given to a user on CloudMQTT.
mqttc.connect('m14.cloudmqtt.com', 17237)#(webserver,port number).

# Start subscribe, with QoS level 0
mqttc.subscribe(topic, 0)

# Publish a message


# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))
