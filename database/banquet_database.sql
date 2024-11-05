CREATE DATABASE IF NOT EXISTS banquet_database;
USE banquet_database;

CREATE TABLE Banquet(
    BID INT AUTO_INCREMENT PRIMARY KEY,
    banquetName VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    location VARCHAR(50) NOT NULL,
    firstNameStaff VARCHAR(50) NOT NULL,
    lastNameStaff VARCHAR(50) NOT NULL,
    dateTime DATETIME NOT NULL,
    available CHAR NOT NULL,
    totalSeats INT NOT NULL
);

CREATE TABLE Attendees(
    email VARCHAR(100) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    phone CHAR(25),
    attendeeType ENUM('Student', 'Alumni', 'Staff', 'Guest') NOT NULL,
    affiliateOrganization CHAR(50),
    CHECK (email LIKE '%_@_%._%')
);

CREATE TABLE Meal(
    mealName VARCHAR(100) PRIMARY KEY,
    special VARCHAR(100),
    type VARCHAR(50)
);

CREATE TABLE Drink(
    drinkName VARCHAR(100) PRIMARY KEY,
    isAlcoholic ENUM('Yes', 'No')
);

CREATE TABLE BanquetDrinks(
    BID INT PRIMARY KEY,
    drinkName VARCHAR(100) PRIMARY KEY,
    price INT,
    FOREIGN KEY (BID) REFERENCES Banquet(BID),
    FOREIGN KEY (drinkName) REFERENCES Drink(drinkName)
);

CREATE TABLE BanquetMeals(
    BID INT PRIMARY KEY,
    mealName VARCHAR(100) PRIMARY KEY,
    price INT,
    FOREIGN KEY (BID) REFERENCES Banquet(BID),
    FOREIGN KEY (mealName) REFERENCES Meal(mealName)
);

CREATE TABLE AttendeeBanquetRegistration(
    BID INT PRIMARY KEY,
    email VARCHAR(100) PRIMARY KEY,
    mealName VARCHAR(100) NOT NULL,
    alcoholicDrink ENUM('Yes', 'No') NOT NULL,
    seatAssignment INT,
    specialNeeds VARCHAR(128),
    regDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seatingPreference1 VARCHAR(100),
    seatingPreference2 VARCHAR(100),
    CHECK (seatingPreference1 LIKE '%_@_%._%'),
    CHECK (seatingPreference2 LIKE '%_@_%._%'),
    FOREIGN KEY (BID, mealName) REFERENCES BanquetMeals(BID, mealName)
);

CREATE TABLE Administrators(
    adminEmail VARCHAR(100) PRIMARY KEY,
    adminName VARCHAR(50) NOT NULL,
    adminLastName VARCHAR(50) NOT NULL,
    adminPassword VARCHAR(50) NOT NULL
);

SHOW TABLES;