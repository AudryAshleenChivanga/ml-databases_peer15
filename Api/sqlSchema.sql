-- Drop the database if it exists (use with caution!)
DROP DATABASE IF EXISTS liver_disease_db;

-- Create the database
CREATE DATABASE liver_disease_db;
USE liver_disease_db;

-- Table: patients
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL
);

-- Table: medical_tests
CREATE TABLE IF NOT EXISTS medical_tests (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    total_bilirubin FLOAT NOT NULL,
    direct_bilirubin FLOAT NOT NULL,
    alkaline_phosphotase INT NOT NULL,
    alamine_aminotransferase INT NOT NULL,
    aspartate_aminotransferase INT NOT NULL,
    total_proteins FLOAT NOT NULL,
    albumin FLOAT NOT NULL,
    albumin_and_globulin_ratio FLOAT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- Table: diagnosis
CREATE TABLE IF NOT EXISTS diagnosis (
    diagnosis_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    diagnosis TINYINT(1) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- Stored Procedure: Calculate Average Age of Patients
DELIMITER //

CREATE PROCEDURE CalculateAverageAge()
BEGIN
    SELECT AVG(age) AS average_age FROM patients;
END //

DELIMITER ;

-- Trigger: Validate Age Before Insert
DELIMITER //

CREATE TRIGGER BeforeInsertPatient
BEFORE INSERT ON patients
FOR EACH ROW
BEGIN
    IF NEW.age < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Age cannot be negative';
    END IF;
END //

DELIMITER ;

-- Create a non-root user
CREATE USER 'app_user'@'%' IDENTIFIED BY 'StrongParam2050!';

-- Grant necessary privileges to the user
GRANT SELECT, INSERT, UPDATE, DELETE ON liver_disease_db.* TO 'app_user'@'%';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
