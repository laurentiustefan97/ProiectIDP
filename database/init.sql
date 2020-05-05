CREATE DATABASE IF NOT EXISTS expenditure_db;

use expenditure_db;
CREATE TABLE IF NOT EXISTS expenditures (
  ID INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50),
  category VARCHAR(50),
  product_name VARCHAR(50),
  product_price INT,
  product_date DATETIME,
  description VARCHAR(200),
  PRIMARY KEY (ID)
);

# Inserting data in database for demonstration purposes
INSERT INTO expenditures
VALUES(1, 'laur', 'car', 'logan', 50000, '2020-05-05 13:00:00', 'my new car');

INSERT INTO expenditures
VALUES(2, 'lucian', 'car', 'audi 15', 3000000, '2020-05-02 8:00:00', 'birthday presence');

INSERT INTO expenditures
VALUES(3, 'viorel', 'car', 'bmw i8', 400000, '2020-04-25 15:50:00', 'for my son');

INSERT INTO expenditures
VALUES(4, 'laur', 'accessories', 'necklance', 50000, '2020-05-04 18:30:00', 'for my gf');

INSERT INTO expenditures
VALUES(5, 'maria', 'book', 'lord of the rings 1', 200, '2020-03-05 22:30:00', 'i love LOTR');

INSERT INTO expenditures
VALUES(6, 'maria', 'book', 'lord of the rings 2', 200, '2020-04-05 22:30:00', 'i love LOTR');

INSERT INTO expenditures
VALUES(7, 'maria', 'book', 'lord of the rings 3', 200, '2020-05-05 22:30:00', 'i love LOTR');

INSERT INTO expenditures
VALUES(8, 'maria', 'accessories', 'necklance', 30000, '2020-05-05 22:30:00', 'i am rich btw');

INSERT INTO expenditures
VALUES(9, 'maria', 'accessories', 'bracelet', 20000, '2020-05-05 22:30:00', 'i am rich btw');

INSERT INTO expenditures
VALUES(10, 'maria', 'accessories', 'earrings', 25000, '2020-05-05 22:30:00', 'i am rich btw');
