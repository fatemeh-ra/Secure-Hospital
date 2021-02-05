from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            context = {}
            context['id'] = User.objects.get(username=user.username).pk
            context['full_name'] = User.objects.get(username=user.username).username
            auth.login(request, user)
            # . . . 
            return render(request , '../Templates/Query.html' , context)
       
        else:
            return render(request, '../Templates/login.html', {'error':'Invalid Username Or Password'})
    else:
        return render(request , '../Templates/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return render(request,'../Templates/home.html')
    
