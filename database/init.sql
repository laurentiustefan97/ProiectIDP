CREATE DATABASE IF NOT EXISTS expenditure_db;
use expenditure_db;

CREATE TABLE IF NOT EXISTS flights (
  ID VARCHAR(10) PRIMARY KEY,
  category VARCHAR(50),
  product_name VARCHAR(50),
  product_price INT,
  product_date DATE,
  description VARCHAR(200)
);
