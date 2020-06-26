CREATE TABLE `sprinkle`.`sprinkle_log` ( `gpioID` TEXT NOT NULL , `gpioName` TEXT NOT NULL , `date_time` TEXT NOT NULL , `runtime` TEXT NOT NULL ) ENGINE = InnoDB;
CREATE TABLE `sprinkle`.`sprinkle_config` ( `gpioID` TEXT NOT NULL , `gpioName` TEXT NOT NULL , `runtime` TEXT NOT NULL , `status` TEXT NOT NULL ) ENGINE = InnoDB;
INSERT INTO `sprinkle_config` (`gpioID`, `gpioName`, `runtime`, `status`) VALUES ('14', 'Front', '10', 'Stopped'), ('5', 'Terrace', '10', 'Stopped'), ('23', 'Japanese', '10', 'Stopped'), ('12', 'Grill-Kitchen', '10', 'Stopped') , ('3', 'Fruit 1', '10', 'Stopped') , ('2', 'Fruit 2', '10', 'Stopped') , ('17', 'Backup', '10', 'Stopped') , ('9', 'Pump', '10', 'Stopped')

