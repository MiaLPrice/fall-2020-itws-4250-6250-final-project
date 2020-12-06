CREATE EXTENSION IF NOT EXISTS postgis;
DROP TABLE IF EXISTS covid;
DROP TABLE IF EXISTS restuarants;
DROP TABLE IF EXISTS inspections;
DROP TABLE IF EXISTS restareas;
DROP TABLE IF EXISTS counties;
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
    located_at GEOGRAPHY,  -- will have to update once filled
    Primary Key (restuarantName,latitude,longitude)
);

CREATE TABLE inspections (
    restuarantID int, 
    InspectionDate timestamp,
    critViolations int,
    nonCritViolations int,
    Primary Key (restuarantID)
);

CREATE TABLE restareas (
    TPID varchar(10), -- should be the key 
    areaName varchar(255),
    latitude float,
    longitude float,
    located_at GEOGRAPHY, -- will have to update once filled 
    Primary Key (TPID)
);

CREATE TABLE counties (
    county varchar(255),
    countGeom POLYGON,
    Primary Key (county)
);

CREATE TABLE cities (
	city varchar(255),
    zipCode varchar(10),
    county varchar(255),
	PRIMARY KEY (zipcode)
);

CREATE TABLE trails (
    artificialKey INT NOT NULL,
    trailName varchar(255),
    latitude float,
    longitude float,
    trailLength decimal,
    Primary Key (artificialKey)
);