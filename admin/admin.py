import mysql.connector
import socket
import json
import threading
from datetime import datetime

# Constants

# Maximum payload size accepted on socket
PAYLOAD_SIZE = 1024
# Maximum number of connections allowed at the same time (only one allowed)
BACKLOG = 1

# Database connection
db_connection = None
# Database cursor
db_cursor = None


def db_connect():
    global db_connection, db_cursor

    db_connection = mysql.connector.connect(user='root',
                                            password='root',
                                            host='database',
                                            port='3306',
                                            database='expenditure_db')
    db_cursor = db_connection.cursor()

    print('Connected to the database!')


def create_listen_socket():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(('0.0.0.0', 5001))
    listen_sock.listen(BACKLOG)

    print('Created listening socket!')

    return listen_sock


def add_expenditure_remote(json_payload):
    global db_connection, db_cursor

    add_new_expenditure = (
        'INSERT INTO expenditures (username, category, product_name, product_price, product_date, description)'
        ' VALUES (%s, %s, %s, %s, %s, %s)')

    category = json_payload['category']
    username = json_payload['username']
    product_name = json_payload['product_name']
    product_price = json_payload['product_price']
    description = json_payload['description']

    data_expenditure = (category, username, product_name,
                        product_price, datetime.now(), description)
    db_cursor.execute(add_new_expenditure, data_expenditure)

    db_connection.commit()

    print('Inserted successfully!')


def delete_expenditure_remote(json_payload):
    global db_connection, db_cursor

    delete_expenditure = 'DELETE FROM expenditures WHERE ID = %s AND username = %s'

    db_cursor.execute(delete_expenditure,
                      (json_payload['ID'], json_payload['username']))

    db_connection.commit()

    print('Deleted successfully!')


# Listener thread function
def accept_connection(listen_sock):
    admin_sock, admin_addr = listen_sock.accept()

    print('[LISTENER_THREAD]: Connected to address ' + str(admin_addr))
    print('[LISTENER_THREAD]: Waiting for requests...')

    while True:
        # We only receive packages as jsons
        json_payload = admin_sock.recv(PAYLOAD_SIZE)
        if not json_payload:
            break

        print('[LISTENER_THREAD]: Received the payload ' + str(json_payload))

        json_payload = json.loads(json_payload)

        if json_payload['operation'] == 'add':
            add_expenditure_remote(json_payload)
        elif json_payload['operation'] == 'delete':
            delete_expenditure_remote(json_payload)


def add_expenditure():
    global db_connection, db_cursor

    add_new_expenditure = (
        'INSERT INTO expenditures (username, category, product_name, product_price, product_date, description)'
        ' VALUES (%s, %s, %s, %s, %s, %s)')

    print('Introduce the product category')
    category = input()

    print('Introduce the user name')
    username = input()

    print('Introduce the product name')
    product_name = input()

    print('Introduce the product price')
    while True:
        product_price = input()

        if product_price.isdigit():
            break

        print('Product price should contain only digits!')

    print('Introduce the expenditure description')
    description = input()

    data_expenditure = (category, username, product_name,
                        product_price, datetime.now(), description)
    db_cursor.execute(add_new_expenditure, data_expenditure)

    db_connection.commit()

    print('Inserted successfully!')


def delete_expenditure():
    global db_connection, db_cursor

    delete_expenditure = 'DELETE FROM expenditures WHERE ID = %s'

    print('Introduce the expenditure ID: ')
    ID = input()

    print()

    db_cursor.execute(delete_expenditure, (ID,))

    db_connection.commit()

    print('Deleted successfully!')


def list_expenditures():
    global db_connection, db_cursor

    query = ('SELECT * FROM expenditures')

    db_cursor.execute(query)

    query_result = [(ID, username, category, product_name, product_price, product_date, description)
                    for (ID, username, category, product_name, product_price, product_date, description)
                    in db_cursor]

    print('\nExpenditures')
    print('{0: <20}'.format('ID') + '{0: <20}'.format('username') + '{0: <20}'.format('category') +
          '{0: <20}'.format('product_name') + '{0: <20}'.format('product_price') +
          '{0: <20}'.format('product_date') + '{0: <20}'.format('description'))

    for (ID, username, category, product_name, product_price, product_date, description) in query_result:
        print('{0: <20}'.format(ID) + '{0: <20}'.format(username) + '{0: <20}'.format(category) +
              '{0: <20}'.format(product_name) + '{0: <20}'.format(product_price) +
              '{0: <20}'.format(str(product_date)) + '{0: <20}'.format(description))


def main():
    global db_connection, db_cursor

    # The listener socket used for the admin connection
    listen_sock = create_listen_socket()

    print('Press any key to start!')
    input()

    db_connect()

    communication_thread = threading.Thread(
        target=accept_connection, args=(listen_sock,))
    communication_thread.start()

    print('--------------------------------------------------------')
    print('Welcome to the expenditure database administration!')
    print('--------------------------------------------------------')

    while True:
        print()
        print('----------------------------------------------------')
        print('Introduce the desired operation:')
        print('[1]: Add expenditure!')
        print('[2]: Delete expenditure!')
        print('[3]: List expenditures!')
        print('[4]: Exit the plane flights database administration!')
        print('----------------------------------------------------')

        operation = input()

        if operation == '1':
            add_expenditure()
        if operation == '2':
            delete_expenditure()
        elif operation == '3':
            list_expenditures()
        elif operation == '4':
            break

    communication_thread.join()


if __name__ == '__main__':
    main()
