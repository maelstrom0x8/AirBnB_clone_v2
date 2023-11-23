-- A script to set sql database server

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'fargo'@'localhost' IDENTIFIED BY 'aeflheim';
GRANT ALL PRIVILEGES ON sceptre.* TO 'fargo'@'localhost';
GRANT SELECT ON performance_schema.* TO 'fargo'@'localhost';
