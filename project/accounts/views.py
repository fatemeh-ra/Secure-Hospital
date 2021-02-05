from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            # . . . 
            return redirect('../mainpage' , )
       
        else:
            return render(request, '../Templates/login.html', {'error':'Invalid Username Or Password'})
    else:
        return render(request , '../Templates/login.html')

def loggedin(request):
    
