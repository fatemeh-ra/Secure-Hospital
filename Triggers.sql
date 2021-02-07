
-- sync django authentication with our model

create or replace function sync_subject() RETURNS trigger AS $sync$
BEGIN
	insert into subjects (subject_id, asl, rsl, wsl) 
	values (new.id, 'U', 'U', 'U');

	RETURN NEW;  
END;
$sync$ LANGUAGE plpgsql;

-- drop trigger sync on auth_user;
create trigger sync after insert on auth_user
    FOR EACH ROW EXECUTE PROCEDURE sync_subject();


----------------------------------------------------------------------------------------------
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

	-- set doctor valid targets
	insert into target_assignment values 
	(default, 'checkup', new.subject_id),
	(default, 'prescribe', new.subject_id),
	(default, 'give_command', new.subject_id),
	(default, 'records', new.subject_id);

	insert into object_targets values
	(default, 'medical_staff_management', new.object_id),
	(default, 'bills', new.object_id),
	(default, 'annual_report', new.object_id),
	(default, 'debt_calculation', new.object_id),
	(default, 'report_handling', new.object_id);

	RETURN NEW;  
END;
$insert_doc$ LANGUAGE plpgsql;

-- drop trigger insert_doc on Doctors;
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

	-- set nurse valid targets
	insert into target_assignment values 
	(default, 'patient_care', new.subject_id),
	(default, 'records', new.subject_id);

	insert into object_targets values
	(default, 'medical_staff_management', new.object_id),
	(default, 'bills', new.object_id),
	(default, 'annual_report', new.object_id),
	(default, 'debt_calculation', new.object_id),
	(default, 'give_command', new.object_id),
	(default, 'report_handling', new.object_id);

	RETURN NEW;  
END;
$insert_nurse$ LANGUAGE plpgsql;

--drop trigger insert_nurse on Nurses;
create trigger insert_nurse before insert on Nurses
    FOR EACH ROW EXECUTE PROCEDURE insert_nurse_func();


----------------------------------------------------------------------------------------------
-- Employee
create or replace function insert_emp_func() RETURNS trigger AS $insert_emp$
BEGIN
	update subjects set asl = 'S', rsl = 'S', wsl = 'U', "role" = 'employee'
	where subject_id = new.subject_id;
	insert into subject_category (subject_id, section_id)
	values (new.subject_id, 105);

	update objects set asl = 'TS', msl = 'TS', csl = 'S'
	where object_id = new.object_id;
	insert into object_category (object_id, section_id)
	values (new.object_id , 105);

	if new.job = 'administrative' then
		update subjects set  rsl = 'TS'
		where subject_id = new.subject_id;
		insert into subject_category (subject_id, section_id) values
		(new.subject_id, 101),
		(new.subject_id, 102),
		(new.subject_id, 103),
		(new.subject_id, 104);
	
	elseif new.job = 'inspection' then
		update subjects set  rsl = 'TS'
		where subject_id = new.subject_id;
		insert into subject_category (subject_id, section_id) values 
		(new.subject_id, 201),
		(new.subject_id, 202);
	end if;

	-- set employee valid targets
	insert into target_assignment values 
	(default, 'bills', new.subject_id),
	(default, 'annual_report', new.subject_id),
	(default, 'debt_calculation', new.subject_id);

	insert into object_targets values
	(default, 'official_staff_management', new.object_id),
	(default, 'bills', new.object_id),
	(default, 'annual_report', new.object_id),
	(default, 'debt_calculation', new.object_id),
	(default, 'report_handling', new.object_id);

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

	insert into subject_category (subject_id, section_id) values
	(new.manager_id, 101),
	(new.manager_id, 102),
	(new.manager_id, 103),
	(new.manager_id, 104),
	(new.manager_id, 105),
	(new.manager_id, 201);

	insert into target_assignment values 
	(default, 'medical_staff_management', new.manager_id),
	(default, 'official_staff_management', new.manager_id),
	(default, 'bills', new.manager_id),
	(default, 'annual_report', new.manager_id),
	(default, 'report_handling', new.manager_id),
	(default, 'debt_calculation', new.manager_id);

	RETURN NEW;  
END;
$insert_manager$ LANGUAGE plpgsql;

-- drop trigger insert_manager on Manager;
create trigger insert_manager before insert on Manager
    FOR EACH ROW EXECUTE PROCEDURE insert_manager_func();
   
create or replace function del_manager_func() RETURNS trigger AS $del_manager$
BEGIN
	update subjects set rsl = 'S'
	where subject_id = old.manager_id;

	delete from subject_category where subject_id = old.manager_id;
	insert into subject_category (subject_id, section_id) values
	(old.manager_id, (select section_id from doctors where subject_id = old.manager_id));

	delete from target_assignment where subject_id = old.manager_id;
	insert into target_assignment values 
	(default, 'checkup', old.manager_id),
	(default, 'prescribe', old.manager_id),
	(default, 'give_command', old.manager_id),
	(default, 'records', old.manager_id);

	RETURN OLD;  
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
	where subject_id = old.manager_id;
	
	delete from subject_category where subject_id = old.manager_id;
	insert into subject_category (subject_id, section_id) values
	(old.manager_id, 105);

	if new.job = 'administrative' then
		update subjects set  rsl = 'TS'
		where subject_id = old.manager_id;
		insert into subject_category (subject_id, section_id) values
		(old.manager_id, 101),
		(old.manager_id, 102),
		(old.manager_id, 103),
		(old.manager_id, 104);
	end if;

	delete from target_assignment where subject_id = old.manager_id;
	insert into target_assignment values 
	(default, 'bills', old.manager_id),
	(default, 'annual_report', old.manager_id),
	(default, 'debt_calculation', old.manager_id);

	RETURN old;  
