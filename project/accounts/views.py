from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import User
import re
from hospital import TestData
from hospital import Queries
# Create your views here.
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            context = {}
            context['id'] = User.objects.get(username=user.username).pk
            context['full_name'] = User.objects.get(username=user.username).username
            valid_functions = Queries.valid_targets(context['id'])
            valid_targets = []
            for l in valid_functions:
                valid_targets.append(l[0])

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
        db_tables = ['Doctors','Nurses','Employees','Reports']

        if request.method == 'POST':
            #SELECT column1, column2, ...
            #FROM table_name

            #section for select queies 
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
                    return HttpResponse(main_Query)
                else:
                    HttpResponse("Error : table name font find in DB")
                    

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
                    return HttpResponse(main_Query)
                else:
                    return HttpResponse('Error : bad query ')

            # UPDATE table_name
            #  SET column1 = value1, column2 = value2, ...
            #  WHERE condition;


            #section for update queies 

            elif request.POST['sentQuery'][0:5].lower() == 'updat'.lower():
                update_elements = re.findall(r'"(.+?)"',request.POST['sentQuery'])
                up_table = update_elements[0].strip()
                up_col = update_elements[1].strip()
                up_condition = ''
                if (len(delete_elements) > 2):
                    del_condition = delete_elements[2].strip()
                if (up_table in db_tables):
                    main_Query = re.sub('["]' , '' , request.POST['sentQuery']) 
                    if (up_condition == ''):
                        main_Query = main_Query + 'where 1=1'
                    main_Query = re.sub('[;@#$!^&%-]' , '' , main_Query)       
                    return HttpResponse(main_Query)
                return HttpResponse('error : table not found ')



         
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
                    return HttpResponse(main_Query)
                return HttpResponse('error : table not found')
