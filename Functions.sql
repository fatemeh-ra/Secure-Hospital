
---------------------------------------------------------------------------------------
-- Read & Write access

drop function geq
create or replace function geq(f char(3), s char(3))
returns boolean
as $$
begin 
	if f = 'TS' then 
		return 1;
	elseif f = 'S' and s <> 'TS' then
		return 1;
	elseif f = 'C' and s <> 'TS' and s <> 'S' then 
		return 1;
	elseif f = 'U' and s = 'U' then 
		return 1;
	else 
		return 0;
	end if;
end
$$ LANGUAGE plpgsql;

--select * from nurses n where n.object_id in (select * from write_access(3))
--update Nurses set age = 25 where age < 25 and subject_id in (select * from write_access(3))

create function write_access(id int)
returns table(object_id int)
as $$
begin
	return query
		select o.object_id from objects o
		where geq((select asl from subjects s2 where subject_id = id) , o.csl)
		and geq(o.asl, (select wsl from subjects s2 where subject_id = id))
		and (select section_id from object_category oc where oc.object_id = o.object_id) 
			in (select section_id from subject_category sc where sc.subject_id = id);
end
$$ LANGUAGE plpgsql;	

create function read_access(id int)
returns table(object_id int)
as $$
begin
	return query
		select o.object_id from objects o
		where geq(o.msl, (select asl from subjects s2 where subject_id = id))
		and geq((select rsl from subjects s2 where subject_id = id), o.asl)
		and (select section_id from object_category oc where oc.object_id = o.object_id) 
			in (select section_id from subject_category sc where sc.subject_id = id);
end
$$ LANGUAGE plpgsql;	

-------------------------------------------------------------------------------------------------
-- Report

--drop procedure add_report 
create or replace procedure add_report(subj_id integer, obj_id integer, detail varchar(255))
as $$
declare 
	r varchar(20);
begin 	
	insert into objects (asl, csl, msl)
	select asl, csl, msl from objects o where o.object_id  = obj_id;

	select "role" into r from subjects s where s.subject_id = $1;
	if r = 'patient' then
		insert into object_category (object_id, section_id)
		select max(object_id), 202 from objects;
	else 
		insert into object_category (object_id, section_id)
		select max(object_id), 201 from objects;
	end if;
	

	insert into object_targets (target_type, object_id) 
	select 'report_handling', max(object_id) from objects;
	insert into reports (reporter_id, object_id, detail)
	select subj_id, max(object_id), detail from objects;
end
$$ LANGUAGE plpgsql;


-------------------------------------------------------------------------------------------------
-- Patient Registeration

create or replace procedure register_patient(f_name varchar(255), l_name varchar(255),
	national_id INT, age INT, sex char(10), illness VARCHAR (255), section_id INT, drugs VARCHAR (255), 
	doctor_id INT, nurse_id int, id int)
as $$
declare 
	o int;
begin 	
	insert into objects (asl, csl, msl) values ('C', 'S', 'S');
	select max(object_id) into o from objects;

	insert into object_category (object_id, section_id) values (o, section_id);

	update subjects set "role" = 'patient'
	where subject_id = id;
	insert into subject_category (subject_id, section_id) values (id, section_id);
	
	insert into patients values (default, id, o, f_name, l_name, national_id,
	"age", sex, illness, section_id, drugs, doctor_id, nurse_id);
end
$$ LANGUAGE plpgsql;

--call register_patient (123, 'name', 'lname', 129, 18, 'Male', 'nothing', 101, 'nothing', 3, 2, 'p1','passp1')



-------------------------------------------------------------------------------------------------
-- Export user data (name)


drop function export_data(int);
create or replace function export_data(id int)
returns table(role varchar(255), f_name varchar(255), lname varchar(255), national_id int, section_id int, object_id int)
as $$
declare 
	r varchar(20);
begin 	
	select s.role into r from subjects s where s.subject_id = $1;
	if r = 'doctor' then
		return query select r, d.f_name, d.l_name, d.national_id, d.section_id, d.object_id from doctors d where d.subject_id = $1;
	elseif r = 'nurse' then
		return query select r, n.f_name, n.l_name, n.national_id, n.section_id, n.object_id from nurses n where n.subject_id = $1;
	elseif r = 'employee' then
		return query select r, e.f_name, e.l_name, e.national_id, 105, e.object_id from employees e where e.subject_id = $1;
	elseif r = 'patient' then
		return query select r, p.f_name, p.l_name, p.national_id, p.section_id, p.object_id from patients p where p.subject_id = $1;
	end if;
end
$$ LANGUAGE plpgsql;	

--select * from export_data(35)



-------------------------------------------------------------------------------------------------
-- Accesss Comprison


create or replace function write_compare(asl varchar(5), msl varchar(5), csl varchar(5), id int)
returns boolean
as $$
begin 	
	if geq((select s.asl from subjects s where s.subject_id = id) , csl)
		and geq(asl, (select s.wsl from subjects s where s.subject_id = id)) then
		return 1;
	else
		return 0;
	end if;
end
$$ LANGUAGE plpgsql;	

create or replace function read_compare(asl varchar(5), msl varchar(5), csl varchar(5), id int)
returns boolean
as $$
begin 	
	if geq(o.msl, (select s.asl from subjects s where s.subject_id = id))
		and geq((select s.rsl from subjects s where s.subject_id = id), o.asl) then
		return 1;
	else
		return 0;
	end if;
end
$$ LANGUAGE plpgsql;	





