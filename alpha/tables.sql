DROP TABLE IF EXISTS dorm;
CREATE TABLE dorm(
	dormID char(3) NOT NULL PRIMARY KEY,  
	dormName enum("Bates", "Beebe", "Cazenove", "Cervantes", "Claflin", "Dower",
	"Freeman", "French House", "Hemlock", "Instead", "Lake House", "McAfee", 
	"Munger", "Orchard", "Pomeroy","Severance", "Shafer", "Simpson West", "Stone Davis", 
	"Tower Court East", "Tower Court West") NOT NULL,
	location enum("East", "West") NOT NULL,
	dormType enum("Dorm","Apartment") NOT NULL, 
	gym tinyint(1) NOT NULL,		/*0 if no gym, 1 if there's a gym*/
	dinningHall tinyint(1) NOT NULL /*0 if no dinninghall, 1 if there's a dinninghall*/
	)
	-- table constraints follow                                              
       ENGINE = InnoDB;

/*update the gym part*/
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("BAT", "Bates", "East", "Dorm", 0, 1); 
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("BEB", "Beebe", "West", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("CAZ", "Cazenove", "West", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("CER", "Cervantes", "West", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("CLA", "Claflin", "West", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("DOW", "Dower", "East", "Dorm", 0, 1); 
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("FRE", "Freeman", "East", "Dorm", 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("FHC", "French House", "East", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("HEM", "Hemlock", "East", "Apartment", 1, 0); 
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("INS", "Instead", "East", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("LAK", "Lake House", "West", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("MAC", "McAfee", "East", "Dorm", 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("MUN", "Munger", "West", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("ORC", "Orchard", "East", "Apartment", 1, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("POM", "Pomeroy", "West", "Dorm", 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("SEV", "Severance", "West", "Dorm", 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("SHA", "Shafer", "West", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("SMW", "Simpson West", "East", "Apartment", 1, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("STO", "Stone Davis", "East", "Dorm", 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("TCE", "Tower Court East", "West", "Dorm", 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, gym, dinningHall)  VALUES ("TCW", "Tower Court West", "West", "Dorm", 0, 1);

/* is if fine to have both foreign key and primary key?*/
DROP TABLE IF EXISTS room;
CREATE TABLE room(
	dormID char(3) NOT NULL, 
	roomNumber char(3) NOT NULL, 
	roomType enum("Single", "Double", "Suite", "Triple", "First Year"),
	avgRating decimal(3,2),
	FOREIGN KEY (dormID) REFERENCES dorm(dormID) ON DELETE CASCADE, 
	PRIMARY KEY (roomNumber,dormID)
	)
	-- table constraints follow                                              
       ENGINE = InnoDB;

INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("MUN", "234", "Single");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("MUN", "334", "Single");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("MUN", "125", "Single");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("SEV", "125", "Single");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("POM", "504", "Single");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("BEB", "200", "Double");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("DOW", "001", "Triple");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("STO", "334", "Single");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("HEM", "125", "Single");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("TCW", "125", "Double");
INSERT INTO room (dormID, roomNumber, roomType)  VALUES ("TCE", "504", "First Year");

DROP TABLE IF EXISTS user;
CREATE TABLE user(
	BID char(9) NOT NULL PRIMARY KEY, 
	email varchar(30) NOT NULL,  
	pwd varchar(20) NOT NULL,
	classYear int(4)NOT NULL
	)
	-- table constraints follow                                              
       ENGINE = InnoDB;

DROP TABLE IF EXISTS userpass;
CREATE TABLE userpass(
	BID varchar(30) NOT NULL, 
	hashed char(50) NOT NULL,
	FOREIGN KEY (BID) REFERENCES user(BID) ON DELETE CASCADE
	)
	-- table constraints follow                                              
       ENGINE = InnoDB;

DROP TABLE IF EXISTS review;
CREATE TABLE review(
	dormID char(3) NOT NULL,
	roomNumber char(3) NOT NULL,
	BID char(8) NOT NULL,
	rating tinyint(5) NOT NULL, 
	comment varchar(200) NOT NULL,
	reviewType enum("pro", "con") NOT NULL, 
	FOREIGN KEY (dormID) REFERENCES dorm(dormID) ON DELETE CASCADE,
	FOREIGN KEY (roomNumber) REFERENCES room(roomNumber) ON DELETE CASCADE, 
	FOREIGN KEY (BID) REFERENCES user(BID) ON DELETE CASCADE
	)
	-- table constraints follow                   
	ENGINE = InnoDB;

DROP TABLE IF EXISTS photo;
CREATE TABLE photo(
	dormID char(3) NOT NULL,
	roomNumber char(3) NOT NULL,
	BID char(8) NOT NULL,
	path varchar(100) NOT NULL,
	FOREIGN KEY (dormID) REFERENCES dorm(dormID) ON DELETE CASCADE,
	FOREIGN KEY (roomNumber) REFERENCES room(roomNumber) ON DELETE CASCADE, 
	FOREIGN KEY (BID) REFERENCES user(BID) ON DELETE CASCADE
	)
	-- table constraints follow                                              
       ENGINE = InnoDB;
	
