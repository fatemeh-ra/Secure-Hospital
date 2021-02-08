
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
