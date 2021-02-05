from django.shortcuts import render

# Create your views here.


def Register(request):
    if not request.GET.get('show', False):
        print("sorry ")
    else:
        return render(request,'../Templates/AddPatient.html') 


    