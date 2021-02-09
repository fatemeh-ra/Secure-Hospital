from django.db import connection
from hospital.Queries import is_manager

def check_targets(query_from, query_where, target):
    """Output: 0 if all targets are valid, 1 otherwise"""
    cursor = connection.cursor()
    result_set = None
    success = 0
    try:
        Query = "select object_id from %s where %s" % (query_from, query_where,)
        cursor.execute(Query)
        result_set = cursor.fetchall()
    finally:
        cursor.close()

    for i in result_set:
        cursor = connection.cursor()
        try:
            cursor.execute("select target_type from object_targets where object_id = %s", (i))
            res = cursor.fetchall()
            res2 = []
            for l in res:
                res2.append(l[0])
            if target not in res2:
                success = 1
                break
        finally:
            cursor.close()

    return success
    


def log_access(query_from, query_where, target, subject_id, read_write):
    """Input read_write: 0 for raed Query, 1 for write query"""
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select object_id from %s where %s"%(query_from, query_where,)
        cursor.execute(Query)
        result_set = cursor.fetchall()
    except:
        print("erro acc 2  ")     
    finally:
        cursor.close()

    cursor = connection.cursor()
    result_set2 = None
    if read_write == 0:
        try:
            Query = "select * from read_access(%s)" % (subject_id,)
            cursor.execute(Query)
            result_set2 = cursor.fetchall()
        except:
            print("erro acc 1  ")          
        finally:
            cursor.close()
    elif read_write == 1:
        try:
            Query = "select * from write_access(%s)" % (subject_id,)
            cursor.execute(Query)
            result_set2 = cursor.fetchall()
        except:
            print("erro acc ")
        finally:
            cursor.close()
            

    print(result_set, result_set2)
    
    for i in list(set(result_set) & set(result_set2)):
        cursor = connection.cursor()
        try:
            cursor.execute("insert into Access_Log values(default, %s, %s, %s)", (subject_id, i, target, ))
        finally:
            cursor.close()


def add_patient_targets(targets, subject_id):
    '''Input: a list of valid targets and id of newly added patient'''
    cursor = connection.cursor()
    object_id = None
    try:
        Query = "select object_id from patients where subject_id=%s" % (subject_id,)
        cursor.execute(Query)
        object_id = cursor.fetchall()[0][0]
    except:
        print("error")
    finally:
        cursor.close()

    if object_id == None : return
    for t in targets:
        cursor = connection.cursor()
        try:
            Query = "insert into object_targets(target_type,object_id) values ('%s', %s)" % (t, object_id,)
            cursor.execute(Query)
        except:
            print("error")
        finally:
            cursor.close()

def target_check_patient(query_where, target, read_write, subject_id, role):
    """Input read_write: 0 for raed Query, 1 for write query
    Output: 0 if all targets are valid, 1 otherwise"""
    success = 0
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select object_id from Patients where %s" % (query_where,)
        cursor.execute(Query)
        result_set = cursor.fetchall()
    except:
        print("error acc 2  ")
    finally:
        cursor.close()

    cursor = connection.cursor()
    result_set2 = None
    if read_write == 0:
        try:
            Query = "select * from read_access(%s)" % (subject_id,)
            cursor.execute(Query)
            result_set2 = cursor.fetchall()
        except:
            print("error acc 1  ")
        finally:
            cursor.close()
    elif read_write == 1:
        try:
            Query = "select * from write_access(%s)" % (subject_id,)
            cursor.execute(Query)
            result_set2 = cursor.fetchall()
        except:
            print("error acc ")
        finally:
            cursor.close()


    for i in list(set(result_set) & set(result_set2)):
        cursor = connection.cursor()
        try:
            cursor.execute("select target_type from object_targets where object_id = %s", (i))
            res = cursor.fetchall()
            res2 = []
            for l in res:
                res2.append(l[0])
        finally:
            cursor.close()
            print(res2, target, role)

        if is_manager(subject_id):
            if target in res2:
                continue

        if role == 'doctor':
            cursor = connection.cursor()
            doc = None
            try:
                cursor.execute("select doctor_id from Patients where object_id = %s", (i,))
                ret = cursor.fetchall()
                doc = ret[0][0]
            finally:
                cursor.close()
            if doc == subject_id:
                if target+'_personal_doc' not in res2:
                    success = 1
                    break
            else:
                if target+'_section_doc' not in res2:
                    success = 1
                    break

        elif role == 'nurse':
            cursor = connection.cursor()
            nur = None
            try:
                cursor.execute("select nurse_id from Patients where object_id = %s", (i,))
                nur = cursor.fetchall()[0][0]
            finally:
                cursor.close()
            if nur == subject_id:
                if target + '_personal_nurse' not in res2:
                    success = 1
                    break
            else:
                success = 1
                break

        elif role == 'employee':
            if target not in res2:
                success = 1
                break

        else:
            success = 1
            break

    return success



