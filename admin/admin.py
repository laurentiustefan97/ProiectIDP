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

    # TODO environment variables for the database credentials
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


def accept_connection(listen_sock):
    admin_sock, admin_addr = listen_sock.accept()

    print('Connected to address ' + str(admin_addr))
    print('Waiting for requests...')

    while True:
        # We only receive packages as jsons
        json_payload = admin_sock.recv(PAYLOAD_SIZE)
        if not json_payload:
            break

        json_payload = json.loads(json_payload)

        print('Received the payload ' + str(json_payload))


def add_expenditure():
    global db_connection, db_cursor

    add_new_expenditure = (
        'INSERT INTO expenditures (username, category, product_name, product_price, product_date, description)'
        ' VALUES (%s, %s, %s, %s, %s, %s)')

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

    data_expenditure = (category, username, product_name,
                        product_price, datetime.now(), description)
    db_cursor.execute(add_new_expenditure, data_expenditure)

    db_connection.commit()

    print('Inserted successfully!')


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
              '{0: <20}'.format(product_date) + '{0: <20}'.format(description))


def main():
    global db_connection, db_cursor

    # The listener socket used for the admin connection
    listen_sock = create_listen_socket()

    print('Press any key to start!')
    input()

    db_connect()

    communication_thread = threading.Thread(
        target=accept_connection, args=listen_sock)

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
        elif operation == '3':
            list_expenditures()
        elif operation == '4':
            break

    communication_thread.join()


if __name__ == '__main__':
    main()
