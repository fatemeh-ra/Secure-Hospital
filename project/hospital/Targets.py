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
            if target not in res:
                success = 1
                break
        finally:
            cursor.close()

        return success
    pass


def log_access(query_from, query_where, target, subject_id, read_write):
    """Input read_write: 0 for raed Query, 1 for write query"""
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select object_id from %s where %s"%(query_from, query_where,)
        cursor.execute(Query)
        result_set = cursor.fetchall()
    finally:
        cursor.close()

    cursor = connection.cursor()
    result_set2 = None
    if read_write == 0:
        try:
            Query = "select * from read_access(%s)" % (subject_id,)
            cursor.execute(Query)
            result_set2 = cursor.fetchall()
        finally:
            cursor.close()
    elif read_write == 1:
        try:
            Query = "select * from write_access(%s)" % (subject_id,)
            cursor.execute(Query)
            result_set2 = cursor.fetchall()
        finally:
            cursor.close()

    # print(result_set, result_set2, list(set(result_set) & set(result_set2)))
    
    for i in list(set(result_set) & set(result_set2)):
        cursor = connection.cursor()
        try:
            cursor.execute("insert into Access_Log values(default, %s, %s, %s)", (subject_id, i, target, ))
        finally:
            cursor.close()
