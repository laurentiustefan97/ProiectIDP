import paho.mqtt.client as mqtt


def on_connect(mqtt_client, userdata, flags, rc):
    print('Connected with result code ' + str(rc) + '\n')

    # TODO subscribe to a specific channel
    mqtt_client.subscribe("IDP")


# The callback for when a PUBLISH message is received from an IOT device
def on_message(mqtt_client, userdata, msg):
    print('Received a message on the topic ' + msg.topic)
    # TODO receive json with the data and parse it
    print('the payload is ' + msg.payload)
    my_data = msg.payload


def init_mqtt_client():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    return mqtt_client


def connect_mqtt_broker(mqtt_client):
    while True:
        try:
            # Connect to the mqtt broker on port 1883
            mqtt_client.connect("mqtt-broker", 1883, 60)
        except socket.gaierror:
            print("Failed to connect to mqtt broker!")
            continue
        break

    print('looping forever')
    mqtt_client.loop_forever()
    print('stopped looping')


def main():
    # Wait for the environment completion
    mqtt_client = init_mqtt_client()

    connect_mqtt_broker(mqtt_client)


if __name__ == '__main__':
    main()
