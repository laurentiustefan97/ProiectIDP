import paho.mqtt.client as mqtt
import socket
import time
import json

# Constants

ADMIN_SERVICE = "admin"
ADMIN_PORT = 5001

# The socket used for the communication with the admin
admin_sock = None


def on_connect(mqtt_client, userdata, flags, rc):
    print('Connected with result code ' + str(rc) + '\n')

    mqtt_client.subscribe('expenditure/#')


def process_add(payload):
    global admin_sock

    print('The operation received is add!')
    print('The payload is ' + str(payload))

    admin_sock.send(payload)


def process_delete(payload):
    global admin_sock

    print('The operation received is delete!')
    print('The payload is ' + str(payload))

    # Sending the json string to the admin
    admin_sock.send(payload)


# The callback for when a PUBLISH message is received from an IOT device
def on_message(mqtt_client, userdata, msg):
    print('Received a message on the topic [' + msg.topic + ']')

    # Take the name of the operation after 'expenditure/'
    operation = msg.topic.split('/')[1]

    # Process the requested operation
    if operation == 'add':
        process_add(msg.payload)
    elif operation == 'delete':
        process_delete(msg.payload)


def init_mqtt_client():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    return mqtt_client


def connect_mqtt_broker(mqtt_client):
    while True:
        try:
            # Connect to the mqtt broker on port 1883
            mqtt_client.connect('mqtt-broker', 1883, 60)
        except socket.gaierror:
            print('Failed to connect to mqtt broker!')
            continue
        break

    # Wait requests from the client
    mqtt_client.loop_forever()


def connect_socket():
    global admin_sock

    admin_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    admin_sock.connect((ADMIN_SERVICE, ADMIN_PORT))


def main():
    # Connect to the admin service
    connect_socket()

    # Create the mqtt client
    mqtt_client = init_mqtt_client()

    # Connect to the mqtt broker
    connect_mqtt_broker(mqtt_client)


if __name__ == '__main__':
    main()
