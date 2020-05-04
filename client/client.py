import paho.mqtt.client as mqtt
import socket
import json


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))


def init_mqtt_client():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
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


def add_expenditure(mqtt_client):
    print('Introduce the product category')
    while True:
        category = input()

        if category.isalpha():
            break

        print('Category must contain only letters!')

    print('Introduce the user name')
    username = input()

    print('Introduce the product name')
    while True:
        product_name = input()

        if product_name.isalpha():
            break

        print('Product name must contain only letters!')

    print('Introduce the product price')
    while True:
        product_price = input()

        if product_price.isdigit():
            break

        print('Product price should contain only digits!')

    print('Introduce the expenditure description')
    description = input()

    # Create a dictionary with the data received
    payload = {
        'category': category,
        'username': username,
        'product_name': product_name,
        'product_price': product_price,
        'description': description,
    }

    # Send over the broker on the /add channel
    # a JSON with the data received as a dictionary
    mqtt_client.publish('expenditure/add', json.dumps(payload))


def main():
    mqtt_client = init_mqtt_client()

    connect_mqtt_broker(mqtt_client)

    mqtt_client.loop_start()

    print('Press any key to start!')
    input()

    print('--------------------------------------------------------')
    print('Welcome to the IDP Expenditure Evidence Service!')
    print('--------------------------------------------------------')

    while True:
        print()
        print('----------------------------------------------------')
        print('Introduce the desired operation:')
        print('[1]: Add an expenditure')
        print('[2]: Exit the IDP Expenditure Evidence Service!')
        print('[x]: More soon!')
        print('----------------------------------------------------')

        operation = input()

        if operation == '1':
            add_expenditure(mqtt_client)
        elif operation == '2':
            break


if __name__ == '__main__':
    main()
