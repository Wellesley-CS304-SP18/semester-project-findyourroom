drop table if exists review;
create table review(
	RID int(1),
	roomNum int(3),
	pro boolean,
	con boolean, 
	comment varchar(100),
	foreign key (RID) references dormInfo(RID),
	foreign key (roomNum) references roomInfo(roomNumber)
);
	
	
