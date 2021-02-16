from hospital.models import *
from django.contrib.auth.models import User
from random import randint, choice
from django.db import connection


def add_test_doctors(n, b):
    for i in range(n):
        user = User.objects.create_user(username='doc'+str(b+i), password='pass_doc'+str(b+i))
        user.save()
        obj = Objects(asl='U',msl='U',csl='U')
        obj.save()
        sec = Sections.objects.filter(section_id=100+randint(1,4))[0]
        doc = Doctors(subject_id=user.id, object_id=obj.object_id, f_name='fname'+str(b+i), l_name='lname'+str(b+i),
                      national_id='127'+str(b+i), speciality='spec', section=sec)
        doc.save()

def add_test_nurses(n, b):
    for i in range(n):
        user = User.objects.create_user(username='nurse'+str(b+i), password='pass_nurse'+str(b+i))
        user.save()
        obj = Objects(asl='U',msl='U',csl='U')
        obj.save()
        sec = Sections.objects.filter(section_id=100+randint(1,4))[0]
        doc = Nurses(subject_id=user.id, object_id=obj.object_id, f_name='fname'+str(b+i), l_name='lname'+str(b+i),
                      national_id='1278'+str(b+i), section=sec)
        doc.save()

def add_test_employees(n, b):
    for i in range(n):
        user = User.objects.create_user(username='emp'+str(b+i), password='pass_emp'+str(b+i))
        user.save()
        obj = Objects(asl='U',msl='U',csl='U')
        obj.save()
        j = choice(['administrative', 'inspection', 'other'])
        doc = Employees(subject_id=user.id, object_id=obj.object_id, f_name='fname'+str(b+i), l_name='lname'+str(b+i),
                      national_id='1279'+str(b+i), job=j)
        doc.save()


def add_manager():
    cursor = connection.cursor()
    try:
        cursor.execute("insert into Manager values(%s)", (50,))
    finally:
        cursor.close()


















