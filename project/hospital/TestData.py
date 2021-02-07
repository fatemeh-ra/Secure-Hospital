from hospital.models import *
from django.contrib.auth.models import User
from random import randint, choice
from django.db import connection


def add_test_doctors(n):
    for i in range(n):
        user = User.objects.create_user(username='doc'+str(i), password='pass_doc'+str(i))
        user.save()
        obj = Objects(asl='U',msl='U',csl='U')
        obj.save()
        sec = Sections.objects.filter(section_id=100+randint(1,4))[0]
        doc = Doctors(subject_id=user.id, object_id=obj.object_id, f_name='fname'+str(i), l_name='lname'+str(i),
                      national_id='127'+str(i), speciality='spec', section=sec)
        doc.save()

def add_test_nurses(n):
    for i in range(n):
        user = User.objects.create_user(username='nurse'+str(i), password='pass_nurse'+str(i))
        user.save()
        obj = Objects(asl='U',msl='U',csl='U')
        obj.save()
        sec = Sections.objects.filter(section_id=100+randint(1,4))[0]
        doc = Nurses(subject_id=user.id, object_id=obj.object_id, f_name='fname'+str(i), l_name='lname'+str(i),
                      national_id='1278'+str(i), section=sec)
        doc.save()

def add_test_employees(n):
    for i in range(n):
        user = User.objects.create_user(username='emp'+str(i), password='pass_emp'+str(i))
        user.save()
        obj = Objects(asl='U',msl='U',csl='U')
        obj.save()
        j = choice(['administrative', 'Inspection', 'other'])
        doc = Employees(subject_id=user.id, object_id=obj.object_id, f_name='fname'+str(i), l_name='lname'+str(i),
                      national_id='1279'+str(i), job=j)
        doc.save()


def add_manager():
    cursor = connection.cursor()
    try:
        cursor.execute("insert into Manager values(%s)", (50,))
    finally:
        cursor.close()


















