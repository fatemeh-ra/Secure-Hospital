--drop table section_manager;
--drop table patient;
--drop table Doctors;
--drop table Nurses;
--drop table Employees;
--drop table Sections;

create table Sections(
	section_id INT not null PRIMARY KEY,
	section_name VARCHAR (255) UNIQUE NOT null
);

create table All_personels(
	personel_id INT primary key,
	role varchar(10) not null check (role in ('doctor', 'nurse', 'employee')),
	subject_ASL varchar(5) not null check (subject_ASL in ('TS', 'S', 'C', 'U')), -- Absolute
	subject_RSL varchar(5) not null check (subject_RSL in ('TS', 'S', 'C', 'U')), -- Read
	subject_WSL varchar(5) not null check (subject_WSL in ('TS', 'S', 'C', 'U')), -- Write
	object_ASL varchar(5) not null check (object_ASL in ('TS', 'S', 'C', 'U')),
	object_RSL varchar(5) not null check (object_RSL in ('TS', 'S', 'C', 'U')),
	object_WSL varchar(5) not null check (object_WSL in ('TS', 'S', 'C', 'U'))
);

create table Category(
	subject_id INT not null references All_personels(personel_id),
	section_id INT not null references Sections(section_id),
	primary key(subject_id, section_id)
);


CREATE TABLE Doctors(
	personel_id INT not null PRIMARY key references All_personels(personel_id),
	f_name VARCHAR (255) NOT null,
	l_name VARCHAR (255) NOT null,
	national_id INT UNIQUE NOT null,
	specialty VARCHAR (255) NOT null,
	section_id INT references sections(section_id),
	employment_date DATE not null,
	age INT,
	salary INT not null,
	marital_status varchar(8) check (marital_status in ('married', 'single'))
);


CREATE TABLE Nurses(
	personel_id INT not null PRIMARY key references All_personels(personel_id),
	f_name VARCHAR (255) NOT null,
	l_name VARCHAR (255) NOT null,
	national_id INT UNIQUE NOT null,
	section_id INT not null references sections(section_id),
	employment_date DATE not null,
	age INT,
	salary INT not null,
	marital_status char(8) check (marital_status in ('married', 'single'))
);


CREATE table Employees(
	personel_id INT not null PRIMARY key references All_personels(personel_id),
	f_name VARCHAR (255) NOT null,
	l_name VARCHAR (255) NOT null,
	national_id INT UNIQUE NOT null,
	job VARCHAR (255) NOT null check (job in ('financial', 'official', 'other')),
	employment_date DATE not null,
	age INT,
	salary INT not null,
	marital_status char(8) check (marital_status in ('married', 'single'))
);


CREATE TABLE Patients(
	registeration_id INT not null PRIMARY key,
	f_name VARCHAR (255) UNIQUE NOT null,
	l_name VARCHAR (255) UNIQUE NOT null,
	national_id INT UNIQUE NOT null,
	age INT,
	sex char(10) check (sex in ('Male', 'Female')),
	illness VARCHAR (255),
	section_id INT not null references Sections(section_id),
	drugs VARCHAR (255),
	doctor_id INT not null references Doctors(personel_id),
	nurse_id INT not null references Nurses(personel_id)
);


create table Section_Manager(
	section_id INT not null references Sections(section_id),
	manager_id INT not null references Doctors(personel_id),
	primary key(section_id, manager_id)
);

create table Manager(
	manager_id int not null references Doctors(personel_id)
);

create table System_Manager(
	manager_id int not null references Employees(personel_id)
);

create table Administrative_assistant(
	assistant_id int not null references Doctors(personel_id)
);

create table Medical_assistant(
	assistant_id int not null references Doctors(personel_id)
);

create table Target_assignment(
	target_id serial not null primary key,
	target_type varchar(20) not null, -- check (target_type in ('')) TODO
	subject_id int not null references All_personels(personel_id)
);

create table Patient_Targets(
	target_id serial not null primary key,
	target_type varchar(20) not null, -- check (target_type in ('')) TODO
	subject_id int not null references Patients(registeration_id)
);

create table Login_personel(
	user_name varchar(255) not null primary key,
	password varchar(255) not null,
	register_id int not null references All_personels(personel_id)
);

create table Reports_personel(
	report_id serial not null primary key,
	reporter_id int not null references All_personels(personel_id),
	detail varchar(255)
);

create table Login_patients(
	user_name varchar(255) not null primary key,
	password varchar(255) not null,
	register_id int not null references Patients(registeration_id)
);

create table Reports_patients(
	report_id serial not null primary key,
	reporter_id int not null references Patients(registeration_id),
	detail varchar(255)
);


