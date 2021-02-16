# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdministrativeAssistant(models.Model):
    assistant = models.ForeignKey('Doctors', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'administrative_assistant'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Doctors(models.Model):
    subject = models.OneToOneField('Subjects', models.DO_NOTHING, primary_key=True)
    object = models.ForeignKey('Objects', models.DO_NOTHING)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    national_id = models.IntegerField(unique=True)
    speciality = models.CharField(max_length=255)
    section = models.ForeignKey('Sections', models.DO_NOTHING)
    employment_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    marital_status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctors'


class Employees(models.Model):
    subject = models.OneToOneField('Subjects', models.DO_NOTHING, primary_key=True)
    object = models.ForeignKey('Objects', models.DO_NOTHING)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    national_id = models.IntegerField(unique=True)
    job = models.CharField(max_length=255)
    employment_date = models.DateField()
    age = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField()
    marital_status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'


class Manager(models.Model):
    manager = models.ForeignKey(Doctors, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'manager'


class MedicalAssistant(models.Model):
    assistant = models.ForeignKey(Doctors, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'medical_assistant'


class Nurses(models.Model):
    subject = models.OneToOneField('Subjects', models.DO_NOTHING, primary_key=True)
    object = models.ForeignKey('Objects', models.DO_NOTHING)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    national_id = models.IntegerField(unique=True)
    section = models.ForeignKey('Sections', models.DO_NOTHING)
    employment_date = models.DateField()
    age = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField()
    marital_status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nurses'


class ObjectCategory(models.Model):
    object = models.OneToOneField('Objects', models.DO_NOTHING, primary_key=True)
    section = models.ForeignKey('Sections', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'object_category'
        unique_together = (('object', 'section'),)


class ObjectTargets(models.Model):
    target_id = models.AutoField(primary_key=True)
    target_type = models.CharField(max_length=20)
    object = models.ForeignKey('Objects', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'object_targets'


class Objects(models.Model):
    object_id = models.AutoField(primary_key=True)
    asl = models.CharField(max_length=5)
    msl = models.CharField(max_length=5)
    csl = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'objects'


class Patients(models.Model):
    registeration_id = models.IntegerField(primary_key=True)
    subject = models.ForeignKey('Subjects', models.DO_NOTHING)
    object = models.ForeignKey(Objects, models.DO_NOTHING)
    f_name = models.CharField(unique=True, max_length=255)
    l_name = models.CharField(unique=True, max_length=255)
    national_id = models.IntegerField(unique=True)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    illness = models.CharField(max_length=255, blank=True, null=True)
    section = models.ForeignKey('Sections', models.DO_NOTHING)
    drugs = models.CharField(max_length=255, blank=True, null=True)
    doctor = models.ForeignKey(Doctors, models.DO_NOTHING)
    nurse = models.ForeignKey(Nurses, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'patients'


class Reports(models.Model):
    report_id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey('Subjects', models.DO_NOTHING)
    object = models.ForeignKey(Objects, models.DO_NOTHING)
    detail = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reports'


class SectionManager(models.Model):
    section = models.OneToOneField('Sections', models.DO_NOTHING, primary_key=True)
    manager = models.ForeignKey(Doctors, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'section_manager'
        unique_together = (('section', 'manager'),)


class Sections(models.Model):
    section_id = models.IntegerField(primary_key=True)
    section_name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'sections'


class SubjectCategory(models.Model):
    subject = models.OneToOneField('Subjects', models.DO_NOTHING, primary_key=True)
    section = models.ForeignKey(Sections, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'subject_category'
        unique_together = (('subject', 'section'),)


class Subjects(models.Model):
    subject_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10)
    asl = models.CharField(max_length=5)
    rsl = models.CharField(max_length=5)
    wsl = models.CharField(max_length=5)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'subjects'


class SystemManager(models.Model):
    manager = models.ForeignKey(Employees, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system_manager'


class TargetAssignment(models.Model):
    target_id = models.AutoField(primary_key=True)
    target_type = models.CharField(max_length=20)
    subject = models.ForeignKey(Subjects, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'target_assignment'
