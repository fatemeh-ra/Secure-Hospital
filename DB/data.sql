
-- q8

insert into sections values
(101, 'General'),	
(102, 'Speciality'),
(103, 'Subspecialty'),
(104, 'Emergency'),
(105, 'Official'),
(201, 'Reports'),
(202, 'Patient_Reports');

delete from auth_user where username='doc0'

delete from employees 

update Nurses set commands = 'first command. ' where subject_id = 111;
update Nurses set commands = 'Second command. ' where subject_id = 111;

update Doctors set section_id = 101 where subject_id = 122

select role from subjects s where s.subject_id = 50

insert into manager values(147);

insert into system_manager values(169);

insert into section_manager values(101, 154);

delete from section_manager 

delete from doctors where subject_id = 152;

SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'doctors';

delete from Nurses where subject_id = 163

select * from export_data(150)

call add_report(169, 24, 'report')

insert into medical_assistant values(150)

delete from administrative_assistant 
delete from medical_assistant 







