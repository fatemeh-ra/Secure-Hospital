from django.db import connection


def check_targets(query_from, query_where, target):
    """Output: 0 if all targets are valid, 0 otherwise"""
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


def log_access(query_from, query_where, target, subject_id):
    cursor = connection.cursor()
    result_set = None
    try:
        Query = "select object_id from %s where %s"%(query_from, query_where,)
        cursor.execute(Query)
        result_set = cursor.fetchall()
    finally:
        cursor.close()

    for i in result_set:
        cursor = connection.cursor()
        try:
            cursor.execute("insert into Access_Log values(default, %s, %s, %s)", (subject_id, i, target, ))
        finally:
            cursor.close()
