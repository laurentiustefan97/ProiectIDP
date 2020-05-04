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
