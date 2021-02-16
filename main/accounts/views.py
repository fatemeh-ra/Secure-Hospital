from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import User
import re
from hospital import TestData
from hospital import Queries
from hospital import Targets
# Create your views here.
error_message = """<center style="padding-top: 300px;"><span style="font-size:100px;"">&#10060;
</span><div style="background-color: rgb(37, 189, 209); width: 500px; height: 60px;  border-radius: 10px;">
<h2 style="font-family: "Roboto Condensed", sans-serif; padding-top: 20px;  "> %s</h2></div></center>')"""

success_message = """<center style="padding-top: 300px;"><span style="font-size:100px;"">&#9996;
</span><div style="background-color: rgb(37, 189, 209); width: 500px; height: 60px;  border-radius: 10px;">
 <h2 style="font-family: "Roboto Condensed", sans-serif ;  padding-top: 20px;  "> %s</h2></div></center>'"""


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            context = {}
            context['id'] = User.objects.get(username=user.username).pk
            context['full_name'] = User.objects.get(username=user.username).username
            context['canAddPatients'] = Queries.register_access(User.objects.get(username=user.username).pk)
            valid_functions = Queries.valid_targets(context['id'])
            export_function = Queries.export_data(context['id'])[0]
            user_extra_data = []
            valid_targets = []
            for i in export_function:
                user_extra_data.append(i)
            for l in valid_functions:
                valid_targets.append(l[0])
            context['usr_role'] = user_extra_data[0]
            context['Name'] = user_extra_data[1]
            context['Fname'] = user_extra_data[2]
            context['nationalID'] = user_extra_data[3]
            context['SectionId'] = user_extra_data[4]
            context['objectid'] = user_extra_data[5]
            context['valid_targets'] = valid_targets
            auth.login(request, user)
            # . . . 
            return render(request , '../Templates/Query.html' , context  )
       
        else:
            return render(request, '../Templates/login.html', {'error':'Invalid Username Or Password'})
    else:
        return render(request , '../Templates/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return render(request,'../Templates/home.html')
    
def sentQuery(request):
        db_tables = ['Doctors','Nurses','Employees','Reports' , 'Patients']
        manager_db_tables = ['Sections', 'Subject_Category', 'Object_Category', 'Section_Manager', 'Manager',
                             'System_Manager', 'Administrative_assistant', 'Medical_assistant', 'Target_assignment',
                             'Object_Targets', 'Access_Log']

        if request.method == 'POST':
            #SELECT column1, column2, ...
            #FROM table_name

            #section for select queies 
            User_query_target = request.POST['usrpoint']
            user_Id = request.POST['subjectID']
            user_role = request.POST['Role']

            if request.POST['sentQuery'][0:5].lower() == 'selec':
                select_elements = re.findall(r'"(.+?)"',request.POST['sentQuery'])
                selected_col = select_elements[0].strip().split(',')
                select_from = select_elements[1].strip()
                select_where = ''
                
                if (len(select_elements) > 2):
                    select_where = select_elements[2].strip()
                if (select_from in db_tables):
                    main_Query = re.sub('["]' , '' , request.POST['sentQuery'])
                    if (select_where == ''):
                        main_Query = main_Query + 'where 1=1'
                    main_Query = re.sub('[;@#$!^&%-]' , '' , main_Query) 
                    #send query to check targets
                    Query_response_list = []
                    context = {}
                    if selected_col[0] == '*':
                        cols = Queries.culomn_names(select_from)
                        cols2 = []
                        for t in cols:
                            cols2.append(t[0])
                        modified_select_col = ''
                        counter = 0
                        for l in cols2:
                            counter = counter + 1
                            if (counter < len(cols2)):
                                modified_select_col = modified_select_col + l +','
                            else:
                                modified_select_col = modified_select_col + l
                        if (select_where == ''):
                            select_where = '1=1'        
                        main_Query = 'select ' + modified_select_col + ' from ' + select_from + ' where ' + select_where   
                        context['colName'] = cols2
                    else:
                        context['colName'] = selected_col
                    if (select_from == 'Patients'):

                        if (Targets.target_check_patient(select_where ,User_query_target , 0,user_Id , user_role ) == 0):
                            Targets.log_access(select_from ,select_where , User_query_target , user_Id , 0)
                            Query_response_list = Queries.read_query(main_Query , user_Id)
                            if(Query_response_list == 1):
                                return HttpResponse(error_message % 'Query Syntax Error')
                            else:
                                context['QueryResults'] = Query_response_list
                                return render(request , '../Templates/showResults.html' , context)

                        else:
                            return HttpResponse(error_message%'Target missmatch with Query')
                    else:
                        if (Targets.check_targets(select_from ,select_where , User_query_target ) == 0):
                            Targets.log_access(select_from ,select_where , User_query_target , user_Id , 0)
                            Query_response_list = Queries.read_query(main_Query , user_Id)
                            if (Query_response_list == 1):
                                return HttpResponse(error_message % 'Query Syntax Error')
                            else:
                                context['QueryResults'] = Query_response_list
                                return render(request, '../Templates/showResults.html', context)

                        else:
                            return HttpResponse(error_message%'Target missmatch with Query')
                elif Queries.is_manager(user_Id) and select_from in manager_db_tables:
                    main_Query = re.sub('["]', '', request.POST['sentQuery'])
                    main_Query = re.sub('[;@#$!^&%-]', '', main_Query)
                    Query_response_list = []
                    context = {}
                    if selected_col[0] == '*':
                        cols = Queries.culomn_names(select_from)
                        cols2 = []
                        for t in cols:
                            cols2.append(t[0])
                        modified_select_col = ''
                        counter = 0
                        for l in cols2:
                            counter = counter + 1
                            if (counter < len(cols2)):
                                modified_select_col = modified_select_col + l + ','
                            else:
                                modified_select_col = modified_select_col + l
                        if (select_where == ''):
                            select_where = '1=1'
                        main_Query = 'select ' + modified_select_col + ' from ' + select_from + ' where ' + select_where
                        context['colName'] = cols2
                    else:
                        context['colName'] = selected_col
                    Query_response_list = Queries.manager_read_query(main_Query)
                    if (Query_response_list == 1):
                        return HttpResponse(error_message % 'Query Syntax Error')
                    else:
                        context['QueryResults'] = Query_response_list
                        return render(request, '../Templates/showResults.html', context)

                else:
                    return HttpResponse(error_message%'Table not found')

            #DELETE FROM table_name WHERE condition;
           
            #section for delete queies 

            elif request.POST['sentQuery'][0:5].lower() == 'delet'.lower():
                delete_elements = re.findall(r'"(.+?)"',request.POST['sentQuery'])
                del_table = delete_elements[0].strip()
                
                del_condition = ''
                if (len(delete_elements) > 1):
                    del_condition = delete_elements[1].strip()
                if (del_table in db_tables):
                    main_Query = re.sub('["]' , '' , request.POST['sentQuery'])
                    if (del_condition == ''):
                        main_Query = main_Query + 'where 1=1'
                    main_Query = re.sub('[;@#$!^&%-]' , '' , main_Query) 
                    if (del_table != 'Patients' ):
                        if ( Targets.check_targets(del_table ,del_condition , User_query_target ) == 0):
                            Targets.log_access(del_table ,del_condition , User_query_target , user_Id , 1)
                            if (Queries.write_query(main_Query , user_Id) == 0):
                                return HttpResponse(success_message%'Query Done Successfully')
                            else:
                                return HttpResponse(error_message%'Query Syntax Error')
                        else:
                            return HttpResponse(error_message%'Target missmatch with Query')
                    else:
                        if (Targets.target_check_patient(del_condition ,User_query_target , 1, user_Id , user_role ) == 0):
                            Targets.log_access(del_table ,del_condition , User_query_target , user_Id , 1)
                            if (Queries.write_query(main_Query , user_Id) == 0):
                                return HttpResponse(success_message%'Query Done Successfully')
                            else:
                                return HttpResponse(error_message%'Query Syntax Error')
                        else:
                            return HttpResponse(error_message%'Target missmatch with Query')
                elif Queries.is_manager(user_Id) and del_table in manager_db_tables:
                    main_Query = re.sub('["]', '', request.POST['sentQuery'])
                    main_Query = re.sub('[;@#$!^&%-]', '', main_Query)
                    if( Queries.manager_write_query(main_Query) ):
                        return HttpResponse(success_message % 'Query Done Successfully')
                    else:
                        return HttpResponse(error_message % 'Query Syntax Error')
                else:
                    return HttpResponse(error_message % 'Table not found')

            # UPDATE table_name
            #  SET column1 = value1, column2 = value2, ...
            #  WHERE condition;


            #section for update queies 

            elif request.POST['sentQuery'][0:5].lower() == 'updat'.lower():
                update_elements = re.findall(r'"(.+?)"',request.POST['sentQuery'])
                up_table = update_elements[0].strip()
                up_col = update_elements[1].strip()
                up_condition = ''
                if (len(update_elements) > 2):
                    up_condition = update_elements[2].strip()
                if (up_table in db_tables):
                    main_Query = re.sub('["]' , '' , request.POST['sentQuery']) 
                    if (up_condition == ''):
                        main_Query = main_Query + 'where 1=1'
                    main_Query = re.sub('[;@#$!^&%-]' , '' , main_Query)
                    if (up_table != 'Patients'):
                        if ( Targets.check_targets(up_table ,up_condition , User_query_target ) == 0):
                            Targets.log_access(up_table ,up_condition , User_query_target , user_Id , 1)
                            if (Queries.write_query(main_Query , user_Id) == 0):
                                return HttpResponse(success_message % 'Query Done Successfully')
                            else:
                                return HttpResponse(error_message%'Query Syntax Error')
                        else:
                            return HttpResponse(error_message % 'Target missmatch with Query')
                    elif(up_table == 'Patients'):
                        if (Targets.target_check_patient(up_condition,User_query_target,1,user_Id,user_role) == 0):
                            Targets.log_access(up_table ,up_condition , User_query_target , user_Id , 1)
                            if (Queries.write_query(main_Query , user_Id) == 0):
                                return HttpResponse(success_message%'Query Done Successfully')
                            else:
                                return HttpResponse(error_message%'Query Syntax Error')
                        else: 
                            return HttpResponse(error_message%'Target missmatch with Query')
                elif Queries.is_manager(user_Id) and up_table in manager_db_tables:
                    main_Query = re.sub('["]', '', request.POST['sentQuery'])
                    main_Query = re.sub('[;@#$!^&%-]', '', main_Query)
                    if( Queries.manager_write_query(main_Query) ):
                        return HttpResponse(success_message % 'Query Done Successfully')
                    else:
                        return HttpResponse(error_message % 'Query Syntax Error')
                else:
                    return HttpResponse(error_message % 'Table not found')




            #INSERT INTO table_name (column1, column2, column3, ...)
            #VALUES (value1, value2, value3, ...)
             #section for insert queies 

             
            elif request.POST['sentQuery'][0:5].lower() == 'inser'.lower():
                insert_elements = re.findall(r'"(.+?)"',request.POST['sentQuery'])
                ins_table = insert_elements[0].strip()
                ins_col = insert_elements[1].strip().split(',')
                ins_val = insert_elements[2].strip().split(',')
                if (ins_table in db_tables):
                    
                    main_Query = re.sub('["]' , '' , request.POST['sentQuery']) 
                    main_Query = re.sub('[;@#$!^&%-]' , '' , main_Query)   

                    if (Queries.check_table_clevel(ins_table,user_Id)[0][0]  and (Queries.insert_query_exec(main_Query) == 0)):
                        
                        return HttpResponse('query done ')
                    else:
                        return HttpResponse('its not ok ')    

                elif Queries.is_manager(user_Id) and ins_table in manager_db_tables:
                    main_Query = re.sub('["]', '', request.POST['sentQuery'])
                    main_Query = re.sub('[;@#$!^&%-]', '', main_Query)
                    if( Queries.insert_query_exec(main_Query) == 0):
                        return HttpResponse(success_message % 'Query Done Successfully')
                    else:
                        return HttpResponse(error_message % 'Query Syntax Error')
                return HttpResponse('error : table not found')



def Myprivacy(request):
    user_object_id = request.POST['object_id']
    my_privacy_list = Queries.my_privacy(int(user_object_id))
    col_name = ['Subject_id' , 'access']
    context = {}
    context['colName'] = col_name

    context['QueryResults'] = my_privacy_list
    return render(request, '../Templates/showResults.html' ,context )


def Reports(request):
    context = {}
    context['object_id'] = request.POST['object_id']
    context['subjectID'] = request.POST['subjectID']

    return render(request , '../Templates/Reports.html' , context)


def submitreport(request):
    report_text = request.POST['report']
    object_id = request.POST['object_id']
    subjectID = request.POST['subjectID']
    
    if(Queries.add_report(subjectID , object_id , report_text) == 0):
       return HttpResponse('<center style="padding-top: 300px;"><span style="font-size:100px;"">&#9996;</span><div style="background-color: rgb(37, 189, 209); width: 500px; height: 60px;  border-radius: 10px;"> <h1 style="font-family: "Roboto Condensed", sans-serif ;  padding-top: 10px;  "> Report added successfully </h1></div></center>') 
    else:
       return HttpResponse('<center style="padding-top: 300px;"><span style="font-size:100px;"">&#10060;</span><div style="background-color: rgb(37, 189, 209); width: 500px; height: 60px;  border-radius: 10px;"> <h1 style="font-family: "Roboto Condensed", sans-serif ;  padding-top: 10px;  "> Report add did not successfully </h1></div></center>')                           