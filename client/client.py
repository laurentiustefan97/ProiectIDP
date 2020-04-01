import paho.mqtt.client as mqtt
import socket


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def init_mqtt_client():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
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


def add_expenditure(mqtt_client):
    print('Introduce the product category')
    category = input()

    print('Introduce the user name')
    username = input()

    print('Introduce the product name')
    product_name = input()

    print('Introduce the product price')
    product_price = input()

    print('Introduce the expenditure date')
    date = input()

    # TODO send over the MQTT client a json with the data
    mqtt_client.publish("IDP", "todo")


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
