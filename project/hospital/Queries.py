from django.db import connection
from django.contrib.auth.models import User
import traceback

def Login_Query(username, password):
    '''Output: Subject_id and role if user is authenticated and None otherwise'''
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select subject_id, \"role\" from subjects where user_name = %s and \"password\" = %s"
        cursor.execute(Query, (username, password, ))
        result_set = cursor.fetchall()
    finally:
        cursor.close()
        return result_set

def valid_targets(subject_id):
    '''Output: valid targets of this user'''
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select target_type from target_assignment where subject_id = %s"
        cursor.execute(Query, (subject_id, ))
        result_set = cursor.fetchall()
    finally:
        cursor.close()
        return result_set

# Needed??
def write_access(subject_id):
    '''Output: list of all objects this user has write access to them'''
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select * from write_access(%(id)S)"
        cursor.execute(Query, ({'id':subject_id}))
        result_set = cursor.fetchall()
    finally:
        cursor.close()
        return result_set

def write_query(Query, subject_id):
    '''Input: Query in form of <Update ~ set ~ where ~ > <delete from ~ where ~ >
    ** It should have where clause
    ** It shouldn't finish with ";"
    Output: 0 if successful and 1 otherwise'''
    cursor = connection.cursor()
    success = 0
    try:
        Query = Query + ' and object_id in (select * from write_access(%s))'%(subject_id)
        # print(Query)
        cursor.execute(Query, ())
    except:
        success = 1
        print('bad Query')
    finally:
        cursor.close()
        return success

def read_query(Query, subject_id):
    '''Input: Query in form of <Select ~ from ~ where ~ >
    ** It should have where clause
    ** It shouldn't finish with ";"
    Output: query output'''
    cursor = connection.cursor()
    result_set = None
    try:
        Query = Query + ' and object_id in (select * from read_access(%s))'%(subject_id)
        # print(Query)
        cursor.execute(Query, ())
        result_set = cursor.fetchall()
    except:
        print('bad Query')
    finally:
        cursor.close()
        return result_set

def add_report(subject_id, object_id, detail):
    '''Input: subject_id and object_id of reporter(object_id for access settings of report)
        Output: 0 if successful and 1 otherwise'''
    cursor = connection.cursor()
    success = 0
    try:
        Query = "Call add_report(%s, %s, %s)"
        cursor.execute(Query, (subject_id, object_id, detail))
    except:
        print(traceback.format_exc())
        success = 1
        print('bad Query')
    finally:
        cursor.close()
        return success

def register_patient(registeration_id,f_name, l_name, national_id, age, sex,
                     illness, section_id, drugs, doctor_id, nurse_id, user, passw):
    '''Input: patient info
        Output: 0 if successful and 1 otherwise'''
    user = User.objects.create_user(username=user, password=passw)
    user.save()
    cursor = connection.cursor()
    success = 0
    try:
        Query = "Call register_patient(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(Query, (registeration_id, f_name, l_name, national_id, age, sex,
                               illness, section_id, drugs, doctor_id, nurse_id, user.id))
    except:
        # print(traceback.format_exc())
        success = 1
        print('bad Query')
    finally:
        cursor.close()
        return success

def export_name(subject_id):
    '''Output: valid targets of this user'''
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select * from export_data(%s)"
        cursor.execute(Query, (subject_id,))
        result_set = cursor.fetchall()
    finally:
        cursor.close()
        return result_set

def my_privacy(object_id):
    '''Output: Accesses ...'''
    cursor = connection.cursor()
    result_set = None
    try:
        Query = '''select subject_id, target from access_log a
                    where a.object_id = %s'''
        cursor.execute(Query, (object_id, ))
        result_set = cursor.fetchall()
    finally:
        cursor.close()
        return result_set
