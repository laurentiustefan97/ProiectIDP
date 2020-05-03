import mysql.connector
import socket
import json
import threading

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


def main():
    global db_connection, db_cursor

    # The listener socket used for the admin connection
    listen_sock = create_listen_socket()

    print('Press any key to start!')
    input()

    db_connect()

    communication_thread = threading.Thread(target=accept_connection, args=listen_sock)

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

        if operation == '4':
            break


    communication_thread.join()


if __name__ == '__main__':
    main()
