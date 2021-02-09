from django.db import connection
from django.contrib.auth.models import User
import traceback


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
    '''Output: list of all objects this user has write access to them
    or 1 if error happens'''
    cursor = connection.cursor()
    result_set = None
    success = 0
    try:
        Query = "select * from write_access(%(id)S)"
        cursor.execute(Query, ({'id':subject_id}))
        result_set = cursor.fetchall()
    except: success = 1
    finally:
        cursor.close()
        if success: return success
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


def insert_query_exec(Query):
    print(Query)
    cursor = connection.cursor()
    success = 0 
    try:
        cursor.execute(Query , ())
    except:
        success = 1 
        print(traceback.format_exc())
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

def register_patient(f_name, l_name, national_id, age, sex,
                     illness, section_id, drugs, doctor_id, nurse_id, user, passw):
    '''Input: patient info
        Output: subject_id if successful and -1 otherwise'''
    user = User.objects.create_user(username=user, password=passw)
    cursor = connection.cursor()
    result = -1
    try:
        Query = "Call register_patient( %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s )"
        print("---------------------------------------------------------------------------")
        print(Query %(f_name, l_name, national_id, age, sex,
                               illness, section_id, drugs, doctor_id, nurse_id, user.id) ) 
        cursor.execute(Query, (f_name, l_name, national_id, age, sex,
                               illness, section_id, drugs, doctor_id, nurse_id, user.id))
        result = user.id
    except:
        print(traceback.format_exc())
        print('bad Query')
    finally:
        cursor.close()
        if(result == -1): user.delete()
        return result

def export_data(subject_id):
    '''Output: user data : role, fname, lname, national_id, section, object_id'''
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select * from export_data(%s)"
        cursor.execute(Query, (subject_id,))
        result_set = cursor.fetchall()
    finally:
        # print(traceback.format_exc())
        cursor.close()
        return result_set


def register_access(subject_id):
    if is_manager(subject_id) : return True
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select role from subjects where subject_id = %s"
        cursor.execute(Query, (subject_id,))
        result_set = cursor.fetchall()
    finally:
        cursor.close()
    # print(result_set[0][0])
    if result_set != None and result_set[0][0] == 'employee':
        cursor = connection.cursor()
        result_set = None
        try:
            Query = "select job from employees where subject_id = %s"
            cursor.execute(Query, (subject_id,))
            result_set = cursor.fetchall()
        finally:
            cursor.close()
        if result_set != None and result_set[0][0] == 'administrative':
            return True
    return False


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



def check_table_clevel(t_name , subject_id):
    db_tables = {'Doctors':('TS', 'TS', 'S'),'Nurses':('S', 'TS', 'S'),
                 'Employees':('TS', 'TS', 'S'),'Reports':('TS', 'TS', 'S')} # TODO: these values must be edited
    cursor = connection.cursor()
    result_set = None
    try:
        Query = 'select * from write_compare(\'%s\', \'%s\', \'%s\', %s)'%(db_tables[t_name]+(subject_id,))
        print(Query)
        cursor.execute(Query)
        result_set = cursor.fetchall()
    finally:
        print(traceback.format_exc())
        cursor.close()
        return result_set


def is_manager(subject_id):
    cursor = connection.cursor()
    result_set = None
    try:
        cursor.execute("select * from Manager where manager_id = %s", (subject_id, ))
        result_set = cursor.fetchall()
    finally:
        cursor.close()

    if result_set != []: return True

    cursor = connection.cursor()
    result_set = None
    try:
        cursor.execute("select * from system_manager where manager_id = %s", (subject_id,))
        result_set = cursor.fetchall()
    finally:
        cursor.close()

    if result_set != []: return True
    return False

def manager_read_query(Query):
    # print(Query)
    cursor = connection.cursor()
    result_set = None
    success = 0
    try:
        cursor.execute(Query, ())
        result_set = cursor.fetchall()
    except:
        success = 1
        print(traceback.format_exc())
    finally:
        cursor.close()
        if success: return success
        return result_set


def manager_write_query(Query):
    # print(Query)
    cursor = connection.cursor()
    success = 0
    try:
        cursor.execute(Query, ())
    except:
        success = 1
        print(traceback.format_exc())
    finally:
        cursor.close()
        return success


def culomn_names(table):
    cursor = connection.cursor()
    result_set = None
    try:
        cursor.execute('SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s', (table.lower(), ))
        result_set = cursor.fetchall()
    except:
        print(traceback.format_exc())
    finally:
        cursor.close()
        return result_set







