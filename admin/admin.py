import mysql.connector
import socket

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
        payload = admin_sock.recv(PAYLOAD_SIZE)
        if not payload:
            break
        print('Received the payload ' + str(payload))


def main():
    # The listener socket used for the admin connection
    listen_sock = create_listen_socket()

    print('Press any key to start!')
    input()

    db_connect()

    # TODO create a thread that communicates with the admin, and the current
    # thread deals with CLI commands
    accept_connection(listen_sock)


if __name__ == '__main__':
    main()
