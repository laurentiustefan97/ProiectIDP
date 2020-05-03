import mysql.connector

def main():
    print('Press any key to start!')
    input()
    print ('You got here')

    connection = mysql.connector.connect(user='root',
                                         password='root',
                                         host='database',
                                         port='3306',
                                         database='expenditure_db')
    cursor = connection.cursor()

    print ('You got even here')

if __name__ == '__main__':
    main()
