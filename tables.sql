DROP TABLE IF EXISTS review;
CREATE TABLE review(
	RID int(1) NOT NULL,
	roomNum int(3) NOT NULL,
	type emun ("pro", "con","none") NOT NULL, 
	comment varchar(200) NOT NULL,
	FOREIGN KEY (RID) REFERENCES dorm(RID),
	FOREIGN KEY (roomNum) REFERENCES room(roomNumber)
);

DROP TABLE IF EXISTS photo;
CREATE TABLE photo(
	RID int(1) NOT NULL,
	roomNum int(3) NOT NULL,
	length int(5) NOT NULL, 
	path varchar(100) NOT NULL,
	FOREIGN KEY (RID) REFERENCES dorm(RID),
	FOREIGN KEY (roomNum) REFERENCES room(roomNumber)
);
	
DROP TABLE IF EXISTS user;
CREATE TABLE user(
	pwd varchar(20) NOT NULL,
	email varchar(20) NOT NULL, 
	classYear int(4)NOT NULL, 
	BID char(9) NOT NULL,
	rating int(1),
	yearLivedIn date,
	RID int(1), 
	roomNumber varchar(3),
	FOREIGN KEY (roomNumber) REFERENCES room roomNumber)
	FOREIGN KEY (RID) REFERENCES dorm(RID)
);

DROP TABLE IF EXISTS dorm;
CREATE TABLE dorm(
	RID int(1) PRIMARY KEY, 
	Name enum("Bates" "Beebe", "Cazenove", "Cedar Lodge", "Cervantes", "Clafflin", "Dower",
	"Freeman", "French House", "Hemlock", "Homestead/Instead", "Lake House", "McAfee", 
	"Munger", "Orchard", "Pomeroy","Severance", "Shafer", "Simpson West", "Stone/Davis", "Tower"),
	location enum("East", "West"),
	type enum("dorm","apartment","language"), 
	gym tinyint(1),
	dinningHall tinyint(1)	
);

DROP TABLE IF EXISTS room;
CREATE TABLE room(
	roomNumber varchar(3) NOT NULL PRIMARY KEY, 
	RID int(1), 
	avgRating decimal(5,2),
	FOREIGN KEY (RID) REFERENCES dorm(RID)
);

