create database scraping;
use scraping;

CREATE TABLE chocolate_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    url VARCHAR(2083) NOT NULL
);

SELECT * FROM chocolate_products;