END;
$del_sysmanager$ LANGUAGE plpgsql;

-- drop trigger insert_manager on System_Manager;
create trigger del_sysmanager before delete on System_Manager
    FOR EACH ROW EXECUTE PROCEDURE del_sysmanager_func();

 ----------------------------------------------------------------------------------------------
-- Section Manager
create or replace function insert_sec_manager_func() RETURNS trigger AS $insert_sec_manager$
BEGIN
	update subjects set rsl = 'TS'
	where subject_id = new.manager_id;

	insert into target_assignment values 
	(default, 'medical_staff_management', new.manager_id);

	RETURN NEW;  
END;
$insert_sec_manager$ LANGUAGE plpgsql;

-- drop trigger insert_sec_manager on Section_Manager;
create trigger insert_sec_manager before insert on Section_Manager
    FOR EACH ROW EXECUTE PROCEDURE insert_sec_manager_func();

--create or replace function del_manager_func() RETURNS trigger AS $del_sec_manager$
--BEGIN
--	update subjects set rsl = 'S'
--	where subject_id = old.manager_id;
--
--	delete from subject_category where subject_id = old.manager_id;
--	insert into subject_category (subject_id, section_id) values
--	(old.manager_id, (select "section" from doctors where subject_id = old.manager_id));
--
--	delete from target_assignment where subject_id = old.manager_id;
--	insert into target_assignment values 
--	(default, 'checkup', old.manager_id),
--	(default, 'prescribe', old.manager_id),
--	(default, 'give_command', old.manager_id),
--	(default, 'records', old.manager_id);
--	RETURN old;  
--END;
--$del_sec_manager$ LANGUAGE plpgsql;

-- drop trigger del_sec_manager on Section_Manager;
create trigger del_sec_manager before insert on Section_Manager
    FOR EACH ROW EXECUTE PROCEDURE del_manager_func();
    
   
----------------------------------------------------------------------------------------------
-- Administrative Assistant
create or replace function insert_admin_assist_func() RETURNS trigger AS $insert_admin_assist$
BEGIN
	update subjects set rsl = 'TS'
	where subject_id = new.assistant_id;
	
	insert into subject_category (subject_id, section_id) values
	(new.assistant_id, 101),
	(new.assistant_id, 102),
	(new.assistant_id, 103),
	(new.assistant_id, 104);

	insert into target_assignment values 
	(default, 'medical_staff_management', new.assistant_id),
	(default, 'report_handling', new.assistant_id);

	RETURN NEW;  
END;
$insert_admin_assist$ LANGUAGE plpgsql;

-- drop trigger insert_admin_assist on Administrative_assistant;
create trigger insert_admin_assist before insert on Administrative_assistant
    FOR EACH ROW EXECUTE PROCEDURE insert_admin_assist_func();

create or replace function del_assist_func() RETURNS trigger AS $del_assist$
BEGIN
	update subjects set rsl = 'S'
	where subject_id = old.assistant_id;

	delete from subject_category where subject_id = old.assistant_id;
	insert into subject_category (subject_id, section_id) values
	(old.assistant_id, (select "section" from doctors where subject_id = old.assistant_id));

	delete from target_assignment where subject_id = old.assistant_id;
	insert into target_assignment values 
	(default, 'checkup', old.assistant_id),
	(default, 'prescribe', old.assistant_id),
	(default, 'give_command', old.assistant_id),
	(default, 'records', old.assistant_id);
	
	return old;
END;
$del_assist$ LANGUAGE plpgsql;

-- drop trigger del_admin_assist on Administrative_assistant;
create trigger del_admin_assist before insert on Administrative_assistant
    FOR EACH ROW EXECUTE PROCEDURE del_assist_func();
      
    
----------------------------------------------------------------------------------------------
-- Medical Assistant
create or replace function insert_med_assist_func() RETURNS trigger AS $insert_med_assist$
BEGIN
	update subjects set rsl = 'TS'
	where subject_id = new.assistant_id;
	
	insert into subject_category (subject_id, section_id) values
	(new.assistant_id, 105);

	insert into target_assignment values 
	(default, 'official_staff_management', new.assistant_id),
	(default, 'bills', new.assistant_id),
	(default, 'annual_report', new.assistant_id),
	(default, 'report_handling', new.assistant_id),
	(default, 'debt_calculation', new.assistant_id);

	RETURN NEW;  
END;
$insert_med_assist$ LANGUAGE plpgsql;

-- drop trigger insert_admin_assist on Medical_assistant;
create trigger insert_med_assist before insert on Medical_assistant
    FOR EACH ROW EXECUTE PROCEDURE insert_med_assist_func();

-- drop trigger del_med_assist on Medical_assistant;
create trigger del_med_assist before insert on Medical_assistant
    FOR EACH ROW EXECUTE PROCEDURE del_assist_func();
      
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
 