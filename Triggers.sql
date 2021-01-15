
-- q1

-- Doctor
create or replace function insert_doc_func() RETURNS trigger AS $insert_doc$
BEGIN
	update subjects set asl = 'S', rsl = 'S', wsl = 'U', "role" = 'doctor'
	where subject_id = new.subject_id;
	insert into subject_category (subject_id, section_id) 
	values (new.subject_id, new.section_id);

	update objects set asl = 'TS', msl = 'TS', csl = 'S'
	where object_id = new.object_id;
	insert into object_category (object_id, section_id)
	values (new.object_id , new.section_id);

-- TODO	: set doctor valid targets
	-- insert into target_assignment values () 
	RETURN NEW;  
END;
$insert_doc$ LANGUAGE plpgsql;

drop trigger insert_doc on Doctors;
create trigger insert_doc before insert on Doctors
    FOR EACH ROW EXECUTE PROCEDURE insert_doc_func();

----------------------------------------------------------------------------------------------
-- Nurse
create or replace function insert_nurse_func() RETURNS trigger AS $insert_nurse$
BEGIN
	update subjects set asl = 'C', rsl = 'C', wsl = 'U', "role" = 'nurse'
	where subject_id = new.subject_id;
	insert into subject_category (subject_id, section_id)
	values (new.subject_id, new.section_id);

	update objects set asl = 'S', msl = 'TS', csl = 'S'
	where object_id = new.object_id;
	insert into object_category (object_id, section_id)
	values (new.object_id , new.section_id);

-- TODO	: set Nurse valid targets
	-- insert into target_assignment values () 
	RETURN NEW;  
END;
$insert_nurse$ LANGUAGE plpgsql;

drop trigger insert_nurse on Nurses;
create trigger insert_nurse before insert on Nurses
    FOR EACH ROW EXECUTE PROCEDURE insert_nurse_func();

----------------------------------------------------------------------------------------------
-- Employee
create or replace function insert_emp_func() RETURNS trigger AS $insert_emp$
BEGIN
	update subjects set asl = 'S', rsl = 'S', wsl = 'U', "role" = 'employee'
	where subject_id = new.subject_id;
	insert into subject_category (subject_id, section_id)
	values (new.subject_id, new.section_id);

	update objects set asl = 'TS', msl = 'TS', csl = 'S'
	where object_id = new.object_id;
	insert into object_category (object_id, section_id)
	values (new.object_id , new.section_id);

-- TODO	: set Employee valid targets
	-- insert into target_assignment values () 
	RETURN NEW;  
END;
$insert_emp$ LANGUAGE plpgsql;

-- drop trigger insert_emp on Employee;
create trigger insert_emp before insert on Employees
    FOR EACH ROW EXECUTE PROCEDURE insert_emp_func();

 
 ----------------------------------------------------------------------------------------------
-- Manager
create or replace function insert_manager_func() RETURNS trigger AS $insert_manager$
BEGIN
	update subjects set rsl = 'TS'
	where subject_id = new.manager_id;

-- TODO : How to add all sections to category?? Manually??
	--insert into subject_category (subject_id, section_id) values ();

-- TODO	: How to set all targets?
	-- insert into target_assignment values () 
	RETURN NEW;  
END;
$insert_manager$ LANGUAGE plpgsql;

-- drop trigger insert_manager on Manager;
create trigger insert_manager before insert on Manager
    FOR EACH ROW EXECUTE PROCEDURE insert_manager_func();
   
create or replace function del_manager_func() RETURNS trigger AS $del_manager$
BEGIN
	update subjects set rsl = 'S'
	where subject_id = new.manager_id;

-- TODO : Remove categories

-- TODO	: Remove targets
	RETURN NEW;  
END;
$del_manager$ LANGUAGE plpgsql;

-- drop trigger insert_manager on Manager;
create trigger del_manager before delete on Manager
    FOR EACH ROW EXECUTE PROCEDURE del_manager_func();

 ----------------------------------------------------------------------------------------------
-- System Manager

-- same as Manager
-- drop trigger insert_manager on System_Manager;
create trigger insert_manager before insert on System_Manager
    FOR EACH ROW EXECUTE PROCEDURE insert_manager_func();
   
create or replace function del_sysmanager_func() RETURNS trigger AS $del_sysmanager$
BEGIN
	update subjects set rsl = 'S'
	where subject_id = new.manager_id;

-- TODO : Remove categories

-- TODO	: Remove targets
	RETURN NEW;  
END;
$del_sysmanager$ LANGUAGE plpgsql;

-- drop trigger insert_manager on System_Manager;
create trigger del_sysmanager before delete on System_Manager
    FOR EACH ROW EXECUTE PROCEDURE del_sysmanager_func();

 ----------------------------------------------------------------------------------------------
