/*
* Created by: Mana Muchaku, Renee Huang, and Serena Fan
* CS304
*
* creates new tables for entities: userInputInfo, userInfo, roomInfo, dormInfo 
* Drops tables if they already exist and recreate new ones
*/

-- change to user's db
use rhuang_db; 


drop table if exists userInfo;
create table userInfo(
	pwd varchar(20),
	email varchar(20), 
	classYear int(4), 
	BID char(9),
	primary key(BID)
);

drop table if exists dormInfo;
create table dormInfo(
	resHallName enum("Bates", "Tower", "Claflin", "Pomeroy", "Shafer", "Munger", "Freeman", "Severance"),
	RID int(1), 

	primary key (RID)
);

drop table if exists roomInfo;
create table roomInfo(
	prosAndCons text, 
	photos BLOB,
	avgRating decimal(5,2),
	roomNumber varchar(3), 
	RID int(1), 

	primary key (roomNumber),
	foreign key (RID) references dormInfo(RID)
);



drop table if exists userInputInfo;
create table userInputInfo(
	BID char(9),
	photos BLOB,
	rating int(1),
	yearLivedIn date,
	roomNumber varchar(3),
	foreign key (BID) references userInfo(BID),
	foreign key (roomNumber) references roomInfo(roomNumber)
);

drop table if exists review;
create table review(
	RID int(1) not null,
	roomNum int(3) not null,
	pro tinyint(1),
	con tinyint(1), 
	comment varchar(100) not null,
	foreign key (RID) references dormInfo(RID),
	foreign key (roomNum) references roomInfo(roomNumber)
);

drop table if exists photo;
create table photo(
	RID int(1) not null,
	roomNum int(3) not null,
	length int(5) not null, 
	path varchar(100) not null,
	foreign key (RID) references dormInfo(RID),
	foreign key (roomNum) references roomInfo(roomNumber)
);
	



insert into userInfo values ("1234", "rhuang@wellesley.edu", "2018", "B20769110");
insert into userInfo values ("1234", "mmuchaku@wellesley.edu", "2018", "B20769111");
insert into userInfo values ("1234", "sfan@wellesley.edu", "2018", "B20769112");

insert into dormInfo values ("Pomeroy", 1);
insert into dormInfo values ("Freeman", 2);
insert into dormInfo values ("Serverance", 3);
insert into dormInfo values ("Munger", 4);
	

insert into roomInfo (roomNumber, RID) values ("504", 1);
insert into roomInfo (roomNumber, RID) values ("243", 4);
insert into roomInfo (roomNumber, RID) values ("111", 3);


insert into userInputInfo (BID, rating, yearLivedIn, roomNumber) values ("B20769110", 4, 2018, "504");
insert into userInputInfo (BID, rating, yearLivedIn, roomNumber) values ("B20769111", 4, 2018, "243");
insert into userInputInfo (BID, rating, yearLivedIn, roomNumber) values ("B20769112", 3, 2018, "111");