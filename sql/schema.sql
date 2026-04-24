-- Database Schema for Aviation Carbon Tracker
CREATE DATABASE IF NOT EXISTS JetTrackerDB;
USE JetTrackerDB;

-- Main table for aircraft telemetry and stats
CREATE TABLE AircraftStats (
    TailNumber VARCHAR(20) PRIMARY KEY,
    CelebrityName VARCHAR(100),
    AircraftModel VARCHAR(100),
    HexCode VARCHAR(10) UNIQUE,
    GallonsPerMile DECIMAL(10, 2),
    AircraftStatus VARCHAR(50) DEFAULT 'Unknown',
    CurrentLat DECIMAL(10, 6),
    CurrentLon DECIMAL(10, 6),
    LastLocation VARCHAR(255),
    TotalMiles DECIMAL(15, 2) DEFAULT 0.00
);

-- Table for tracking takeoff/landing events
CREATE TABLE FlightHistory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    HexCode VARCHAR(10),
    Event VARCHAR(50), -- e.g., 'Takeoff', 'Landing', 'Ping'
    LocationName VARCHAR(255),
    DistanceCovered DECIMAL(10, 2),
    LogTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (HexCode) REFERENCES AircraftStats(HexCode)
);
