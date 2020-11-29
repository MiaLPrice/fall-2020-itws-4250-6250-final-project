DROP DATABASE IF EXISTS final-project;
CREATE DATABASE final-project;

DROP USER IF EXISTS databasestudent;
CREATE USER databasestudent WITH PASSWORD 'restaurant';

GRANT ALL PRIVILEGES ON DATABASE final-project TO databasestudent;
