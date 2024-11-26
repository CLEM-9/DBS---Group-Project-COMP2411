CREATE DATABASE IF NOT EXISTS banquet_database;
USE banquet_database;

CREATE TABLE IF NOT EXISTS Attendees(
    email VARCHAR(100) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    phone CHAR(8),
    attendeeType ENUM('Student', 'Alumni', 'Staff', 'Guest') NOT NULL,
    affiliateOrganization CHAR(50),
    CHECK (email LIKE '%_@_%._%')
);

CREATE TABLE IF NOT EXISTS Banquet (
    BID INT AUTO_INCREMENT PRIMARY KEY,
    banquetName VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    location VARCHAR(50) NOT NULL,
    staffEmail VARCHAR(100) NOT NULL,
    banquetDate DATE NOT NULL,
    banquetTime TIME NOT NULL,
    available ENUM('Yes', 'No'),
    totalSeats INT NOT NULL,
    FOREIGN KEY (staffEmail) REFERENCES Attendees(email)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT unique_banquet UNIQUE (address, location, banquetDate)
);

CREATE TABLE IF NOT EXISTS Meal(
    mealName VARCHAR(100) PRIMARY KEY,
    special VARCHAR(100),
    type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Drink(
    drinkName VARCHAR(100) PRIMARY KEY,
    isAlcoholic BIT
);

CREATE TABLE IF NOT EXISTS BanquetDrinks(
    BID INT,
    drinkName VARCHAR(100),
    price INT,
    PRIMARY KEY (BID, drinkName),
    FOREIGN KEY (BID) REFERENCES Banquet(BID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (drinkName) REFERENCES Drink(drinkName)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS BanquetMeals(
    BID INT,
    mealName VARCHAR(100),
    price INT,
    PRIMARY KEY (BID, mealName),
    FOREIGN KEY (BID) REFERENCES Banquet(BID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (mealName) REFERENCES Meal(mealName)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS UserBanquetRegistration(
    BID INT,
    email VARCHAR(100),
    mealName VARCHAR(100) NOT NULL,
    alcoholicDrink BIT NOT NULL,
    seatAssigned INT,
    specialNeeds VARCHAR(128),
    regDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seatingPreference1 VARCHAR(100),
    seatingPreference2 VARCHAR(100),
    PRIMARY KEY (BID, email),
    CHECK (seatingPreference1 LIKE '%_@_%._%'),
    CHECK (seatingPreference2 LIKE '%_@_%._%'),
    FOREIGN KEY (BID) REFERENCES BanquetMeals(BID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (mealName) REFERENCES BanquetMeals(mealName)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (email) REFERENCES Attendees(email)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Administrators(
    adminEmail VARCHAR(100) PRIMARY KEY,
    adminName VARCHAR(50) NOT NULL,
    adminLastName VARCHAR(50) NOT NULL,
    adminPassword VARCHAR(50) NOT NULL
);

SHOW TABLES;