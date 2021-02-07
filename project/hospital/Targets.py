from django.db import connection


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
        print(Query)
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





def check_table_clevel(t_name , subject_id):

    db_tables = ['Doctors','Nurses','Employees','Reports']
    