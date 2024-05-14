CREATE DATABASE IF NOT EXISTS bsi;

USE bsi;

CREATE TABLE IF NOT EXISTS locations
(
    ID_location SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    latitude    DOUBLE(10, 8)     NOT NULL,
    longitude   DOUBLE(10, 8)     NOT NULL,
    PRIMARY KEY (ID_location),
    UNIQUE KEY (latitude, longitude)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS area
(
    ID_area      SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ID_location1 SMALLINT UNSIGNED NOT NULL,
    ID_location2 SMALLINT UNSIGNED NOT NULL,
    ID_location3 SMALLINT UNSIGNED NOT NULL,
    ID_location4 SMALLINT UNSIGNED NOT NULL,
    ID_location5 SMALLINT UNSIGNED NOT NULL,
    ID_location6 SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (ID_area),
    FOREIGN KEY location1 (ID_location1) REFERENCES locations (ID_location),
    FOREIGN KEY location2 (ID_location2) REFERENCES locations (ID_location),
    FOREIGN KEY location3 (ID_location3) REFERENCES locations (ID_location),
    FOREIGN KEY location4 (ID_location4) REFERENCES locations (ID_location),
    FOREIGN KEY location5 (ID_location5) REFERENCES locations (ID_location),
    FOREIGN KEY location6 (ID_location6) REFERENCES locations (ID_location)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS detection_results
(
    ID_detection_result INTEGER UNSIGNED  NOT NULL AUTO_INCREMENT,
    location            SMALLINT UNSIGNED NOT NULL,
    detection_time      TIMESTAMP         NOT NULL DEFAULT NOW(),
    area_computed       BIT               NOT NULL DEFAULT b'0',
    PRIMARY KEY (ID_detection_result),
    FOREIGN KEY location (location) REFERENCES locations (ID_location)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS area_detection_results
(
    ID_area_result        INTEGER UNSIGNED  NOT NULL AUTO_INCREMENT,
    ID_area               SMALLINT UNSIGNED NOT NULL,
    area_detection_result TINYINT           NOT NULL DEFAULT 0,
    area_detection_time   TIMESTAMP         NOT NULL DEFAULT NOW(),
    PRIMARY KEY (ID_area_result),
    UNIQUE KEY (ID_area, area_detection_time)
) ENGINE = InnoDB;