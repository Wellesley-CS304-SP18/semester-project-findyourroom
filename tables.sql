DROP TABLE IF EXISTS dorm;
CREATE TABLE dorm(
	dormID char(3) NOT NULL PRIMARY KEY,  
	dormName enum("Bates", "Beebe", "Cazenove", "Cervantes", "Claflin", "Dower",
	"Freeman", "French House", "Hemlock", "Instead", "Lake House", "McAfee", 
	"Munger", "Orchard", "Pomeroy","Severance", "Shafer", "Simpson West", "Stone Davis", 
	"Tower Court East", "Tower Court West") NOT NULL,
	location enum("East Side", "West Side") NOT NULL,
	dormType enum("dorm","apartment") NOT NULL, /*come back to this later*/
	specialdorm tinyint(1) NOT NULL, /*if the dorm has language requirement etc */ 
	gym tinyint(1) NOT NULL,		/*0 if no gym, 1 if there's a gym*/
	dinningHall tinyint(1) NOT NULL /*0 if no dinninghall, 1 if there's a dinninghall*/
);

/*update the gym part*/
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("BAT", "Bates", "West Side", "dorm", 0, 0, 1); 
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("BEB", "Beebe", "West Side", "dorm", 0, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("CAZ", "Cazenove", "West Side", "dorm", 0, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("CER", "Cervantes", "West Side", "dorm", 0, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("CLA", "Claflin", "West Side", "dorm", 0, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("DOW", "Dower", "East Side", "dorm", 0, 0, 1); 
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("FRE", "Freeman", "East Side", "dorm", 0, 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("FHC", "French House", "East Side", "dorm",1, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("HEM", "Hemlock", "East Side", "dorm",0, 1, 0); 
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("INS", "Instead", "East Side", "dorm",1, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("LAK", "Lake House", "West Side", "dorm", 0, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("MAC", "McAfee", "East Side", "dorm",0, 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("MUN", "Munger", "West Side", "dorm", 0, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("ORC", "Orchard", "East Side", "dorm", 0, 1, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("POM", "Pomeroy", "West Side", "dorm", 0, 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("SEV", "Severance", "West Side", "dorm", 0, 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("SHA", "Shafer", "West Side", "dorm",0, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("SMW", "Simpson West", "East Side", "dorm",0 , 1, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("STO", "Stone Davis", "East Side", "dorm",0, 0, 0);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("TCE", "Tower Court East", "West Side", "dorm",0 , 0, 1);
INSERT INTO dorm (dormID, dormName, location, dormType, specialdorm, gym, dinningHall)  VALUES ("TCW", "Tower Court West", "West Side", "dorm", 0, 0, 1);

/* is if fine to have both foreign key and primary key?*/
DROP TABLE IF EXISTS room;
CREATE TABLE room(
	dormID char(3) NOT NULL, 
	roomNumber char(3) NOT NULL, 
	avgRating decimal(3,2),
	FOREIGN KEY (dormID) REFERENCES dorm(dormID), 
	PRIMARY KEY (roomNumber,dormID)
);

INSERT INTO room (dormID, roomNumber)  VALUES ("MUN", "234");
INSERT INTO room (dormID, roomNumber)  VALUES ("SEV", "125");
INSERT INTO room (dormID, roomNumber)  VALUES ("POM", "504");

DROP TABLE IF EXISTS review;
CREATE TABLE review(
	dormID char(3) NOT NULL,
	roomNumber char(3) NOT NULL,
	BID char(9) NOT NULL,
	rating tinyint(5); 
	comment varchar(200) NOT NULL,
	reviewType enum("pro", "con") NOT NULL, 
	FOREIGN KEY (dormID) REFERENCES dorm(dormID),
	FOREIGN KEY (roomNumber) REFERENCES room(roomNumber)
);

DROP TABLE IF EXISTS photo;
CREATE TABLE photo(
	dormID char(3) NOT NULL,
	roomNumber char(3) NOT NULL,
	BID char(9) NOT NULL,
	length int(5) NOT NULL, 
	path varchar(100) NOT NULL,
	FOREIGN KEY (dormID) REFERENCES dorm(dormID),
	FOREIGN KEY (roomNumber) REFERENCES room(roomNumber)
);
	
DROP TABLE IF EXISTS user;
CREATE TABLE user(
	email varchar(20) NOT NULL PRIMARY KEY, 
	pwd varchar(20) NOT NULL,
	BID char(9) NOT NULL, 
	classYear int(4)NOT NULL, 
);

