import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server. 
def on_connect(client, userdata, flags, rc): 
    print("Connected with result code " + str(rc)) 
 
    # Subscribing in on_connect() means that if we lose the connection and 
    # reconnect then subscriptions will be renewed. 
    client.subscribe("laur/#") 
 
# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg): 
    print(msg.topic+" "+str(msg.payload)) 

def init_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    return client

def main():
    client = init_mqtt_client()

    client.connect('localhost', 1883, 1883)

    client.loop_start()

    while True:
        client.publish("laur/test", input())

if __name__ == '__main__':
    main()
