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
	
