create table ROUTINE (
	video_num int(7) not null,
	sex varchar(2) not null,
	length int(3) not null,
	timing varchar(10) not null,
	bodypart varchar(20) not null,
	level varchar(2) not null,
	url varchar(100) not null,
	primary key (video_num)
);

create table EXERCISE (
	video_num int(7) not null,
	sex varchar(2) not null,
	length int(3) not null,
	timing varchar(10) not null,
	bodypart varchar(20) not null,
	excer_type varchar(10) not null,
	trainer varchar(15) not null,
	equipment varchar(20) not null,
	level varchar(2) not null,
	url varchar(100) not null,
	primary key (video_num)
);

create table ROUTINETHEME(
	theme_num int(2) not null,
	theme varchar(30) not null,
	primary key(theme_num)
);

create table DETAILSTEP(
	theme_num int(1) not null,
	step_num int(2) not null,
	length int(3) not null,
	timing varchar(22) not null,
	bodypart varchar(42) not null,
	excer_type varchar(22) not null,
	equipment varchar(42) not null,
	primary key(theme_num, step_num)
);


create table REGISTER(
	ID varchar(20) not null,
	PW varchar(100) not null,
	user_num int(6) not null,
	user_point int(6) not null,
	watch_num int(4) not null,
	watch_time int(6) not null,
	open_box int(1) not null,
	primary key(ID)
);


create table USER (
	user_num int(6) not null,
	sex varchar(1) not null,
	age int(3) not null,
	bodypart varchar(20) not null,
	health_point int(3) not null,
	label int(1) DEFAULT 0,
	primary key(user_num)
);


create table HISTORY (
	user_num int(7) not null,
	video_num int(7) not null,
	rating int(1) not null,
	time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ALTER TABLE REGISTER ADD FOREIGN KEY (user_num) REFERENCES USER(user_num);
-- ALTER TABLE ROUTINETHEME ADD FOREIGN KEY (theme_num) REFERENCES DETAILSTEP(theme_num);