-- Section Manager
create or replace function insert_manager_func() RETURNS trigger AS $insert_sec_manager$
BEGIN
	update subjects set rsl = 'TS'
	where subject_id = new.manager_id;

-- TODO	: Does it need more targets??
	-- insert into target_assignment values () 
	RETURN NEW;  
END;
$insert_sec_manager$ LANGUAGE plpgsql;

-- drop trigger insert_sec_manager on Section_Manager;
create trigger insert_sec_manager before insert on Section_Manager
    FOR EACH ROW EXECUTE PROCEDURE insert_manager_func();

create or replace function del_manager_func() RETURNS trigger AS $del_sec_manager$
BEGIN
	update subjects set rsl = 'S'
	where subject_id = new.manager_id;

-- TODO	: Delete added targets
	-- insert into target_assignment values () 
	RETURN NEW;  
END;
$del_sec_manager$ LANGUAGE plpgsql;

-- drop trigger del_sec_manager on Section_Manager;
create trigger del_sec_manager before insert on Section_Manager
    FOR EACH ROW EXECUTE PROCEDURE del_sec_manager_func();
   
   
 ----------------------------------------------------------------------------------------------
-- Section Manager
create or replace function insert_sec_manager_func() RETURNS trigger AS $insert_sec_manager$
BEGIN
	update subjects set rsl = 'TS'
	where subject_id = new.manager_id;

-- TODO	: Does it need more targets??
	-- insert into target_assignment values () 
	RETURN NEW;  
END;
$insert_sec_manager$ LANGUAGE plpgsql;

-- drop trigger insert_sec_manager on Section_Manager;
create trigger insert_sec_manager before insert on Section_Manager
    FOR EACH ROW EXECUTE PROCEDURE insert_sec_manager_func();

create or replace function del_sec_manager_func() RETURNS trigger AS $del_sec_manager$
BEGIN
	update subjects set rsl = 'S'
	where subject_id = new.manager_id;

-- TODO	: Delete added targets
	-- insert into target_assignment values () 
	RETURN NEW;  
END;
$del_sec_manager$ LANGUAGE plpgsql;

-- drop trigger del_sec_manager on Section_Manager;
create trigger del_sec_manager before insert on Section_Manager
    FOR EACH ROW EXECUTE PROCEDURE del_sec_manager_func();
      
   
----------------------------------------------------------------------------------------------
-- Administrative Assistant
create or replace function insert_admin_assist_func() RETURNS trigger AS $insert_admin_assist$
BEGIN
	update subjects set rsl = 'TS'
	where subject_id = new.assistant_id;

-- TODO	: Add all non-medical sections

	RETURN NEW;  
END;
$insert_admin_assist$ LANGUAGE plpgsql;

-- drop trigger insert_admin_assist on Administrative_assistant;
create trigger insert_admin_assist before insert on Administrative_assistant
    FOR EACH ROW EXECUTE PROCEDURE insert_admin_assist_func();

create or replace function del_admin_assist_func() RETURNS trigger AS $del_admin_assist$
BEGIN
	update subjects set rsl = 'S'
	where subject_id = new.assistant_id;

-- TODO	: Delete added sections

	RETURN NEW;  
END;
$del_admin_assist$ LANGUAGE plpgsql;

-- drop trigger del_admin_assist on Administrative_assistant;
create trigger del_admin_assist before insert on Administrative_assistant
    FOR EACH ROW EXECUTE PROCEDURE del_admin_assist_func();
      
    
----------------------------------------------------------------------------------------------
-- Medical Assistant
create or replace function insert_med_assist_func() RETURNS trigger AS $insert_med_assist$
BEGIN
	update subjects set rsl = 'TS'
	where subject_id = new.assistant_id;

-- TODO	: Add all medical sections

	RETURN NEW;  
END;
$insert_med_assist$ LANGUAGE plpgsql;

-- drop trigger insert_admin_assist on Medical_assistant;
create trigger insert_med_assist before insert on Medical_assistant
    FOR EACH ROW EXECUTE PROCEDURE insert_med_assist_func();

create or replace function del_med_assist_func() RETURNS trigger AS $del_med_assist$
BEGIN
	update subjects set rsl = 'S'
	where subject_id = new.assistant_id;

-- TODO	: Delete added Sections

	RETURN NEW;  
END;
$del_med_assist$ LANGUAGE plpgsql;

-- drop trigger del_med_assist on Medical_assistant;
create trigger del_med_assist before insert on Medical_assistant
    FOR EACH ROW EXECUTE PROCEDURE del_med_assist_func();
      
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
 