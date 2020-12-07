DROP TABLE IF EXISTS covid;
DROP TABLE IF EXISTS restuarants;
DROP TABLE IF EXISTS inspections;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS trails;

CREATE TABLE covid (
    updateDate date,
    county varchar(255),
    testsPerformeted INT,
    newPostives INT,
    Primary key (county, updateDate)
);

CREATE TABLE restuarants (
    restuarantID INT,
    restuarantName varchar(255),
    restuarantAddress varchar(255),
    zipCode varchar(10),
    latitude float,
    longitude float,
    Primary Key (restuarantName,latitude,longitude)
);

CREATE TABLE inspections (
    restuarantID int, 
    InspectionDate timestamp,
    critViolations int,
    nonCritViolations int,
    Primary Key (restuarantID)
);

CREATE TABLE cities (
	city varchar(255),
    zipCode varchar(10),
    county varchar(255),
	Primary Key (zipcode)
);

CREATE TABLE trails (
    artificialKey INT NOT NULL,
    trailName varchar(255),
    latitude float,
    longitude float,
    trailLength decimal,
    Primary Key (artificialKey)
);