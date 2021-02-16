
-- q1
-- Triggers in Triggers.sql

-- q2
-- Valid Targets
select target_type from target_assignment where subject_id = 1

-- q3
-- Write access objects
select o.object_id from patients p2 inner join objects o on o.object_id = p2.object_id
where o.csl <= (select asl from subjects s2 where subject_id = 1) 
	and o.asl >= (select wsl from subjects s2 where subject_id = 1)
	and (select section_id from object_category oc where oc.object_id = o.object_id) 
		in (select section_id from subject_category sc where sc.subject_id = 1)

-- q3
-- Read access objects
select o.object_id from patients p2 inner join objects o on o.object_id = p2.object_id
where o.csl <= (select asl from subjects s2 where subject_id = 1) 
	and o.asl >= (select wsl from subjects s2 where subject_id = 1)
	and (select section_id from object_category oc where oc.object_id = o.object_id) 
		in (select section_id from subject_category sc where sc.subject_id = 1)

-- q4				
-- My Privacy
select subject_id, access_type, target from access_log a
where a.object_id = 1

-- q6
-- test data in data.sql

-- q7
create or replace function add_report(subject_id integer, object_id integer, detail varchar(255))
returns void
as $$
begin 
	insert into objects (asl, csl, msl)
	select asl, csl, msl from objects o where o.object_id  = object_id;

	insert into object_category (object_id, section_id)
	select max(object_id), 101 from objects;		-- 101 is the report section id, change it in the cotext
	
	insert into reports (reporter_id, object_id, detail)
	select max(object_id), subject_id, detail from objects;
end
$$ LANGUAGE plpgsql;


-- q8
-- Login
select subject_id, "role" from subjects s where user_name = 'user' and "password" = 'pass';


-- q9
-- Patient Registeration
create or replace function register_patient(registeration_id INT, f_name varchar(255), l_name varchar(255),
	national_id INT, age INT, sex char(10), illness VARCHAR (255), section_id INT, drugs VARCHAR (255), 
	doctor_id INT, nurse_id int, username varchar(255), pass varchar(255))
returns void
as $$
declare 
	s int;
	o int;
begin 	
	insert into objects (asl, csl, msl) values ('C', 'S', 'S');
	select max(object_id) into o from objects;

	insert into object_category (object_id, section_id) values (o, section_id);

	insert into subject (asl, rsl, wsl, "role", username, "password") values ('U', 'U', 'U', 'patient', username, pass);
	select max(subject_id) into s from subjects;

	insert into subject_category (subject_id, section_id) values (s, section_id);
	
	insert into patients values (registeration_id, s, o, f_name, l_name, national_id,
	"age", sex, illness, section_id, drugs, doctor_id, nurse_id, username, pass);
end
$$ LANGUAGE plpgsql;
--drop function register_patient


-- q10
-- LOGGING
-- TODO



