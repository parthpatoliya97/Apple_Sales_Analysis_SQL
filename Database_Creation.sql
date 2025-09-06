-- Create the database
CREATE DATABASE IF NOT EXISTS apple_sales;
USE apple_sales;

-- Create category table
CREATE TABLE category (
    category_id VARCHAR(10) PRIMARY KEY,
    category_name VARCHAR(20) NOT NULL
);

-- Create store table
CREATE TABLE store (
    store_id VARCHAR(10) PRIMARY KEY,
    store_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- Create products table
CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(35) NOT NULL,
    category_id VARCHAR(10) NOT NULL,
    launch_date DATE NOT NULL,
    price DOUBLE NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

-- Create sales table
CREATE TABLE sales (
    sale_id VARCHAR(15) PRIMARY KEY,
    sale_date DATE NOT NULL,
    store_id VARCHAR(10) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (store_id) REFERENCES store(store_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create warranty table
CREATE TABLE warranty (
    claim_id VARCHAR(10) PRIMARY KEY,
    claim_date DATE NOT NULL,
    sale_id VARCHAR(15) NOT NULL,
    repair_status VARCHAR(15) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id)
);
