-- Création de la base de données
CREATE DATABASE db_comparators;

-- Connexion à la base de données
\c db_comparators;

-- Création des tables
-- Table Product_State
CREATE TABLE Product_State (
    ID_state SERIAL PRIMARY KEY,
    State_label VARCHAR(255)
);

-- Table Categories
CREATE TABLE Categories (
    ID_category SERIAL PRIMARY KEY,
    Category_name VARCHAR(255)
);

-- Table Products
CREATE TABLE Products (
    ID_product SERIAL PRIMARY KEY,
    Product_label VARCHAR(255),
    Ticket_label VARCHAR(255),
    Barcode VARCHAR(255),
    ID_category INTEGER REFERENCES Categories(ID_category),
    Image VARCHAR(255),
    ID_state INTEGER REFERENCES Product_State(ID_state),
    Product_creation_date DATE,
    Product_modification_date DATE
);

-- Table Store_Price
CREATE TABLE Store_Price (
    ID_Store_Price SERIAL PRIMARY KEY,
    ID_product INTEGER REFERENCES Products(ID_product),
    ID_store INTEGER,
    Price NUMERIC,
    Price_creation_date DATE,
    Price_modification_date DATE,
    VAT NUMERIC
);

-- Table Store
CREATE TABLE Store (
    ID_store SERIAL PRIMARY KEY,
    Store_label VARCHAR(127),
    Address VARCHAR(255),
    Postal_code INTEGER,
    City VARCHAR(50),
    Longitude NUMERIC,
    Latitude NUMERIC,
    Store_creation_date DATE,
    Store_modification_date DATE
);

-- Clé étrangère entre Store_Price et Store
ALTER TABLE Store_Price
ADD CONSTRAINT fk_store FOREIGN KEY (ID_store) REFERENCES Store(ID_store);